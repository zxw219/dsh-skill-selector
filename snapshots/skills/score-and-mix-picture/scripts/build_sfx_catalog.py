#!/usr/bin/env python3
"""Build a searchable metadata catalog for the bundled sound-effect library."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ASSET_ROOT = SKILL_ROOT / "assets" / "sfx"
DEFAULT_OUTPUT = SKILL_ROOT / "references" / "sfx-catalog.json"
DEFAULT_SOURCES = SKILL_ROOT / "references" / "sfx-sources.json"
AUDIO_EXTENSIONS = {".wav", ".ogg", ".flac", ".mp3", ".m4a", ".aac"}

CATEGORY_TAGS = {
    "impacts": ["impact", "hit", "contact", "transient"],
    "foley": ["foley", "sync", "prop", "movement"],
    "ui": ["ui", "interface", "feedback"],
    "digital": ["digital", "electronic", "sci-fi", "technology"],
    "whoosh": ["whoosh", "swish", "transition", "movement", "passby"],
    "ambience": ["ambience", "environment", "bed", "atmosphere"],
}


def executable(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"Required executable not found on PATH: {name}")
    return path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def split_tokens(name: str) -> list[str]:
    without_source = name.split("__", 1)[-1]
    expanded = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", without_source)
    return [token.lower() for token in re.split(r"[^A-Za-z0-9]+", expanded) if token]


def probe(path: Path) -> dict[str, Any]:
    command = [
        executable("ffprobe"),
        "-v",
        "error",
        "-select_streams",
        "a:0",
        "-show_entries",
        "stream=codec_name,sample_rate,channels,channel_layout,duration:format=duration",
        "-of",
        "json",
        str(path),
    ]
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed for {path}: {result.stderr[-1000:]}")
    data = json.loads(result.stdout)
    streams = data.get("streams") or []
    if not streams:
        raise RuntimeError(f"No audio stream: {path}")
    stream = streams[0]
    raw_duration = stream.get("duration") or data.get("format", {}).get("duration")
    duration = float(raw_duration)
    return {
        "codec": stream.get("codec_name"),
        "sample_rate": int(stream["sample_rate"]) if stream.get("sample_rate") else None,
        "channels": stream.get("channels"),
        "channel_layout": stream.get("channel_layout"),
        "duration": round(duration, 6),
    }


def build_entry(path: Path, asset_root: Path, sources: dict[str, Any]) -> dict[str, Any]:
    relative = path.relative_to(asset_root)
    category = relative.parts[0]
    source_id = path.stem.split("__", 1)[0]
    if source_id not in sources:
        raise ValueError(f"Unknown source_id {source_id!r} for {path}")
    tags = set(CATEGORY_TAGS.get(category, []))
    tags.update(split_tokens(path.stem))
    return {
        "id": relative.with_suffix("").as_posix(),
        "path": (Path("assets") / "sfx" / relative).as_posix(),
        "category": category,
        "source_id": source_id,
        "tags": sorted(tags),
        **probe(path),
        "size_bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--asset-root", type=Path, default=DEFAULT_ASSET_ROOT)
    parser.add_argument("--sources", type=Path, default=DEFAULT_SOURCES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--workers", type=int, default=8)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    asset_root = args.asset_root.expanduser().resolve()
    sources_path = args.sources.expanduser().resolve()
    output = args.output.expanduser().resolve()
    sources_payload = json.loads(sources_path.read_text(encoding="utf-8-sig"))
    sources = {item["id"]: item for item in sources_payload["sources"]}
    files = sorted(
        path
        for path in asset_root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in AUDIO_EXTENSIONS
        and "licenses" not in path.parts
    )
    if not files:
        raise RuntimeError(f"No audio files found under {asset_root}")
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        entries = list(pool.map(lambda path: build_entry(path, asset_root, sources), files))
    entries.sort(key=lambda entry: entry["id"])
    category_counts = Counter(entry["category"] for entry in entries)
    source_counts = Counter(entry["source_id"] for entry in entries)
    payload = {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "asset_root": "assets/sfx",
        "total": len(entries),
        "category_counts": dict(sorted(category_counts.items())),
        "source_counts": dict(sorted(source_counts.items())),
        "entries": entries,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "total": len(entries), "categories": payload["category_counts"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
