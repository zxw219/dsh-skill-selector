#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import tempfile
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


ALIASES = [
    (r"\bactivision[ -]?blizzard\b|动视暴雪", " activisionblizzard "),
    (r"\bmicrosoft\b|微软", " microsoft "),
    (r"\bnvidia\b|英伟达", " nvidia "),
    (r"\bopenai\b|开放人工智能", " openai "),
    (r"\banthropic\b|安特罗匹克", " anthropic "),
    (r"\bgoogle\b|谷歌", " google "),
    (r"\bapple\b|苹果", " apple "),
    (r"\bxiaomi\b|小米", " xiaomi "),
    (r"\btesla\b|特斯拉", " tesla "),
    (r"\bsmartphones?\b|智能手机|手机", " phone "),
    (r"\bcomputers?\b|\bpcs?\b|计算机|电脑", " computer "),
    (r"\bvehicles?\b|\bcars?\b|车辆|汽车", " car "),
]

EVENTS = {
    "acquire": r"\bacquir(?:e|es|ed|ing)\b|\bacquisition\b|收购|并购",
    "recall": r"\brecall(?:s|ed|ing)?\b|召回",
    "price-up": r"\bprice (?:rise|increase|hike)s?\b|涨价|提价|价格上涨",
    "price-down": r"\bprice (?:cut|drop|reduction)s?\b|降价|价格下调",
    "release": r"\b(?:launch|launches|launched|release|releases|released|unveil|unveils|unveiled)\b|发布|推出|上线|亮相",
    "funding": r"\b(?:funding|financing)\b|融资",
    "listing": r"\b(?:ipo|listing|listed)\b|上市|挂牌",
    "lawsuit": r"\b(?:lawsuit|sues?|sued)\b|起诉|诉讼",
    "ban": r"\b(?:ban|bans|banned|blocked)\b|禁用|封禁|禁止",
    "earnings": r"\b(?:earnings|revenue)\b|财报|营收",
    "security-incident": r"\b(?:breach|breached|hack|hacked|leak|leaked|vulnerability)\b|泄露|入侵|漏洞|安全事件",
    "outage": r"\b(?:outage|downtime|offline)\b|故障|宕机|服务中断",
}

STOP = {"about", "after", "from", "into", "latest", "new", "news", "official", "report", "the", "this", "with", "company"}
WEAK = {"agent", "app", "code", "data", "model", "platform", "store", "system", "tool"}
NOISE = re.compile(r"发布|推出|上线|亮相|收购|并购|召回|涨价|提价|降价|融资|上市|挂牌|起诉|诉讼|禁用|封禁|禁止|财报|营收|正式|宣布|公司|完成|启动|回应|表示|消息|最新|今日|今天", re.I)
TRACKING = {"fbclid", "gclid", "ref", "source", "spm", "utm_campaign", "utm_content", "utm_medium", "utm_source", "utm_term"}


def normalize(title: str) -> str:
    value = title.casefold()
    for pattern, replacement in ALIASES:
        value = re.sub(pattern, replacement, value, flags=re.I)
    value = re.sub(r"[【】\[\]（）()“”'‘’：:｜|·•—–]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def event_kinds(title: str) -> set[str]:
    value = normalize(title)
    return {kind for kind, pattern in EVENTS.items() if re.search(pattern, value, flags=re.I)}


def tokens(title: str) -> set[str]:
    value = NOISE.sub(" ", normalize(title))
    for pattern in EVENTS.values():
        value = re.sub(pattern, " ", value, flags=re.I)
    result = {f"l:{x}" for x in re.findall(r"[a-z0-9][a-z0-9.+#-]{2,}", value) if x not in STOP}
    for sequence in re.findall(r"[\u3400-\u9fff]{2,}", value):
        result.update(f"h:{sequence[i:i+2]}" for i in range(len(sequence) - 1))
    return result


def similarity(a: str, b: str) -> float:
    na, nb = normalize(a), normalize(b)
    if na == nb:
        return 1.0
    ea, eb = event_kinds(a), event_kinds(b)
    if ea and eb and ea.isdisjoint(eb):
        return 0.0
    if bool(ea) != bool(eb):
        return 0.0
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    common = ta & tb
    latin = [x[2:] for x in common if x.startswith("l:")]
    han = sum(x.startswith("h:") for x in common)
    strong_latin = sum(x not in WEAK for x in latin)
    dice = 2 * len(common) / (len(ta) + len(tb))
    containment = len(common) / min(len(ta), len(tb))
    same_event = bool(ea and eb)
    if same_event and strong_latin >= 2:
        return max(dice, containment, 0.72)
    if strong_latin >= 2 and containment >= 0.22:
        return max(dice, containment)
    if strong_latin >= 1 and len(latin) >= 3 and dice >= 0.28:
        return max(dice, containment)
    if strong_latin >= 1 and han >= 2 and containment >= 0.3:
        return max(dice, containment)
    if han >= 3 and dice >= 0.3 and containment >= 0.38:
        return max(dice, containment)
    return 0.0


def canonical_url(url: str) -> str:
    parts = urlsplit(url)
    query = urlencode(sorted((k, v) for k, v in parse_qsl(parts.query) if k.casefold() not in TRACKING))
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.casefold(), parts.netloc.casefold(), path, query, ""))


def independent(a: dict, b: dict) -> bool:
    return a["platform"].casefold() != b["platform"].casefold() and canonical_url(a["url"]) != canonical_url(b["url"])


def affinity(story: dict, group: list[dict]) -> float:
    return sum(similarity(comparison_title(story), comparison_title(other)) for other in group)


def comparison_title(story: dict) -> str:
    return str(story.get("semantic_title") or story["title"])


def safe_rank(value: object) -> int:
    try:
        return int(value) if value is not None else 99
    except (TypeError, ValueError):
        return 99


def build_clusters(items: list[dict], min_platforms: int = 2) -> list[dict]:
    valid = [x | {"rank": safe_rank(x.get("rank", 99))} for x in items if x.get("platform") and x.get("title") and x.get("url")]
    groups = []
    for seed in valid:
        group = [seed]
        candidates = sorted(
            (x for x in valid if independent(seed, x) and similarity(comparison_title(seed), comparison_title(x)) > 0),
            key=lambda x: similarity(comparison_title(seed), comparison_title(x)),
            reverse=True,
        )
        seen = {seed["platform"].casefold()}
        for candidate in candidates:
            if candidate["platform"].casefold() in seen:
                continue
            if all(independent(candidate, other) and similarity(comparison_title(candidate), comparison_title(other)) > 0 for other in group):
                group.append(candidate)
                seen.add(candidate["platform"].casefold())
        if len(group) >= min_platforms:
            groups.append(group)

    output, fingerprints = [], set()
    for group in groups:
        fingerprint = tuple(sorted((x["platform"].casefold(), canonical_url(x["url"])) for x in group))
        if fingerprint in fingerprints:
            continue
        fingerprints.add(fingerprint)
        lead = max(group, key=lambda x: (affinity(x, group), -x["rank"], -len(x["title"])))
        rank_signal = sum(max(1, 20 - min(19, x["rank"])) for x in group)
        output.append({
            "title": lead["title"],
            "lead_url": lead["url"],
            "platform_count": len(group),
            "score": len(group) * 100 + rank_signal,
            "stories": sorted(group, key=lambda x: x["rank"]),
            "requires_human_verification": True,
        })
    return sorted(output, key=lambda x: x["score"], reverse=True)


def load_json(path: Path) -> list[dict]:
    # utf-8-sig accepts both ordinary UTF-8 and PowerShell's common BOM variant.
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        raise ValueError("input must be a JSON array")
    return data


def self_test() -> None:
    def item(platform: str, title: str, n: int, url: str | None = None) -> dict:
        return {"platform": platform, "title": title, "url": url or f"https://{platform}.example/{n}", "rank": n}

    same = build_clusters([
        item("ithome", "微软完成收购动视暴雪", 0),
        item("hn", "Microsoft completes acquisition of Activision Blizzard", 0),
    ])
    assert same and same[0]["platform_count"] == 2
    assert not build_clusters([item("a", "苹果公司发布新手机", 0), item("b", "苹果公司发布新电脑", 0)])
    assert not build_clusters([item("a", "小米汽车宣布涨价", 0), item("b", "小米汽车启动召回", 0)])
    assert not build_clusters([item("a", "OpenAI launches GPT-5.5 coding model", 0), item("b", "OpenAI GPT-5.5 coding model suffers security breach", 0)])
    shared = "https://origin.example/story?utm_source=feed"
    assert not build_clusters([item("a", "OpenAI 发布 GPT-5.5", 0, shared), item("b", "OpenAI launches GPT-5.5", 0, "https://origin.example/story")])
    bridge = build_clusters([
        item("a", "OpenAI 发布 GPT-5.5", 0),
        item("b", "OpenAI GPT-5.5 vs Anthropic Claude 5 benchmark", 0),
        item("c", "Anthropic 发布 Claude 5", 0),
    ])
    assert not bridge
    bilingual = [
        item("a", "字节跳动收购 Pico", 0) | {"semantic_title": "ByteDance acquires Pico"},
        item("b", "ByteDance acquires Pico", 0),
    ]
    assert build_clusters(bilingual)[0]["platform_count"] == 2
    assert build_clusters([item("a", "same story", 0, "https://x.example/a?b=2&a=1"), item("b", "same story", 0, "https://x.example/a?a=1&b=2")]) == []
    assert build_clusters([item("a", "OpenAI 发布 GPT-5.5", 0) | {"rank": None}, item("b", "OpenAI launches GPT-5.5", 0)])[0]["platform_count"] == 2
    with tempfile.TemporaryDirectory() as tmp:
        bom_file = Path(tmp) / "signals.json"
        bom_file.write_text(json.dumps([item("a", "测试标题", 0)], ensure_ascii=False), encoding="utf-8-sig")
        assert load_json(bom_file)[0]["title"] == "测试标题"
    print("cluster self-test: ok")


def main() -> None:
    parser = argparse.ArgumentParser(description="Find candidate cross-platform hotspot clusters")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--profile", default="auto", help="Reserved for the calling workflow")
    parser.add_argument("--min-platforms", type=int, default=2)
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.input:
        parser.error("--input is required unless --self-test is used")
    clusters = build_clusters(load_json(args.input), max(2, args.min_platforms))[:max(1, args.top)]
    result = {"main_candidate": clusters[0] if clusters else None, "clusters": clusters}
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
