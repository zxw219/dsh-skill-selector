#!/usr/bin/env python3
"""Search the bundled SFX catalog with English or Chinese terms."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = SKILL_ROOT / "references" / "sfx-catalog.json"

QUERY_ALIASES = {
    "冲击": ["impact", "hit"],
    "撞击": ["impact", "hit"],
    "击中": ["impact", "hit"],
    "重型": ["heavy"],
    "沉重": ["heavy", "low"],
    "轻型": ["light"],
    "轻微": ["light"],
    "中型": ["medium"],
    "低频": ["low"],
    "高频": ["high"],
    "金属": ["metal", "plate", "tin", "bell"],
    "木头": ["wood", "plank"],
    "木质": ["wood", "plank"],
    "玻璃": ["glass"],
    "软质": ["soft"],
    "拳击": ["punch"],
    "脚步": ["footstep"],
    "草地": ["grass"],
    "雪地": ["snow"],
    "地毯": ["carpet"],
    "混凝土": ["concrete"],
    "转场": ["transition", "whoosh", "swish"],
    "呼啸": ["whoosh", "swish"],
    "嗖": ["whoosh", "swish"],
    "界面": ["ui", "interface"],
    "点击": ["click", "select", "tick"],
    "确认": ["confirmation"],
    "错误": ["error"],
    "提示": ["notification", "confirmation", "question"],
    "铃声": ["bell", "bong"],
    "故障": ["glitch"],
    "科技": ["digital", "electronic", "sci-fi"],
    "数字": ["digital", "electronic"],
    "激光": ["laser"],
    "上升": ["up", "phaserup", "powerup", "riser"],
    "下降": ["down", "phaserdown", "downer"],
    "风": ["wind", "ambience"],
    "环境": ["ambience", "environment"],
    "衣物": ["cloth"],
    "布料": ["cloth"],
    "门": ["door"],
    "开门": ["door", "open"],
    "关门": ["door", "close"],
    "书": ["book"],
    "翻书": ["book", "flip"],
    "纸": ["book", "flip"],
    "刀": ["knife", "slice"],
    "皮革": ["leather"],
    "硬币": ["coins"],
}


def query_terms(query: str) -> list[str]:
    lower = query.lower()
    terms = set(re.findall(r"[a-z0-9]+", lower))
    for key, values in QUERY_ALIASES.items():
        if key in query:
            terms.update(values)
    return sorted(terms)


def score(entry: dict[str, Any], terms: list[str]) -> int:
    if not terms:
        return 1
    tags = set(entry.get("tags", []))
    name = entry["id"].lower()
    category = entry["category"].lower()
    total = 0
    matched = 0
    for term in terms:
        term_score = 0
        if term in tags:
            term_score = max(term_score, 8)
        if term in name:
            term_score = max(term_score, 5)
        if term in category:
            term_score = max(term_score, 3)
        if term_score:
            matched += 1
            total += term_score
    if matched == 0:
        return 0
    return total + matched * 2 + (6 if matched == len(terms) else 0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--category")
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--plan-snippet", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    catalog_path = args.catalog.expanduser().resolve()
    catalog = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
    terms = query_terms(args.query)
    if args.query.strip() and not terms:
        print(f"query={args.query!r} terms=<unrecognized> results=0")
        return 0
    ranked = []
    for entry in catalog["entries"]:
        if args.category and entry["category"] != args.category:
            continue
        value = score(entry, terms)
        if value:
            ranked.append((value, entry))
    ranked.sort(key=lambda item: (-item[0], item[1]["duration"], item[1]["id"]))
    selected = []
    for value, entry in ranked[: max(1, args.limit)]:
        item = dict(entry)
        item["score"] = value
        item["absolute_path"] = str((SKILL_ROOT / entry["path"]).resolve())
        selected.append(item)
    if args.plan_snippet:
        snippets = [
            {
                "path": item["absolute_path"],
                "timeline_start": 0.0,
                "source_in": 0.0,
                "duration": item["duration"],
                "gain_db": -6.0,
                "fade_in": 0.0,
                "fade_out": min(0.05, item["duration"] / 4),
                "loop": False,
                "label": item["id"],
            }
            for item in selected
        ]
        print(json.dumps(snippets, ensure_ascii=False, indent=2))
    elif args.json:
        print(json.dumps(selected, ensure_ascii=False, indent=2))
    else:
        print(f"query={args.query!r} terms={','.join(terms) or '*'} results={len(selected)}")
        for item in selected:
            print(
                f"[{item['score']:02d}] {item['id']} | {item['duration']:.3f}s | "
                f"{item['sample_rate']} Hz | {item['channels']} ch\n  {item['absolute_path']}"
            )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
