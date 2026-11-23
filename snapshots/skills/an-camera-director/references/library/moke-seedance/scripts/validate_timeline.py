#!/usr/bin/env python3
"""Validate top-level timestamp ranges in a compiled Seedance prompt."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


RANGE_RE = re.compile(
    r"(?P<start>\d+(?:\.\d+)?)\s*(?:s|秒)?\s*(?:–|—|-|~|～|至)\s*"
    r"(?P<end>\d+(?:\.\d+)?)\s*(?:s|秒)",
    re.IGNORECASE,
)
DURATION_RE = re.compile(
    r"(?:总时长|目标时长|时长)\s*[:：=]?\s*"
    r"(?P<duration>\d+(?:\.\d+)?)\s*(?:s|秒)",
    re.IGNORECASE,
)
SHOT_PREFIX_RE = re.compile(
    r"^(?:镜头|shot)\s*(?:"
    r"(?:#?\d+|[A-Za-z]|[一二三四五六七八九十百]+)\s*(?:[｜|:：、.\-–—(（【\[]\s*)?"
    r"|[｜|:：(（【\[]\s*"
    r"|(?=\d)"
    r")",
    re.IGNORECASE,
)


def normalize_line(line: str) -> str:
    """Remove Markdown/list decoration without changing semantic text."""
    clean = line.strip()
    clean = re.sub(r"^(?:>\s*)+", "", clean)
    clean = re.sub(r"^#{1,6}\s*", "", clean)
    clean = re.sub(r"^(?:[-+*]\s+|\d+[.)、]\s*)", "", clean)
    return clean.lstrip("*_` 【[（(")


def extract_ranges(text: str) -> list[tuple[float, float]]:
    """Prefer explicit shot headers; otherwise accept decorated leading ranges."""
    shot_ranges: list[tuple[float, float]] = []
    leading_ranges: list[tuple[float, float]] = []

    for line in text.splitlines():
        clean = normalize_line(line)
        shot_prefix = SHOT_PREFIX_RE.match(clean)
        if shot_prefix:
            match = RANGE_RE.search(clean, shot_prefix.end())
            if match:
                shot_ranges.append((float(match.group("start")), float(match.group("end"))))
            continue
        match = RANGE_RE.match(clean)
        if match:
            leading_ranges.append((float(match.group("start")), float(match.group("end"))))
    return shot_ranges or leading_ranges


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check that prompt time ranges start at 0, are contiguous, and end at the target duration."
    )
    parser.add_argument("path", type=Path, help="UTF-8 prompt text or Markdown file")
    parser.add_argument("--duration", type=float, help="Expected duration in seconds")
    parser.add_argument("--tolerance", type=float, default=1e-6)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    text = args.path.read_text(encoding="utf-8")
    ranges = extract_ranges(text)
    if not ranges:
        print("FAIL: no timestamp ranges found", file=sys.stderr)
        return 1

    errors: list[str] = []
    tolerance = args.tolerance
    if tolerance < 0:
        print("FAIL: tolerance must be non-negative", file=sys.stderr)
        return 2
    if abs(ranges[0][0]) > tolerance:
        errors.append(f"first range starts at {ranges[0][0]:g}s instead of 0s")

    for index, (start, end) in enumerate(ranges, start=1):
        if end <= start:
            errors.append(f"range {index} is not positive: {start:g}s–{end:g}s")
        if index > 1:
            previous_end = ranges[index - 2][1]
            if abs(start - previous_end) > tolerance:
                relation = "gap" if start > previous_end else "overlap"
                errors.append(
                    f"{relation} before range {index}: previous ends at {previous_end:g}s, "
                    f"next starts at {start:g}s"
                )

    expected = args.duration
    if expected is None:
        match = DURATION_RE.search(text)
        if match:
            expected = float(match.group("duration"))
    if expected is None:
        errors.append(
            "target duration is missing; declare 总时长/目标时长/时长 or pass --duration"
        )
    elif abs(ranges[-1][1] - expected) > tolerance:
        errors.append(f"last range ends at {ranges[-1][1]:g}s instead of target {expected:g}s")

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(
        f"PASS: {len(ranges)} contiguous ranges, ending at {ranges[-1][1]:g}s, "
        f"target {expected:g}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
