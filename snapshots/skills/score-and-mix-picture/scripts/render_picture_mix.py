#!/usr/bin/env python3
"""Render a score-only edit and a dialogue-safe full mix from a JSON plan."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TOLERANCE_SECONDS = 0.020


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
        tail = result.stderr[-6000:]
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(command)}\n{tail}")
    return result


def probe(path: Path) -> dict[str, Any]:
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


def as_float(value: Any, label: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(result):
        raise ValueError(f"{label} must be finite")
    return result


def media_duration(data: dict[str, Any]) -> float:
    values: list[float] = []
    raw_values = [data.get("format", {}).get("duration")]
    raw_values.extend(stream.get("duration") for stream in data.get("streams", []))
    for raw in raw_values:
        try:
            value = float(raw)
        except (TypeError, ValueError):
            continue
        if math.isfinite(value) and value >= 0:
            values.append(value)
    if not values:
        raise RuntimeError("Could not determine media duration")
    return max(values)


def has_audio(data: dict[str, Any]) -> bool:
    return any(stream.get("codec_type") == "audio" for stream in data.get("streams", []))


def audio_summary(path: Path, data: dict[str, Any] | None = None) -> dict[str, Any]:
    data = data or probe(path)
    streams = [s for s in data.get("streams", []) if s.get("codec_type") == "audio"]
    first = streams[0] if streams else {}
    return {
        "path": str(path),
        "duration": round(media_duration(data), 6),
        "codec": first.get("codec_name"),
        "sample_rate": int(first["sample_rate"]) if first.get("sample_rate") else None,
        "channels": first.get("channels"),
        "size_bytes": path.stat().st_size,
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_path(raw: Any, base: Path, label: str) -> Path:
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError(f"{label} must be a non-empty path string")
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = base / path
    path = path.resolve()
    if not path.is_file():
        raise FileNotFoundError(f"{label} not found: {path}")
    return path


def validate_clip_list(
    raw_clips: Any,
    *,
    prefix: str,
    base: Path,
    picture_duration: float,
    required: bool,
) -> list[dict[str, Any]]:
    if raw_clips is None and not required:
        return []
    if not isinstance(raw_clips, list) or (required and not raw_clips):
        requirement = "at least one cue entry" if required else "a list"
        raise ValueError(f"{prefix} must contain {requirement}")
    clips: list[dict[str, Any]] = []
    for index, raw_clip in enumerate(raw_clips):
        label = f"{prefix}[{index}]"
        if not isinstance(raw_clip, dict):
            raise ValueError(f"{label} must be an object")
        path = resolve_path(raw_clip.get("path"), base, f"{label}.path")
        source_probe = probe(path)
        if not has_audio(source_probe):
            raise ValueError(f"{label}.path has no audio stream: {path}")
        source_duration = media_duration(source_probe)
        timeline_start = as_float(raw_clip.get("timeline_start", 0.0), f"{label}.timeline_start")
        source_in = as_float(raw_clip.get("source_in", 0.0), f"{label}.source_in")
        requested_duration = raw_clip.get("duration")
        if requested_duration is None:
            duration = min(source_duration - source_in, picture_duration - timeline_start)
        else:
            duration = as_float(requested_duration, f"{label}.duration")
        fade_in = as_float(raw_clip.get("fade_in", 0.0), f"{label}.fade_in")
        fade_out = as_float(raw_clip.get("fade_out", 0.0), f"{label}.fade_out")
        gain_db = as_float(raw_clip.get("gain_db", 0.0), f"{label}.gain_db")
        loop = bool(raw_clip.get("loop", False))

        if timeline_start < 0 or timeline_start >= picture_duration:
            raise ValueError(f"{label}.timeline_start falls outside picture duration")
        if source_in < 0 or source_in >= source_duration:
            raise ValueError(f"{label}.source_in falls outside source duration")
        if duration <= 0:
            raise ValueError(f"{label}.duration must be greater than zero")
        if timeline_start + duration > picture_duration + TOLERANCE_SECONDS:
            raise ValueError(f"{label} ends after picture; shorten duration or move it earlier")
        if not loop and source_in + duration > source_duration + TOLERANCE_SECONDS:
            raise ValueError(f"{label} requests more source audio than available; edit duration or set loop=true")
        if fade_in < 0 or fade_out < 0 or fade_in + fade_out > duration:
            raise ValueError(f"{label} has invalid fades for its duration")
        if gain_db < -120 or gain_db > 24:
            raise ValueError(f"{label}.gain_db must be between -120 and +24")

        clips.append(
            {
                "path": path,
                "source_probe": source_probe,
                "source_duration": source_duration,
                "timeline_start": timeline_start,
                "source_in": source_in,
                "duration": min(duration, picture_duration - timeline_start),
                "fade_in": fade_in,
                "fade_out": fade_out,
                "gain_db": gain_db,
                "loop": loop,
                "label": str(raw_clip.get("label") or f"{prefix}-{index + 1}"),
            }
        )
    return clips


def load_and_validate(plan_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    plan = json.loads(plan_path.read_text(encoding="utf-8-sig"))
    if not isinstance(plan, dict):
        raise ValueError("Mix plan root must be an object")
    base = plan_path.parent
    picture = resolve_path(plan.get("picture"), base, "picture")
    picture_probe = probe(picture)
    picture_duration = media_duration(picture_probe)

    clips = validate_clip_list(
        plan.get("music"),
        prefix="music",
        base=base,
        picture_duration=picture_duration,
        required=True,
    )
    sfx_clips = validate_clip_list(
        plan.get("sfx"),
        prefix="sfx",
        base=base,
        picture_duration=picture_duration,
        required=False,
    )

    original = plan.get("original_audio") or {}
    ducking = plan.get("ducking") or {}
    master = plan.get("master") or {}
    config = {
        "picture": picture,
        "picture_probe": picture_probe,
        "picture_duration": picture_duration,
        "picture_has_audio": has_audio(picture_probe),
        "clips": clips,
        "sfx_clips": sfx_clips,
        "original_audio": {
            "enabled": bool(original.get("enabled", True)),
            "gain_db": as_float(original.get("gain_db", 0.0), "original_audio.gain_db"),
        },
        "ducking": {
            "enabled": bool(ducking.get("enabled", True)),
            "threshold": as_float(ducking.get("threshold", 0.025), "ducking.threshold"),
            "ratio": as_float(ducking.get("ratio", 8.0), "ducking.ratio"),
            "attack_ms": as_float(ducking.get("attack_ms", 15.0), "ducking.attack_ms"),
            "release_ms": as_float(ducking.get("release_ms", 350.0), "ducking.release_ms"),
            "speech_band": bool(ducking.get("speech_band", True)),
        },
        "master": {
            "sample_rate": int(master.get("sample_rate", 48000)),
            "music_target_lufs": as_float(master.get("music_target_lufs", -18.0), "master.music_target_lufs"),
            "full_mix_target_lufs": as_float(master.get("full_mix_target_lufs", -14.0), "master.full_mix_target_lufs"),
            "loudness_range": as_float(master.get("loudness_range", 11.0), "master.loudness_range"),
            "true_peak_db": as_float(master.get("true_peak_db", -1.0), "master.true_peak_db"),
        },
    }

    d = config["ducking"]
    if not (0.000976 <= d["threshold"] <= 1.0):
        raise ValueError("ducking.threshold must be between 0.000976 and 1.0")
    if not (1.0 <= d["ratio"] <= 20.0):
        raise ValueError("ducking.ratio must be between 1 and 20")
    if not (0.01 <= d["attack_ms"] <= 2000):
        raise ValueError("ducking.attack_ms must be between 0.01 and 2000")
    if not (0.01 <= d["release_ms"] <= 9000):
        raise ValueError("ducking.release_ms must be between 0.01 and 9000")

    m = config["master"]
    if not (8000 <= m["sample_rate"] <= 192000):
        raise ValueError("master.sample_rate must be between 8000 and 192000")
    if not (-70 <= m["music_target_lufs"] <= -5 and -70 <= m["full_mix_target_lufs"] <= -5):
        raise ValueError("LUFS targets must be between -70 and -5")
    if not (-9 <= m["true_peak_db"] <= 0):
        raise ValueError("master.true_peak_db must be between -9 and 0")
    return plan, config


def render_bus_raw(
    clips: list[dict[str, Any]],
    *,
    duration: float,
    sample_rate: int,
    output: Path,
    output_label: str,
) -> None:
    if not clips:
        raise ValueError("render_bus_raw requires at least one clip")
    command = [executable("ffmpeg"), "-hide_banner", "-nostats", "-y"]
    for clip in clips:
        if clip["loop"]:
            command.extend(["-stream_loop", "-1"])
        command.extend(["-i", str(clip["path"])])

    filters: list[str] = []
    labels: list[str] = []
    for index, clip in enumerate(clips):
        chain = [
            f"[{index}:a:0]atrim=start={clip['source_in']:.6f}:duration={clip['duration']:.6f}",
            "asetpts=PTS-STARTPTS",
            f"aresample={sample_rate}",
            "aformat=sample_fmts=fltp:channel_layouts=stereo",
        ]
        if clip["fade_in"] > 0:
            chain.append(f"afade=t=in:st=0:d={clip['fade_in']:.6f}:curve=qsin")
        if clip["fade_out"] > 0:
            fade_start = clip["duration"] - clip["fade_out"]
            chain.append(f"afade=t=out:st={fade_start:.6f}:d={clip['fade_out']:.6f}:curve=qsin")
        chain.append(f"volume={clip['gain_db']:.3f}dB")
        delay_ms = round(clip["timeline_start"] * 1000)
        if delay_ms > 0:
            chain.append(f"adelay={delay_ms}:all=1")
        label = f"b{index}"
        filters.append(",".join(chain) + f"[{label}]")
        labels.append(f"[{label}]")

    filters.append(
        "".join(labels)
        + f"amix=inputs={len(labels)}:duration=longest:dropout_transition=0:normalize=0,"
        + f"apad=pad_dur={duration:.6f},atrim=duration={duration:.6f}[{output_label}]"
    )
    command.extend(
        [
            "-filter_complex",
            ";".join(filters),
            "-map",
            f"[{output_label}]",
            "-t",
            f"{duration:.6f}",
            "-ar",
            str(sample_rate),
            "-ac",
            "2",
            "-c:a",
            "pcm_f32le",
            str(output),
        ]
    )
    run(command)


def render_music_raw(config: dict[str, Any], output: Path) -> None:
    render_bus_raw(
        config["clips"],
        duration=config["picture_duration"],
        sample_rate=config["master"]["sample_rate"],
        output=output,
        output_label="musicraw",
    )


def render_sfx_raw(config: dict[str, Any], output: Path) -> None:
    render_bus_raw(
        config["sfx_clips"],
        duration=config["picture_duration"],
        sample_rate=config["master"]["sample_rate"],
        output=output,
        output_label="sfxraw",
    )


def parse_loudnorm(stderr: str) -> dict[str, Any]:
    blocks = re.findall(r"\{\s*\"input_i\".*?\}", stderr, flags=re.DOTALL)
    if not blocks:
        raise RuntimeError("FFmpeg loudnorm did not return JSON measurements")
    return json.loads(blocks[-1])


def measure_loudness(path: Path, target: float, lra: float, true_peak: float) -> dict[str, Any]:
    command = [
        executable("ffmpeg"),
        "-hide_banner",
        "-nostats",
        "-i",
        str(path),
        "-af",
        f"loudnorm=I={target}:LRA={lra}:TP={true_peak}:print_format=json",
        "-f",
        "null",
        "-",
    ]
    return parse_loudnorm(run(command).stderr)


def finite_measurements(measurements: dict[str, Any]) -> bool:
    keys = ["input_i", "input_lra", "input_tp", "input_thresh", "target_offset"]
    try:
        return all(math.isfinite(float(measurements[key])) for key in keys)
    except (KeyError, TypeError, ValueError):
        return False


def normalize_two_pass(
    source: Path,
    output: Path,
    *,
    target: float,
    lra: float,
    true_peak: float,
    sample_rate: int,
    duration: float,
) -> dict[str, Any]:
    measured = measure_loudness(source, target, lra, true_peak)
    if finite_measurements(measured):
        loudnorm = (
            f"loudnorm=I={target}:LRA={lra}:TP={true_peak}:"
            f"measured_I={measured['input_i']}:measured_LRA={measured['input_lra']}:"
            f"measured_TP={measured['input_tp']}:measured_thresh={measured['input_thresh']}:"
            f"offset={measured['target_offset']}:linear=true:print_format=summary"
        )
        mode = "two-pass-linear"
    else:
        loudnorm = f"loudnorm=I={target}:LRA={lra}:TP={true_peak}:linear=false:print_format=summary"
        mode = "single-pass-dynamic-fallback"
    limiter = 10 ** (true_peak / 20.0)
    filter_value = f"{loudnorm},alimiter=limit={limiter:.8f}:attack=5:release=50:level=false"
    command = [
        executable("ffmpeg"),
        "-hide_banner",
        "-nostats",
        "-y",
        "-i",
        str(source),
        "-af",
        filter_value,
        "-t",
        f"{duration:.6f}",
        "-ar",
        str(sample_rate),
        "-ac",
        "2",
        "-c:a",
        "pcm_s24le",
        str(output),
    ]
    run(command)
    final_measurement = measure_loudness(output, target, lra, true_peak)
    return {"mode": mode, "first_pass": measured, "output_measurement": final_measurement}


def render_sfx_master(
    source: Path,
    output: Path,
    *,
    true_peak: float,
    sample_rate: int,
    duration: float,
) -> None:
    limiter = 10 ** (true_peak / 20.0)
    command = [
        executable("ffmpeg"),
        "-hide_banner",
        "-nostats",
        "-y",
        "-i",
        str(source),
        "-af",
        f"alimiter=limit={limiter:.8f}:attack=1:release=50:level=false",
        "-t",
        f"{duration:.6f}",
        "-ar",
        str(sample_rate),
        "-ac",
        "2",
        "-c:a",
        "pcm_s24le",
        str(output),
    ]
    run(command)


def render_full_mix_raw(
    config: dict[str, Any],
    music_edit: Path,
    output: Path,
    *,
    use_original: bool,
    sfx_edit: Path | None,
) -> None:
    picture = config["picture"]
    duration = config["picture_duration"]
    sample_rate = config["master"]["sample_rate"]
    original_gain = config["original_audio"]["gain_db"]
    ducking = config["ducking"]
    command = [
        executable("ffmpeg"),
        "-hide_banner",
        "-nostats",
        "-y",
        "-i",
        str(picture),
        "-i",
        str(music_edit),
    ]
    if sfx_edit is not None:
        command.extend(["-i", str(sfx_edit)])
    filters = [
        f"[1:a:0]aresample={sample_rate},aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"apad=pad_dur={duration:.6f},atrim=duration={duration:.6f}[musicbase]",
    ]
    mix_labels: list[str]
    if use_original:
        filters.insert(
            0,
            f"[0:a:0]aresample={sample_rate},aformat=sample_fmts=fltp:channel_layouts=stereo,"
            f"volume={original_gain:.3f}dB,apad=pad_dur={duration:.6f},atrim=duration={duration:.6f}[origbase]",
        )
        if ducking["enabled"]:
            filters.append("[origbase]asplit=2[origmix][detectbase]")
            if ducking["speech_band"]:
                filters.append("[detectbase]highpass=f=120,lowpass=f=5000[detect]")
            else:
                filters.append("[detectbase]anull[detect]")
            filters.append(
                "[musicbase][detect]sidechaincompress="
                f"threshold={ducking['threshold']}:ratio={ducking['ratio']}:"
                f"attack={ducking['attack_ms']}:release={ducking['release_ms']}:"
                "makeup=1:knee=2.828:link=average:detection=rms[ducked]"
            )
            mix_labels = ["[origmix]", "[ducked]"]
        else:
            mix_labels = ["[origbase]", "[musicbase]"]
    else:
        mix_labels = ["[musicbase]"]
    if sfx_edit is not None:
        filters.append(
            f"[2:a:0]aresample={sample_rate},aformat=sample_fmts=fltp:channel_layouts=stereo,"
            f"apad=pad_dur={duration:.6f},atrim=duration={duration:.6f}[sfxbase]"
        )
        mix_labels.append("[sfxbase]")
    if len(mix_labels) == 1:
        filters.append(f"{mix_labels[0]}anull[fullraw]")
    else:
        filters.append(
            "".join(mix_labels)
            + f"amix=inputs={len(mix_labels)}:duration=longest:dropout_transition=0:normalize=0,"
            + f"apad=pad_dur={duration:.6f},atrim=duration={duration:.6f}[fullraw]"
        )
    command.extend(
        [
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[fullraw]",
            "-t",
            f"{duration:.6f}",
            "-ar",
            str(sample_rate),
            "-ac",
            "2",
            "-c:a",
            "pcm_f32le",
            str(output),
        ]
    )
    run(command)


def verify_duration(path: Path, expected: float) -> dict[str, Any]:
    data = probe(path)
    actual = media_duration(data)
    delta = actual - expected
    if abs(delta) > TOLERANCE_SECONDS:
        raise RuntimeError(
            f"Output duration mismatch for {path.name}: expected {expected:.6f}s, got {actual:.6f}s"
        )
    return {"probe": data, "duration": actual, "duration_delta": delta}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="Path to the JSON mix plan")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--force", action="store_true", help="Overwrite existing deliverables")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plan_path = args.plan.expanduser().resolve()
    if not plan_path.is_file():
        raise FileNotFoundError(plan_path)
    _, config = load_and_validate(plan_path)

    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    music_output = output_dir / "music-edit.wav"
    sfx_output = output_dir / "sfx-edit.wav"
    full_output = output_dir / "full-mix.wav"
    report_output = output_dir / "mix-report.json"
    planned_outputs = [music_output, full_output, report_output]
    if config["sfx_clips"]:
        planned_outputs.append(sfx_output)
    existing = [path for path in planned_outputs if path.exists()]
    if existing and not args.force:
        names = ", ".join(path.name for path in existing)
        raise FileExistsError(f"Deliverables already exist ({names}); use --force to replace them")

    master = config["master"]
    duration = config["picture_duration"]
    notes: list[str] = []

    with tempfile.TemporaryDirectory(prefix="score-and-mix-picture-") as temp_name:
        temp_dir = Path(temp_name)
        music_raw = temp_dir / "music-raw.wav"
        sfx_raw = temp_dir / "sfx-raw.wav"
        full_raw = temp_dir / "full-raw.wav"
        render_music_raw(config, music_raw)
        music_loudness = normalize_two_pass(
            music_raw,
            music_output,
            target=master["music_target_lufs"],
            lra=master["loudness_range"],
            true_peak=master["true_peak_db"],
            sample_rate=master["sample_rate"],
            duration=duration,
        )

        sfx_master: Path | None = None
        sfx_loudness: dict[str, Any] | None = None
        if config["sfx_clips"]:
            render_sfx_raw(config, sfx_raw)
            render_sfx_master(
                sfx_raw,
                sfx_output,
                true_peak=master["true_peak_db"],
                sample_rate=master["sample_rate"],
                duration=duration,
            )
            sfx_master = sfx_output
            sfx_loudness = measure_loudness(
                sfx_output,
                master["full_mix_target_lufs"],
                master["loudness_range"],
                master["true_peak_db"],
            )

        use_original = config["original_audio"]["enabled"] and config["picture_has_audio"]
        if use_original or sfx_master is not None:
            render_full_mix_raw(
                config,
                music_output,
                full_raw,
                use_original=use_original,
                sfx_edit=sfx_master,
            )
            full_loudness = normalize_two_pass(
                full_raw,
                full_output,
                target=master["full_mix_target_lufs"],
                lra=master["loudness_range"],
                true_peak=master["true_peak_db"],
                sample_rate=master["sample_rate"],
                duration=duration,
            )
            if not use_original:
                if not config["picture_has_audio"]:
                    notes.append("Picture contains no audio stream; full-mix.wav contains music plus the SFX bus.")
                else:
                    notes.append("Original audio was disabled; full-mix.wav contains music plus the SFX bus.")
        else:
            shutil.copy2(music_output, full_output)
            full_loudness = music_loudness
            if not config["picture_has_audio"]:
                notes.append("Picture contains no audio stream; full-mix.wav is identical to music-edit.wav.")
            else:
                notes.append("Original audio was disabled; full-mix.wav is identical to music-edit.wav.")

    music_verified = verify_duration(music_output, duration)
    sfx_verified = verify_duration(sfx_output, duration) if config["sfx_clips"] else None
    full_verified = verify_duration(full_output, duration)

    def report_clips(clips: list[dict[str, Any]]) -> list[dict[str, Any]]:
        result = []
        for clip in clips:
            result.append(
            {
                "label": clip["label"],
                "path": str(clip["path"]),
                "source_duration": clip["source_duration"],
                "timeline_start": clip["timeline_start"],
                "source_in": clip["source_in"],
                "duration": clip["duration"],
                "fade_in": clip["fade_in"],
                "fade_out": clip["fade_out"],
                "gain_db": clip["gain_db"],
                "loop": clip["loop"],
                "sha256": sha256(clip["path"]),
                "probe": audio_summary(clip["path"], clip["source_probe"]),
            }
        )
        return result

    music_clip_report = report_clips(config["clips"])
    sfx_clip_report = report_clips(config["sfx_clips"])

    report = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "render_engine": "FFmpeg",
        "plan": str(plan_path),
        "picture": {
            "path": str(config["picture"]),
            "duration": duration,
            "has_audio": config["picture_has_audio"],
        },
        "music_clips": music_clip_report,
        "sfx_clips": sfx_clip_report,
        "settings": {
            "original_audio": config["original_audio"],
            "ducking": config["ducking"],
            "master": config["master"],
        },
        "outputs": {
            "music_edit": {
                **audio_summary(music_output, music_verified["probe"]),
                "duration_delta": music_verified["duration_delta"],
                "sha256": sha256(music_output),
                "loudness": music_loudness,
            },
            "full_mix": {
                **audio_summary(full_output, full_verified["probe"]),
                "duration_delta": full_verified["duration_delta"],
                "sha256": sha256(full_output),
                "loudness": full_loudness,
            },
        },
        "notes": notes,
    }
    if sfx_verified is not None:
        report["outputs"]["sfx_edit"] = {
            **audio_summary(sfx_output, sfx_verified["probe"]),
            "duration_delta": sfx_verified["duration_delta"],
            "sha256": sha256(sfx_output),
            "loudness_measurement_only": sfx_loudness,
        }
    report_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "music_edit": str(music_output),
                **({"sfx_edit": str(sfx_output)} if config["sfx_clips"] else {}),
                "full_mix": str(full_output),
                "report": str(report_output),
                "duration": duration,
                "notes": notes,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # concise CLI failure
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
