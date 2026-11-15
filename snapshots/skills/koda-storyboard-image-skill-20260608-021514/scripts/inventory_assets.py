#!/usr/bin/env python3
"""Create a compact asset inventory for shot-by-shot storyboard prompting."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
from pathlib import Path
from typing import Any


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tif", ".tiff", ".heic", ".avif"}
VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".webm"}
AUDIO_EXTS = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}
TEXT_EXTS = {
    ".txt",
    ".md",
    ".csv",
    ".tsv",
    ".json",
    ".yaml",
    ".yml",
    ".srt",
    ".vtt",
    ".ass",
    ".html",
    ".htm",
    ".xml",
    ".rtf",
}
DOC_EXTS = {".pdf", ".docx", ".pptx", ".xlsx", ".xls", ".pages", ".key"}
DEFAULT_IGNORES = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
}


def sha1_head(path: Path, max_bytes: int = 1024 * 1024) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        h.update(f.read(max_bytes))
    return h.hexdigest()[:12]


def image_dimensions(path: Path) -> dict[str, int] | None:
    try:
        from PIL import Image  # type: ignore

        with Image.open(path) as img:
            return {"width": int(img.width), "height": int(img.height)}
    except Exception:
        return None


def category_for(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in IMAGE_EXTS:
        return "image"
    if ext in VIDEO_EXTS:
        return "video"
    if ext in AUDIO_EXTS:
        return "audio"
    if ext in TEXT_EXTS:
        return "text"
    if ext in DOC_EXTS:
        return "document"
    return "other"


def text_sample(path: Path, limit: int) -> str | None:
    if path.suffix.lower() not in TEXT_EXTS:
        return None
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
    cleaned = " ".join(text.split())
    if not cleaned:
        return None
    return cleaned[:limit]


def should_ignore(path: Path, root: Path, extra_ignores: set[str]) -> bool:
    rel_parts = path.relative_to(root).parts
    ignores = DEFAULT_IGNORES | extra_ignores
    return any(part in ignores for part in rel_parts)


def scan_assets(root: Path, sample_chars: int, extra_ignores: set[str]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if path.is_dir() or should_ignore(path, root, extra_ignores):
            continue
        try:
            stat = path.stat()
        except OSError:
            continue

        rel = path.relative_to(root).as_posix()
        category = category_for(path)
        item: dict[str, Any] = {
            "path": rel,
            "name": path.name,
            "category": category,
            "extension": path.suffix.lower(),
            "size_bytes": stat.st_size,
            "mime": mimetypes.guess_type(path.name)[0],
            "sha1_head": sha1_head(path),
        }
        if category == "image":
            dims = image_dimensions(path)
            if dims:
                item.update(dims)
        sample = text_sample(path, sample_chars)
        if sample:
            item["text_sample"] = sample
        items.append(item)
    return items


def write_markdown(items: list[dict[str, Any]], root: Path) -> str:
    lines = [
        f"# Asset Inventory",
        "",
        f"Root: `{root}`",
        f"Total files: {len(items)}",
        "",
    ]
    by_category: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        by_category.setdefault(item["category"], []).append(item)

    for category in ["image", "video", "audio", "document", "text", "other"]:
        group = by_category.get(category, [])
        if not group:
            continue
        lines.extend([f"## {category.title()} Assets", ""])
        for item in group:
            bits = [f"`{item['path']}`", f"{item['size_bytes']} bytes"]
            if "width" in item and "height" in item:
                bits.append(f"{item['width']}x{item['height']}")
            if item.get("mime"):
                bits.append(str(item["mime"]))
            bits.append(f"sha1:{item['sha1_head']}")
            lines.append(f"- {' | '.join(bits)}")
            if item.get("text_sample"):
                lines.append(f"  - sample: {item['text_sample']}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Inventory assets for storyboard prompting.")
    parser.add_argument("root", type=Path, help="Directory to scan.")
    parser.add_argument("--json-out", type=Path, help="Optional JSON output path.")
    parser.add_argument("--md-out", type=Path, help="Optional Markdown output path.")
    parser.add_argument("--sample-chars", type=int, default=500, help="Text sample length per text file.")
    parser.add_argument("--ignore", action="append", default=[], help="Directory name to ignore. Can repeat.")
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    items = scan_assets(root, args.sample_chars, set(args.ignore))
    payload = {"root": str(root), "total_files": len(items), "assets": items}

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    markdown = write_markdown(items, root)
    if args.md_out:
        args.md_out.parent.mkdir(parents=True, exist_ok=True)
        args.md_out.write_text(markdown, encoding="utf-8")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
