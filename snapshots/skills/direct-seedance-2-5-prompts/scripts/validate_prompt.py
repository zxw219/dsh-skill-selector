#!/usr/bin/env python3
"""Validate structure, timeline continuity, length, and token contracts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HEADINGS = (
    "【片段总述】",
    "【素材绑定】",
    "【全局画面与声音】",
    "【时间轴镜头】",
    "【全局补充】",
)

TIME_RANGE = re.compile(
    r"(?m)^\s*(\d+(?:\.\d+)?)\s*[–—~-]\s*(\d+(?:\.\d+)?)\s*(?:秒|s)\b",
    re.IGNORECASE,
)


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def read_profile(path: str | None) -> dict:
    if not path:
        return {}
    value = json.loads(read_text(path))
    if not isinstance(value, dict):
        raise ValueError("Profile must be a JSON object.")
    return value


def profile_tokens(profile: dict, key: str) -> list[str]:
    value = profile.get(key, [])
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"Profile field '{key}' must be an array of strings.")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Seedance 2.5 formal prompt.")
    parser.add_argument("prompt", help="UTF-8 prompt file")
    parser.add_argument("--profile", help="UTF-8 JSON file with entry constraints")
    parser.add_argument("--duration", type=float, help="Expected total duration in seconds")
    parser.add_argument("--max-chars", type=int, help="Character limit of the current platform entry")
    parser.add_argument(
        "--require-token",
        action="append",
        default=[],
        help="Token or asset marker that must appear; repeat as needed",
    )
    parser.add_argument(
        "--forbid-token",
        action="append",
        default=[],
        help="Token that must not appear; repeat as needed",
    )
    args = parser.parse_args()

    try:
        text = read_text(args.prompt)
        profile = read_profile(args.profile)
        required_tokens = profile_tokens(profile, "required_tokens") + args.require_token
        forbidden_tokens = profile_tokens(profile, "forbidden_tokens") + args.forbid_token
        expected_duration = args.duration if args.duration is not None else profile.get("duration")
        max_characters = args.max_chars if args.max_chars is not None else profile.get("max_chars")
        if expected_duration is not None and not isinstance(expected_duration, (int, float)):
            raise ValueError("Profile field 'duration' must be a number.")
        if max_characters is not None and not isinstance(max_characters, int):
            raise ValueError("Profile field 'max_chars' must be an integer.")
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        return 2

    errors: list[str] = []
    warnings: list[str] = []

    positions = []
    for heading in HEADINGS:
        index = text.find(heading)
        positions.append(index)
        if index < 0:
            errors.append(f"Missing heading: {heading}")
        elif text.count(heading) > 1:
            errors.append(f"Heading appears more than once: {heading}")
    if all(index >= 0 for index in positions) and positions != sorted(positions):
        errors.append("Required headings are not in the expected order.")

    if all(index >= 0 for index in positions) and positions == sorted(positions):
        for index, heading in enumerate(HEADINGS):
            start = positions[index] + len(heading)
            end = positions[index + 1] if index + 1 < len(positions) else len(text)
            if not text[start:end].strip():
                errors.append(f"Section is empty: {heading}")

    if re.search(r"(?i)\bTODO\b|待填写|请补充|占位符", text):
        errors.append("Prompt contains unfinished placeholder text.")

    for token in required_tokens:
        if token not in text:
            errors.append(f"Required token not found: {token}")

    for token in forbidden_tokens:
        if token in text:
            errors.append(f"Forbidden token found: {token}")

    timeline_start = text.find("【时间轴镜头】")
    timeline_end = text.find("【全局补充】")
    timeline_text = (
        text[timeline_start + len("【时间轴镜头】") : timeline_end]
        if 0 <= timeline_start < timeline_end
        else text
    )
    ranges = [(float(start), float(end)) for start, end in TIME_RANGE.findall(timeline_text)]
    if not ranges:
        errors.append("No timeline ranges were found. Use lines such as '0–3秒【阶段】…'.")
    else:
        tolerance = 1e-6
        if abs(ranges[0][0]) > tolerance:
            errors.append(f"Timeline starts at {ranges[0][0]:g}s instead of 0s.")
        previous_end = ranges[0][0]
        for index, (start, end) in enumerate(ranges, start=1):
            if end <= start:
                errors.append(f"Timeline range {index} has a non-positive duration: {start:g}–{end:g}s.")
            if abs(start - previous_end) > tolerance:
                relation = "gap" if start > previous_end else "overlap"
                errors.append(
                    f"Timeline {relation} before range {index}: previous end {previous_end:g}s, next start {start:g}s."
                )
            previous_end = end

        inferred_duration = ranges[-1][1]
        if expected_duration is not None and abs(inferred_duration - expected_duration) > tolerance:
            errors.append(
                f"Timeline ends at {inferred_duration:g}s but expected duration is {expected_duration:g}s."
            )
        if expected_duration is None and not inferred_duration.is_integer():
            warnings.append(
                f"Total duration inferred from the timeline is {inferred_duration:g}s; confirm whether the entry accepts it."
            )

    char_count = len(text)
    if max_characters is not None and char_count > max_characters:
        errors.append(f"Prompt has {char_count} characters, exceeding the limit by {char_count - max_characters}.")
    elif max_characters is not None:
        remaining = max_characters - char_count
        if remaining < max(50, round(max_characters * 0.05)):
            warnings.append(f"Only {remaining} characters remain below the configured limit.")

    result = {
        "valid": not errors,
        "characters": char_count,
        "max_characters": max_characters,
        "timeline_ranges": len(ranges),
        "timeline_end_seconds": ranges[-1][1] if ranges else None,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
