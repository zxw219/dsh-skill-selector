#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3:4 肖像提示词自检器（确定性输出评测）。

七条规则：
  R1 禁用裁切锁死语义
  R2 「锁定」只允许用于比例
  R3 必须出现 3:4 比例
  R4 必须出现 #808080 / 中性灰 背景
  R5 身份四定值（骨相／五官／识别／气质）至少出现 3 项
  R6 光的正向句必须含 漫射／柔光／平光／铺照 之一
  R7 负向块只允许一行且条目不超过 8 个

用法：
  python lint_prompt.py --text "<提示词>"
  python lint_prompt.py --file prompt.txt
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BANNED_CROP_LOCK = [
    "裁切", "裁掉", "裁到", "出画", "不入画", "不入镜",
    "止于", "锁死", "锁定边界", "锁定构图", "不得被", "不得超",
    "画面下缘", "画面边缘", "边缘切断",
]
LOCK_ALLOWED_HINTS = ("比例", "3:4", "3：4")
FIXED_FIELDS = ["骨相", "五官", "识别", "气质"]
LIGHT_HINTS = ["漫射", "柔光", "平光", "铺照"]
BACKGROUND_HINTS = ["#808080", "中性灰"]
NEGATIVE_LINE_LIMIT = 1
NEGATIVE_ITEM_LIMIT = 8


def check(text: str) -> dict:
    violations: list[dict] = []

    for bad in BANNED_CROP_LOCK:
        if bad in text:
            violations.append({"rule": "R1", "detail": f"出现禁用裁切锁死语义：{bad}"})

    for m in re.finditer("锁定", text):
        tail = text[m.start(): m.start() + 10]
        if not any(h in tail for h in LOCK_ALLOWED_HINTS):
            violations.append({"rule": "R2", "detail": f"「锁定」未指向比例：{tail}"})

    if "3:4" not in text and "3：4" not in text:
        violations.append({"rule": "R3", "detail": "缺少 3:4 比例声明"})

    if not any(h in text for h in BACKGROUND_HINTS):
        violations.append({"rule": "R4", "detail": "缺少 #808080 / 中性灰 背景声明"})

    hit = [f for f in FIXED_FIELDS if f in text]
    if len(hit) < 3:
        violations.append({"rule": "R5", "detail": f"身份四定值仅出现 {len(hit)} 项：{hit}"})

    if not any(h in text for h in LIGHT_HINTS):
        violations.append({"rule": "R6", "detail": "缺少漫射柔光／平光铺照的光线正向句"})

    if "负向" in text:
        tail = text.split("负向", 1)[1]
        lines = [ln.strip() for ln in tail.splitlines() if ln.strip()]
        if len(lines) > NEGATIVE_LINE_LIMIT:
            violations.append({"rule": "R7", "detail": f"负向块占了 {len(lines)} 行，只允许 1 行"})
        if lines:
            items = [x for x in re.split(r"[、;；,，]", lines[0]) if x.strip()]
            if len(items) > NEGATIVE_ITEM_LIMIT:
                violations.append({"rule": "R7", "detail": f"负向条目 {len(items)} 个，超过 {NEGATIVE_ITEM_LIMIT}"})

    return {"ok": not violations, "rule_count": 7, "violations": violations}


def run_cases(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    results = []
    for case in payload.get("cases", []):
        outcome = check(str(case.get("text", "")))
        expected_ok = bool(case.get("expected_ok"))
        got_rules = sorted({v["rule"] for v in outcome["violations"]})
        expect_rules = sorted(set(case.get("expect_rules", [])))
        passed = (outcome["ok"] == expected_ok) and set(expect_rules) <= set(got_rules)
        results.append({
            "name": case.get("name"),
            "passed": passed,
            "expected_ok": expected_ok,
            "actual_ok": outcome["ok"],
            "expect_rules": expect_rules,
            "got_rules": got_rules,
        })
    total = len(results)
    passed_n = sum(1 for r in results if r["passed"])
    return {
        "ok": total > 0 and passed_n == total,
        "summary": {"total": total, "passed": passed_n, "failed": total - passed_n},
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="3:4 肖像提示词自检器（确定性输出评测）。")
    parser.add_argument("--text", help="直接传入提示词文本")
    parser.add_argument("--file", help="从文件读取提示词")
    parser.add_argument("--cases", help="运行输出评测用例 JSON")
    args = parser.parse_args()

    if args.cases:
        result = run_cases(Path(args.cases))
    else:
        if args.text:
            text = args.text
        elif args.file:
            text = Path(args.file).read_text(encoding="utf-8")
        else:
            parser.error("需要 --text / --file / --cases 之一")
        result = check(text)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
