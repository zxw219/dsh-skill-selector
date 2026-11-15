#!/usr/bin/env python3
"""Validate and optionally mark a Koda project batch scaffold as ready."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


BLOCKER_PATTERNS = [
    ("TODO marker", re.compile(r"\[(?:TODO|fill)(?::|\])", re.IGNORECASE)),
    ("packet_status: scaffold", re.compile(r"^\s*packet_status:\s*scaffold\s*$", re.MULTILINE)),
    ("continuity_status: scaffold", re.compile(r"^\s*continuity_status:\s*scaffold\s*$", re.MULTILINE)),
]
PLACEHOLDER_PROMPT_PATTERNS = [
    re.compile(r"fill from scene packet before image generation", re.IGNORECASE),
    re.compile(r"\[(?:TODO|fill)(?::|\])", re.IGNORECASE),
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def has_blocker(text: str) -> list[str]:
    return [name for name, pattern in BLOCKER_PATTERNS if pattern.search(text)]


def clip(text: str, limit: int) -> str:
    cleaned = "\n".join(line.rstrip() for line in text.strip().splitlines() if line.strip())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def section_text(markdown: str, heading: str, limit: int) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(markdown)
    if not match:
        return ""
    next_heading = re.search(r"^##\s+", markdown[match.end() :], re.MULTILINE)
    end = match.end() + next_heading.start() if next_heading else len(markdown)
    return clip(markdown[match.end() : end], limit)


def sheet_plan_text(packet_text: str, sheet_id: str, limit: int = 900) -> str:
    plan = section_text(packet_text, "15-Second Sheet Plan", limit * 2)
    if not plan:
        return ""
    match = re.search(r"sheet[_\-\s]*(\d+)", sheet_id, re.IGNORECASE)
    if not match:
        return clip(plan, limit)
    sheet_number = int(match.group(1))
    labels = {f"sheet {sheet_number}", f"sheet {sheet_number:02d}"}
    lines = [line for line in plan.splitlines() if any(label in line.lower() for label in labels)]
    return clip("\n".join(lines) if lines else plan, limit)


def prompt_row_errors(row: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    sheet_id = row.get("sheet_id") or "<missing sheet_id>"
    if not row.get("shot_range"):
        errors.append(f"{sheet_id} missing shot_range")
    if not row.get("output_name"):
        errors.append(f"{sheet_id} missing output_name")
    prompt_notes = str(row.get("prompt_notes") or "").strip()
    if not prompt_notes:
        errors.append(f"{sheet_id} missing prompt_notes")
    elif any(pattern.search(prompt_notes) for pattern in PLACEHOLDER_PROMPT_PATTERNS):
        errors.append(f"{sheet_id} prompt_notes still placeholder")
    asset_refs = row.get("asset_refs", [])
    if not isinstance(asset_refs, list) or not asset_refs:
        errors.append(f"{sheet_id} missing asset_refs")
    return errors


def write_dispatch_prompts(batch_dir: Path, prompt_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    dispatch_dir = batch_dir / "dispatch_prompts"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    bible_text = (batch_dir / "continuity_bible.md").read_text(encoding="utf-8")
    bible_excerpt = clip(bible_text, 1800)

    updated_rows = []
    for row in prompt_rows:
        scene_id = str(row.get("scene_id"))
        sheet_id = str(row.get("sheet_id"))
        packet_path = batch_dir / "scene_packets" / f"{scene_id}.md"
        packet_text = packet_path.read_text(encoding="utf-8")
        assets = row.get("asset_refs", [])
        asset_lines = "\n".join(f"- {asset}" for asset in assets[:12])

        prompt = f"""Create one 16:9 Koda-style annotated rough-sketch Storyboard Previs Control Sheet.
Generate exactly one sheet: {sheet_id}. Do not generate other sheets.
This is a video-control storyboard, not polished key art, not a cinematic still, not separate shot cards.

Sheet:
- Scene: {scene_id}
- Shot range: {row.get("shot_range", "")}
- Output target: {row.get("output_name", "")}

Reference assets:
{asset_lines}

Story beats for this sheet:
{sheet_plan_text(packet_text, sheet_id) or row.get("prompt_notes", "")}

Prompt notes:
{row.get("prompt_notes", "")}

Scene action:
{section_text(packet_text, "Story Action", 1200)}

First / final state:
{section_text(packet_text, "First / Final State", 900)}

Continuity locks:
{section_text(packet_text, "Continuity Locks", 1200)}

Global continuity:
{bible_excerpt}

Layout rules:
- Top masthead with title, sheet id, lens/camera note, continuity note.
- Middle grid with 4-7 sequential rough thumbnail panels.
- Bottom director strip aligned to panel columns.
- Add in-panel blocking arrows, camera arrows, axis line, prop contact marks, entry/exit marks, and short Simplified Chinese production labels.
- No dialogue subtitles. No new characters, props, locations, or plot events.
- Low-detail monochrome rough sketch on an off-white production board.
"""
        prompt_path = dispatch_dir / f"{sheet_id}.txt"
        prompt_path.write_text(prompt.strip() + "\n", encoding="utf-8")
        row = dict(row)
        row["dispatch_prompt"] = prompt_path.relative_to(batch_dir).as_posix()
        updated_rows.append(row)
    return updated_rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a Koda project batch scaffold.")
    parser.add_argument("batch_dir", type=Path, help="Directory containing scene_manifest.json and related files.")
    parser.add_argument("--mark-ready", action="store_true", help="Set manifest/progress/prompt statuses to ready if validation passes.")
    parser.add_argument("--write-dispatch-prompts", action="store_true", help="Write compact per-sheet prompts for immediate image_gen dispatch.")
    args = parser.parse_args()

    batch_dir = args.batch_dir.expanduser().resolve()
    manifest_path = batch_dir / "scene_manifest.json"
    bible_path = batch_dir / "continuity_bible.md"
    prompt_path = batch_dir / "prompt_plan.jsonl"
    progress_path = batch_dir / "batch_progress.json"
    packet_dir = batch_dir / "scene_packets"

    errors: list[str] = []
    for path in [manifest_path, bible_path, prompt_path, progress_path]:
        if not path.exists():
            errors.append(f"Missing {path.name}")
    if not packet_dir.exists():
        errors.append("Missing scene_packets/")
    if errors:
        raise SystemExit("\n".join(errors))

    manifest = load_json(manifest_path)
    progress = load_json(progress_path)
    prompt_rows = read_jsonl(prompt_path)
    scenes = manifest.get("scenes", [])
    if not scenes:
        errors.append("scene_manifest.json has no scenes")

    bible_text = bible_path.read_text(encoding="utf-8")
    blockers = has_blocker(bible_text)
    if blockers:
        errors.append(f"continuity_bible.md is not ready: {', '.join(blockers)}")

    prompt_ids = {row.get("sheet_id") for row in prompt_rows}
    progress_ids = {entry.get("sheet_id") for entry in progress.get("entries", [])}
    if prompt_ids != progress_ids:
        errors.append("prompt_plan.jsonl and batch_progress.json sheet ids differ")
    for row in prompt_rows:
        errors.extend(prompt_row_errors(row))

    for scene in scenes:
        scene_id = scene.get("scene_id")
        packet_path = packet_dir / f"{scene_id}.md"
        if not packet_path.exists():
            errors.append(f"Missing packet for {scene_id}")
            continue
        packet_text = packet_path.read_text(encoding="utf-8")
        blockers = has_blocker(packet_text)
        if blockers:
            errors.append(f"{packet_path.name} is not ready: {', '.join(blockers)}")
        if not scene.get("expected_sheet_count"):
            errors.append(f"{scene_id} missing expected_sheet_count")

    if errors:
        raise SystemExit("Batch is not ready:\n" + "\n".join(f"- {error}" for error in errors))

    prompt_rows_changed = False
    if args.write_dispatch_prompts:
        prompt_rows = write_dispatch_prompts(batch_dir, prompt_rows)
        prompt_rows_changed = True

    if args.mark_ready:
        manifest["status"] = "ready"
        for scene in manifest.get("scenes", []):
            scene["status"] = "ready"
            scene["packet_status"] = "ready"
        write_json(manifest_path, manifest)

        progress["status"] = "ready"
        for item in progress.get("scene_status", []):
            item["status"] = "ready"
        write_json(progress_path, progress)

        ready_rows = []
        for row in prompt_rows:
            row["status"] = "ready"
            ready_rows.append(json.dumps(row, ensure_ascii=False))
        prompt_path.write_text("\n".join(ready_rows) + "\n", encoding="utf-8")
    elif prompt_rows_changed:
        prompt_path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in prompt_rows) + "\n", encoding="utf-8")

    if args.write_dispatch_prompts:
        print(f"Dispatch prompts written to {batch_dir / 'dispatch_prompts'}")
    print("Batch is ready." if args.mark_ready else "Batch validates as ready.")


if __name__ == "__main__":
    main()
