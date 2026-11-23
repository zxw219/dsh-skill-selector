#!/usr/bin/env python3
"""Crop a raster image to an exact 2.35:1 frame without stretching."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


BASE_WIDTH = 47
BASE_HEIGHT = 20
RATIO = BASE_WIDTH / BASE_HEIGHT


def clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def crop_box(width: int, height: int, anchor_x: float, anchor_y: float) -> tuple[int, int, int, int]:
    if width * BASE_HEIGHT == height * BASE_WIDTH:
        return 0, 0, width, height

    scale = min(width // BASE_WIDTH, height // BASE_HEIGHT)
    if scale < 1:
        raise ValueError("Input is too small for an exact 47:20 crop")
    crop_width = BASE_WIDTH * scale
    crop_height = BASE_HEIGHT * scale
    left = int(round((width - crop_width) * clamp(anchor_x)))
    top = int(round((height - crop_height) * clamp(anchor_y)))
    left = max(0, min(left, width - crop_width))
    top = max(0, min(top, height - crop_height))
    return left, top, left + crop_width, top + crop_height


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--anchor-x", type=float, default=0.5, help="Horizontal crop anchor from 0 (left) to 1 (right)")
    parser.add_argument("--anchor-y", type=float, default=0.5, help="Vertical crop anchor from 0 (top) to 1 (bottom)")
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(f"Input not found: {args.input}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(args.input) as image:
        image.load()
        box = crop_box(image.width, image.height, args.anchor_x, args.anchor_y)
        cropped = image.crop(box)
        save_kwargs = {}
        if args.output.suffix.lower() in {".jpg", ".jpeg"}:
            if cropped.mode not in {"RGB", "L"}:
                cropped = cropped.convert("RGB")
            save_kwargs = {"quality": 95, "subsampling": 0}
        cropped.save(args.output, **save_kwargs)
        print(f"Saved {cropped.width}x{cropped.height} ({cropped.width / cropped.height:.6f}:1) to {args.output}")


if __name__ == "__main__":
    main()
