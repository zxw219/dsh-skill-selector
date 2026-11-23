#!/usr/bin/env python3
"""Probe media and extract technical, scene-cut, and silence evidence."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any


def executable(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"Required executable not found on PATH: {name}")
    return path


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if check and result.returncode != 0:
        tail = result.stderr[-4000:]
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(command)}\n{tail}")
    return result


def ffprobe(path: Path) -> dict[str, Any]:
    command = [
        executable("ffprobe"),
        "-v",
        "error",
        "-show_format",
        "-show_streams",
        "-of",
        "json",
        str(path),
    ]
    return json.loads(run(command).stdout)


def float_or_none(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def fps_from_stream(stream: dict[str, Any]) -> float | None:
    value = stream.get("avg_frame_rate") or stream.get("r_frame_rate")
    if not value or value == "0/0":
        return None
    try:
        return float(Fraction(value))
    except (ValueError, ZeroDivisionError):
        return None


def duration_from_probe(data: dict[str, Any]) -> float:
    candidates = [float_or_none(data.get("format", {}).get("duration"))]
    candidates.extend(float_or_none(s.get("duration")) for s in data.get("streams", []))
    values = [v for v in candidates if v is not None and v >= 0]
    if not values:
        raise RuntimeError("Could not determine media duration")
    return max(values)


def summarize_probe(data: dict[str, Any]) -> dict[str, Any]:
    video_streams = [s for s in data.get("streams", []) if s.get("codec_type") == "video"]
    audio_streams = [s for s in data.get("streams", []) if s.get("codec_type") == "audio"]
    videos = []
    for s in video_streams:
        videos.append(
            {
                "index": s.get("index"),
                "codec": s.get("codec_name"),
                "width": s.get("width"),
                "height": s.get("height"),
                "fps": fps_from_stream(s),
                "duration": float_or_none(s.get("duration")),
                "pixel_format": s.get("pix_fmt"),
            }
        )
    audios = []
    for s in audio_streams:
        audios.append(
            {
                "index": s.get("index"),
                "codec": s.get("codec_name"),
                "sample_rate": int(s["sample_rate"]) if s.get("sample_rate") else None,
                "channels": s.get("channels"),
                "channel_layout": s.get("channel_layout"),
                "duration": float_or_none(s.get("duration")),
            }
        )
    return {
        "duration": duration_from_probe(data),
        "format_name": data.get("format", {}).get("format_name"),
        "size_bytes": int(data.get("format", {}).get("size", 0) or 0),
        "video_streams": videos,
        "audio_streams": audios,
    }


def detect_scenes(path: Path, threshold: float) -> list[float]:
    filter_value = f"select='gt(scene,{threshold})',showinfo"
    command = [
        executable("ffmpeg"),
        "-hide_banner",
        "-nostats",
        "-i",
        str(path),
        "-map",
        "0:v:0",
        "-vf",
        filter_value,
        "-an",
        "-f",
        "null",
        "-",
    ]
    result = run(command)
    found = re.findall(r"pts_time:([0-9]+(?:\.[0-9]+)?)", result.stderr)
    return sorted({round(float(value), 3) for value in found})


def detect_silence(path: Path, noise_db: float, minimum_duration: float) -> list[dict[str, float]]:
    command = [
        executable("ffmpeg"),
        "-hide_banner",
        "-nostats",
        "-i",
        str(path),
        "-map",
        "0:a:0",
        "-af",
        f"silencedetect=noise={noise_db}dB:d={minimum_duration}",
        "-vn",
        "-f",
        "null",
        "-",
    ]
    result = run(command)
    starts = [float(v) for v in re.findall(r"silence_start: ([0-9]+(?:\.[0-9]+)?)", result.stderr)]
    ends = [
        (float(end), float(duration))
        for end, duration in re.findall(
            r"silence_end: ([0-9]+(?:\.[0-9]+)?) \| silence_duration: ([0-9]+(?:\.[0-9]+)?)",
            result.stderr,
        )
    ]
    regions: list[dict[str, float]] = []
    for index, (end, duration) in enumerate(ends):
        start = starts[index] if index < len(starts) else max(0.0, end - duration)
        regions.append(
            {
                "start": round(start, 3),
                "end": round(end, 3),
                "duration": round(duration, 3),
            }
        )
    return regions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("media", type=Path, help="Video or audio file to inspect")
    parser.add_argument("--output", type=Path, help="Write the JSON report to this path")
    parser.add_argument("--scene-threshold", type=float, default=0.35)
    parser.add_argument("--silence-noise-db", type=float, default=-40.0)
    parser.add_argument("--silence-min-duration", type=float, default=0.25)
    parser.add_argument("--skip-scenes", action="store_true")
    parser.add_argument("--skip-silence", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    media = args.media.expanduser().resolve()
    if not media.is_file():
        raise FileNotFoundError(media)
    raw = ffprobe(media)
    summary = summarize_probe(raw)
    has_video = bool(summary["video_streams"])
    has_audio = bool(summary["audio_streams"])

    report: dict[str, Any] = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "path": str(media),
        **summary,
        "scene_threshold": args.scene_threshold,
        "scene_cut_candidates": [],
        "silence_settings": {
            "noise_db": args.silence_noise_db,
            "minimum_duration": args.silence_min_duration,
        },
        "silence_regions": [],
        "semantic_analysis_required": has_video,
    }

    if has_video and not args.skip_scenes:
        report["scene_cut_candidates"] = detect_scenes(media, args.scene_threshold)
    if has_audio and not args.skip_silence:
        report["silence_regions"] = detect_silence(
            media, args.silence_noise_db, args.silence_min_duration
        )

    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        output = args.output.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # concise CLI failure
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
