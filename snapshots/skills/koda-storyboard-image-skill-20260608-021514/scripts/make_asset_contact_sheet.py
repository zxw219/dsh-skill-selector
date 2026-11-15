#!/usr/bin/env python3
"""Build a labeled image contact sheet for asset-grounded storyboard work."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
DEFAULT_IGNORES = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"}


def scene_asset_paths(manifest_path: Path, scene_id: str) -> set[str]:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    wanted = scene_id.lower()
    paths: set[str] = set()
    for scene in data.get("scenes", []):
        if str(scene.get("scene_id", "")).lower() != wanted:
            continue
        for key in ["asset_candidates", "global_asset_candidates"]:
            for rel in scene.get(key, []):
                paths.add(str(rel).replace("\\", "/"))
    return paths


def collect_images(root: Path, includes: list[str], max_images: int, explicit_paths: set[str] | None = None) -> list[Path]:
    terms = [term.lower() for term in includes if term.strip()]
    images: list[Path] = []
    for path in sorted(root.rglob("*")):
        if path.is_dir() or path.suffix.lower() not in IMAGE_EXTS:
            continue
        rel_parts = path.relative_to(root).parts
        if any(part in DEFAULT_IGNORES for part in rel_parts):
            continue
        rel = path.relative_to(root).as_posix()
        if explicit_paths is not None and rel not in explicit_paths:
            continue
        haystack = path.as_posix().lower()
        if terms and not any(term in haystack for term in terms):
            continue
        images.append(path)
        if len(images) >= max_images:
            break
    return images


def fit_text(text: str, max_chars: int) -> str:
    return text if len(text) <= max_chars else text[: max_chars - 3] + "..."


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a labeled contact sheet from project images.")
    parser.add_argument("root", type=Path, help="Asset root to scan.")
    parser.add_argument("--out", type=Path, required=True, help="Output JPG/PNG path.")
    parser.add_argument("--include", action="append", default=[], help="Only include paths containing this text. Can repeat.")
    parser.add_argument("--manifest", type=Path, help="scene_manifest.json from prepare_project_batch.py.")
    parser.add_argument("--scene", help="Scene id to filter images from --manifest, such as SC01.")
    parser.add_argument("--max-images", type=int, default=48)
    parser.add_argument("--thumb-w", type=int, default=320)
    parser.add_argument("--thumb-h", type=int, default=220)
    parser.add_argument("--cols", type=int, default=4)
    args = parser.parse_args()

    try:
        from PIL import Image, ImageDraw, ImageFont  # type: ignore
    except Exception as exc:
        raise SystemExit(f"Pillow is required to make contact sheets: {exc}")

    root = args.root.expanduser().resolve()
    explicit_paths = None
    if args.scene and not args.manifest:
        raise SystemExit("--scene requires --manifest.")
    if args.manifest:
        if not args.scene:
            raise SystemExit("--manifest requires --scene.")
        explicit_paths = scene_asset_paths(args.manifest.expanduser().resolve(), args.scene)
    images = collect_images(root, args.include, args.max_images, explicit_paths=explicit_paths)
    if not images:
        raise SystemExit("No matching images found.")

    cols = max(1, args.cols)
    rows = math.ceil(len(images) / cols)
    label_h = 52
    pad = 16
    sheet_w = cols * args.thumb_w + (cols + 1) * pad
    sheet_h = rows * (args.thumb_h + label_h) + (rows + 1) * pad
    sheet = Image.new("RGB", (sheet_w, sheet_h), (246, 242, 232))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except Exception:
        font = ImageFont.load_default()

    for index, path in enumerate(images):
        col = index % cols
        row = index // cols
        x = pad + col * (args.thumb_w + pad)
        y = pad + row * (args.thumb_h + label_h + pad)
        with Image.open(path) as img:
            img = img.convert("RGB")
            img.thumbnail((args.thumb_w, args.thumb_h))
            bg = Image.new("RGB", (args.thumb_w, args.thumb_h), (230, 226, 216))
            ox = (args.thumb_w - img.width) // 2
            oy = (args.thumb_h - img.height) // 2
            bg.paste(img, (ox, oy))
        sheet.paste(bg, (x, y))
        draw.rectangle((x, y, x + args.thumb_w, y + args.thumb_h), outline=(40, 40, 40), width=2)
        rel = path.relative_to(root).as_posix()
        draw.text((x, y + args.thumb_h + 8), f"{index + 1:02d}. {fit_text(rel, 42)}", fill=(20, 20, 20), font=font)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.suffix.lower() in {".jpg", ".jpeg"}:
        sheet.save(args.out, quality=92)
    else:
        sheet.save(args.out)
    print(args.out)


if __name__ == "__main__":
    main()
