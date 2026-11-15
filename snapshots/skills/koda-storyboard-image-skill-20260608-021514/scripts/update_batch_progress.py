#!/usr/bin/env python3
"""Update a Koda batch progress ledger after one sheet dispatch."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


VALID_STATUSES = {"pending", "running", "done", "failed"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def overall_status(entries: list[dict[str, Any]]) -> str:
    statuses = [entry.get("status") for entry in entries]
    if statuses and all(status == "done" for status in statuses):
        return "done"
    if any(status == "running" for status in statuses):
        return "running"
    if any(status == "failed" for status in statuses):
        return "failed"
    return "ready"


def next_sheet(entries: list[dict[str, Any]]) -> dict[str, Any] | None:
    for status in ("pending", "failed"):
        for entry in entries:
            if entry.get("status") == status:
                return entry
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Update batch_progress.json for one Koda storyboard sheet.")
    parser.add_argument("batch_dir", type=Path, help="Batch directory containing batch_progress.json.")
    parser.add_argument("--sheet-id", required=True, help="Sheet id to update, for example SC01_sheet_02.")
    parser.add_argument("--status", required=True, choices=sorted(VALID_STATUSES), help="New sheet status.")
    parser.add_argument("--output-path", help="Returned/generated output path for done or running status.")
    parser.add_argument("--error", help="Failure note for failed status.")
    parser.add_argument("--print-next", action="store_true", help="Print the next pending/failed sheet after update.")
    args = parser.parse_args()

    progress_path = args.batch_dir.expanduser().resolve() / "batch_progress.json"
    if not progress_path.exists():
        raise SystemExit(f"Missing batch_progress.json: {progress_path}")

    progress = load_json(progress_path)
    entries = progress.get("entries", [])
    if not isinstance(entries, list):
        raise SystemExit("batch_progress.json entries must be a list")

    target = None
    for entry in entries:
        if entry.get("sheet_id") == args.sheet_id:
            target = entry
            break
    if target is None:
        raise SystemExit(f"Unknown sheet_id: {args.sheet_id}")

    target["status"] = args.status
    if args.output_path is not None:
        target["output_path"] = args.output_path
    if args.status == "failed":
        target["error"] = args.error or "generation failed"
    elif args.error is not None:
        target["error"] = args.error
    else:
        target["error"] = None

    progress["status"] = overall_status(entries)
    write_json(progress_path, progress)

    if args.print_next:
        next_entry = next_sheet(entries)
        if next_entry:
            print(json.dumps(next_entry, ensure_ascii=False))
        else:
            print("NO_NEXT_SHEET")
    else:
        print(f"updated {args.sheet_id} -> {args.status}")


if __name__ == "__main__":
    main()
