#!/usr/bin/env python3
"""framecraft · 冲击点后期工具

Frame-addressed impact accents for existing footage: hit-stop holds, flashes,
ink / invert / punch tone hits, RGB split, decaying camera shake and punch-in
zoom, stacked through named recipes or a multi-hit cue file. Also ships
analysis helpers: contact sheets, candidate hit detection and an approximate
full-frame flash safety scan.

Python standard library only. Requires ffmpeg and ffprobe on PATH.
All outputs are new files. The input is never overwritten.
"""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction

VERSION = "2.1.0"

LEGACY_STYLES = ("white", "dark", "invert", "ink", "punch", "still")
LAYER_TYPES = ("hitstop", "flash", "invert", "ink", "punch", "rgbsplit", "shake", "zoom", "still")
MAX_CUES = 32
COLOR_RE = re.compile(r"^(white|black|red|yellow|orange|cyan|blue|magenta|#[0-9A-Fa-f]{6})$")

# Durations are in milliseconds so recipes behave the same at 24, 30 or 60 fps.
# "frames" wins over "ms" when both are present. "offset" may be "after_hold",
# meaning: start right after this cue's hit-stop ends.
RECIPES: dict[str, dict] = {
    "light": {
        "label": "轻击：一帧明暗脉冲＋轻微震动",
        "layers": [
            {"type": "punch", "frames": 1, "contrast": 1.18, "brightness": 0.06},
            {"type": "shake", "ms": 120, "amp": 0.004},
        ],
    },
    "heavy": {
        "label": "重击：顿帧＋明暗冲击＋衰减震动＋推近",
        "layers": [
            {"type": "hitstop", "ms": 80},
            {"type": "punch", "frames": 1, "contrast": 1.35, "brightness": 0.12},
            {"type": "shake", "ms": 220, "amp": 0.008},
            {"type": "zoom", "ms": 200, "zoom": 1.06},
        ],
    },
    "crit": {
        "label": "暴击／终结技：长顿帧＋白闪＋墨色硬对比＋强推近＋强震",
        "layers": [
            {"type": "hitstop", "ms": 140},
            {"type": "flash", "frames": 1, "color": "white", "strength": 0.8},
            {"type": "ink", "frames": 2, "offset_frames": 1},
            {"type": "zoom", "ms": 300, "zoom": 1.10},
            {"type": "shake", "ms": 320, "amp": 0.012},
        ],
    },
    "manga": {
        "label": "漫画：两帧墨色硬对比＋震动＋小推近",
        "layers": [
            {"type": "ink", "frames": 2},
            {"type": "shake", "ms": 200, "amp": 0.008},
            {"type": "zoom", "ms": 160, "zoom": 1.05},
        ],
    },
    "anime": {
        "label": "动画：一帧负片＋短顿帧＋推近＋震动",
        "layers": [
            {"type": "hitstop", "ms": 60},
            {"type": "invert", "frames": 1},
            {"type": "zoom", "ms": 220, "zoom": 1.08},
            {"type": "shake", "ms": 200, "amp": 0.008},
        ],
    },
    "energy": {
        "label": "能量：RGB 色散＋半强度白闪＋推近",
        "layers": [
            {"type": "rgbsplit", "ms": 200, "shift": 0.006},
            {"type": "flash", "frames": 1, "color": "white", "strength": 0.55},
            {"type": "zoom", "ms": 240, "zoom": 1.05},
        ],
    },
    "blackout": {
        "label": "暗帧顿挫：先看清命中（顿帧），再短黑",
        "layers": [
            {"type": "hitstop", "ms": 80},
            {"type": "flash", "frames": 2, "color": "black", "strength": 1.0, "offset": "after_hold"},
        ],
    },
    "cinema": {
        "label": "写实电影：克制的明暗脉冲＋小幅震动",
        "layers": [
            {"type": "punch", "frames": 1, "contrast": 1.15, "brightness": 0.05},
            {"type": "shake", "ms": 140, "amp": 0.004},
        ],
    },
}


class FramecraftError(Exception):
    """Actionable input or rendering problem."""


# ---------------------------------------------------------------- basics

def tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise FramecraftError(f"找不到 {name}；请先安装 FFmpeg 并确认它已加入 PATH。")
    return path


def run_checked(command: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode:
        tail = "\n".join(result.stderr.strip().splitlines()[-15:])
        raise FramecraftError(f"视频处理失败（返回码 {result.returncode}）。\n{tail}")
    return result


def parse_rate(value: str) -> Fraction:
    try:
        rate = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise FramecraftError(f"无法识别帧率：{value}") from exc
    if not (Fraction(1) <= rate <= Fraction(240)):
        raise FramecraftError(f"不支持的帧率：{value}。请检查视频文件。")
    return rate


def read_media(path: Path) -> dict:
    if not path.is_file():
        raise FramecraftError(f"没有找到视频文件：{path}")
    probe = run_checked([
        tool("ffprobe"), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)
    ])
    try:
        data = json.loads(probe.stdout)
        streams = data.get("streams") or []
        video = next(s for s in streams if s.get("codec_type") == "video")
        # r_frame_rate is the nominal cadence; avg_frame_rate can be inflated by
        # muxers that compute it from the last frame PTS.
        nominal = video.get("r_frame_rate") or "0"
        average = video.get("avg_frame_rate") or "0"
        try:
            rate = parse_rate(nominal)
        except FramecraftError:
            rate = parse_rate(average)
        try:
            average_rate = parse_rate(average)
        except FramecraftError:
            average_rate = rate
        duration = float(data.get("format", {}).get("duration") or video.get("duration") or "0")
        width, height = int(video["width"]), int(video["height"])
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError("bad duration")
        if width <= 0 or height <= 0:
            raise ValueError("bad dimensions")
        return {
            "input": str(path.resolve()), "fps": rate, "fps_display": str(rate),
            "duration": duration, "width": width, "height": height,
            "frames_estimate": math.ceil(duration * float(rate) - 1e-7),
            "has_audio": any(s.get("codec_type") == "audio" for s in streams),
            "variable_rate_possible": abs(float(rate - average_rate)) / float(rate) > 0.03,
            "codec": video.get("codec_name", "unknown"),
        }
    except (StopIteration, KeyError, ValueError, TypeError, ZeroDivisionError) as exc:
        raise FramecraftError("无法读取有效视频流、分辨率、帧率或时长。") from exc


def total_frames(duration: float, fps: Fraction) -> int:
    return math.ceil(duration * float(fps) - 1e-7)


def plan_frames(at: float, frames: int, fps: Fraction, duration: float) -> tuple[int, int]:
    """Legacy helper: contact frame index and last affected frame for a block."""
    if not math.isfinite(at) or at < 0:
        raise FramecraftError("击点时间必须是从 0 开始的有限秒数。")
    if not isinstance(frames, int) or frames < 1:
        raise FramecraftError("持续帧数必须是至少 1 的整数。")
    total = total_frames(duration, fps)
    start = math.floor(at * float(fps) + 0.5)
    if start >= total:
        raise FramecraftError(f"击点 {at:.3f}s 超出了视频画面范围（约 {duration:.3f}s）。")
    if start + frames > total:
        raise FramecraftError(f"从第 {start} 帧开始插 {frames} 帧会越过末尾；请缩短帧数或提前击点。")
    return start, start + frames - 1


def ms_to_frames(ms: float, fps: Fraction) -> int:
    if not math.isfinite(ms) or ms <= 0:
        raise FramecraftError("毫秒时长必须是正数。")
    return max(1, math.floor(ms * float(fps) / 1000 + 0.5))


def validate_output(source: Path, output: Path, suffix: str = ".mp4") -> None:
    # Refuse existing targets outright, including symlinks, hardlinks and the source itself.
    if output.is_symlink() or output.exists():
        raise FramecraftError(f"输出位置已存在文件：{output}。为保护原有内容，请换个新文件名。")
    if source.resolve() == output.resolve():
        raise FramecraftError("输出路径不能等于输入路径。")
    if output.suffix.lower() != suffix:
        raise FramecraftError(f"输出请使用 {suffix} 扩展名。")
    if not output.parent.is_dir():
        raise FramecraftError(f"输出目录不存在：{output.parent}")


def safe_publish(temporary: Path, output: Path) -> None:
    """Publish without ever overwriting a target, including creation races."""
    try:
        os.link(temporary, output)
    except FileExistsError as exc:
        raise FramecraftError(f"输出文件已经存在：{output}") from exc
    except OSError:
        try:
            with output.open("xb") as destination, temporary.open("rb") as origin:
                shutil.copyfileobj(origin, destination, 1024 * 1024)
        except FileExistsError as exc:
            raise FramecraftError(f"输出文件已经存在：{output}") from exc
        except Exception:
            output.unlink(missing_ok=True)
            raise


# ---------------------------------------------------------------- cue model

def legacy_layers(style: str, frames: int) -> list[dict]:
    if style not in LEGACY_STYLES:
        raise FramecraftError(f"样式必须是：{', '.join(LEGACY_STYLES)}")
    if style == "white":
        return [{"type": "flash", "frames": frames, "color": "white", "strength": 1.0}]
    if style == "dark":
        return [{"type": "flash", "frames": frames, "color": "black", "strength": 1.0}]
    if style == "punch":
        return [{"type": "punch", "frames": frames}]
    return [{"type": style, "frames": frames}]


def _number(layer: dict, key: str, default: float, low: float, high: float) -> float:
    value = layer.get(key, default)
    try:
        value = float(value)
    except (TypeError, ValueError) as exc:
        raise FramecraftError(f"图层参数 {key} 必须是数字。") from exc
    if not (math.isfinite(value) and low <= value <= high):
        raise FramecraftError(f"图层参数 {key}={value} 超出允许范围 {low}–{high}。")
    return value


def _focus(value) -> tuple[float, float]:
    if value is None:
        return (0.5, 0.5)
    if isinstance(value, str):
        value = value.split(",")
    try:
        fx, fy = (float(v) for v in value)
    except (TypeError, ValueError) as exc:
        raise FramecraftError("焦点格式应为 x,y（0–1 之间的比例，例如 0.62,0.40）。") from exc
    if not (0 <= fx <= 1 and 0 <= fy <= 1):
        raise FramecraftError("焦点 x,y 必须都在 0 到 1 之间。")
    return (fx, fy)


def resolve_cues(raw_cues: list[dict], fps: Fraction, duration: float, width: int,
                 default_image: Path | None = None) -> list[dict]:
    """Turn user cues (seconds, recipes, ms) into concrete frame-addressed layers."""
    if not raw_cues:
        raise FramecraftError("至少需要一个击点。")
    if len(raw_cues) > MAX_CUES:
        raise FramecraftError(f"一次最多处理 {MAX_CUES} 个击点；请分段处理。")
    total = total_frames(duration, fps)
    resolved = []
    for index, cue in enumerate(raw_cues, 1):
        if not isinstance(cue, dict) or "at" not in cue:
            raise FramecraftError(f"第 {index} 个击点缺少 at（秒数）。")
        try:
            at = float(cue["at"])
        except (TypeError, ValueError) as exc:
            raise FramecraftError(f"第 {index} 个击点的 at 不是数字。") from exc
        if not math.isfinite(at) or at < 0:
            raise FramecraftError("击点时间必须是从 0 开始的有限秒数。")
        start = math.floor(at * float(fps) + 0.5)
        if start >= total:
            raise FramecraftError(f"击点 {at:.3f}s 超出了视频画面范围（约 {duration:.3f}s）。")
        if "layers" in cue:
            layers = cue["layers"]
            name = cue.get("recipe", "custom")
        else:
            name = cue.get("recipe", "heavy")
            if name not in RECIPES:
                raise FramecraftError(f"未知配方：{name}。可选：{', '.join(RECIPES)}")
            layers = RECIPES[name]["layers"]
        if not isinstance(layers, list) or not layers:
            raise FramecraftError(f"第 {index} 个击点的 layers 必须是非空列表。")
        focus = _focus(cue.get("focus"))
        hold = 0
        out_layers = []
        # Hit-stop first so "after_hold" offsets can see it.
        ordered = sorted(layers, key=lambda layer: 0 if layer.get("type") == "hitstop" else 1)
        for layer in ordered:
            if not isinstance(layer, dict):
                raise FramecraftError("每个图层必须是对象。")
            kind = layer.get("type")
            if kind not in LAYER_TYPES:
                raise FramecraftError(f"未知图层类型：{kind}。可选：{', '.join(LAYER_TYPES)}")
            if "frames" in layer:
                frames = layer["frames"]
                if not isinstance(frames, int) or isinstance(frames, bool) or frames < 1:
                    raise FramecraftError("图层 frames 必须是至少 1 的整数。")
            elif "ms" in layer:
                frames = ms_to_frames(float(layer["ms"]), fps)
            else:
                frames = 1
            offset_raw = layer.get("offset_frames", layer.get("offset", 0))
            if offset_raw == "after_hold":
                offset = hold
            elif isinstance(offset_raw, int) and not isinstance(offset_raw, bool) and offset_raw >= 0:
                offset = offset_raw
            else:
                raise FramecraftError("offset_frames 必须是非负整数或 \"after_hold\"。")
            first = start + offset
            if kind == "hitstop":
                # Hold the contact frame: frames first+1 .. first+frames show frame `first`.
                last_allowed = total - 1
                frames = min(frames, last_allowed - first)
                if frames < 1:
                    continue
                hold = frames
                item = {"type": kind, "first": first, "last": first + frames, "frames": frames}
            else:
                if first >= total:
                    continue
                last = min(first + frames - 1, total - 1)
                item = {"type": kind, "first": first, "last": last, "frames": last - first + 1}
            if kind == "flash":
                color = str(layer.get("color", "white"))
                if not COLOR_RE.match(color):
                    raise FramecraftError("flash 颜色可用 white/black/red/yellow/orange/cyan/blue/magenta 或 #RRGGBB。")
                item["color"] = color
                item["strength"] = _number(layer, "strength", 1.0, 0.05, 1.0)
            elif kind == "punch":
                item["contrast"] = _number(layer, "contrast", 1.33, 1.0, 2.5)
                item["brightness"] = _number(layer, "brightness", 0.14, -0.3, 0.4)
            elif kind == "ink":
                item["contrast"] = _number(layer, "contrast", 2.6, 1.2, 4.0)
            elif kind == "rgbsplit":
                item["shift_px"] = max(1, round(width * _number(layer, "shift", 0.006, 0.001, 0.05)))
            elif kind == "shake":
                amp = round(width * _number(layer, "amp", 0.008, 0.001, 0.05) / 2) * 2
                item["amp_px"] = max(2, amp)
                direction = str(layer.get("direction", "both"))
                if direction not in ("both", "h", "v"):
                    raise FramecraftError("shake 的 direction 只能是 both、h（横震）或 v（竖震）。")
                item["direction"] = direction
            elif kind == "zoom":
                item["zoom"] = _number(layer, "zoom", 1.06, 1.005, 1.6)
                item["focus"] = _focus(layer.get("focus")) if "focus" in layer else focus
            elif kind == "still":
                image = layer.get("image", default_image)
                if not image:
                    raise FramecraftError("still（插入冲击图）必须提供图片路径。")
                image = Path(image).expanduser()
                if not image.is_file():
                    raise FramecraftError(f"找不到冲击图：{image}")
                if image.suffix.lower() not in (".png", ".jpg", ".jpeg"):
                    raise FramecraftError("冲击图片必须为 PNG/JPEG。")
                item["image"] = str(image.resolve())
            out_layers.append(item)
        resolved.append({"at": at, "frame": start, "recipe": name, "layers": out_layers})
    return resolved


FLASH_TYPES = {"flash", "invert", "ink", "still"}


def flash_events(resolved: list[dict], fps: Fraction) -> list[float]:
    """Times (s) of planned luminance events that count toward the flash budget."""
    times = []
    for cue in resolved:
        for layer in cue["layers"]:
            if layer["type"] not in FLASH_TYPES:
                continue
            if layer["type"] == "flash" and layer["strength"] < 0.25:
                continue
            times.append(layer["first"] / float(fps))
    return sorted(times)


def max_in_window(times: list[float], window: float = 1.0) -> tuple[int, float]:
    best, best_at, j = 0, 0.0, 0
    for i, t in enumerate(times):
        while times[j] <= t - window:
            j += 1
        if i - j + 1 > best:
            best, best_at = i - j + 1, times[j]
    return best, best_at


# ---------------------------------------------------------------- filtergraph

def _between(var: str, first: int, last: int) -> str:
    return f"between({var},{first},{last})"


def build_graph(resolved: list[dict], fps: Fraction, width: int, height: int,
                image_index: dict[str, int]) -> str:
    rate = f"{fps.numerator}/{fps.denominator}"
    parts = [f"[0:v]fps=fps={rate},setpts=PTS-STARTPTS,format=yuv420p[v0]"]
    counter = 0

    def nxt() -> str:
        nonlocal counter
        counter += 1
        return f"v{counter}"

    cur = "v0"
    layers = [layer for cue in resolved for layer in cue["layers"]]

    # 1) Hit-stop holds (frame count and duration are preserved).
    for layer in (l for l in layers if l["type"] == "hitstop"):
        a, b, out = nxt(), nxt(), nxt()
        parts.append(f"[{cur}]split[{a}][{b}];[{a}][{b}]freezeframes=first={layer['first'] + 1}:"
                     f"last={layer['last']}:replace={layer['first']}[{out}]")
        cur = out

    # 2) Tone hits.
    for layer in layers:
        kind = layer["type"]
        enable = f"enable='{_between('n', layer['first'], layer['last'])}'"
        if kind == "flash":
            filt = f"drawbox=x=0:y=0:w=iw:h=ih:color={layer['color']}@{layer['strength']:.2f}:t=fill:{enable}"
        elif kind == "invert":
            filt = f"negate={enable}"
        elif kind == "ink":
            filt = f"eq=contrast={layer['contrast']:.2f}:brightness=-0.06:saturation=0:{enable}"
        elif kind == "punch":
            filt = f"eq=contrast={layer['contrast']:.2f}:brightness={layer['brightness']:.2f}:saturation=1.02:{enable}"
        elif kind == "rgbsplit":
            k = layer["shift_px"]
            filt = f"rgbashift=rh=-{k}:bh={k}:edge=smear:{enable},format=yuv420p"
        elif kind == "still":
            src = image_index[layer["image"]]
            img, out = nxt(), nxt()
            parts.append(f"[{src}:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
                         f"crop={width}:{height},format=yuv420p[{img}];"
                         f"[{cur}][{img}]overlay=shortest=0:{enable}[{out}]")
            cur = out
            continue
        else:
            continue
        out = nxt()
        parts.append(f"[{cur}]{filt}[{out}]")
        cur = out

    # 3) Camera motion on a branch, composited only on the active frames.
    for layer in layers:
        kind = layer["type"]
        if kind not in ("shake", "zoom"):
            continue
        first, last, length = layer["first"], layer["last"], layer["frames"]
        main, branch, moved, out = nxt(), nxt(), nxt(), nxt()
        if kind == "shake":
            amp = layer["amp_px"]
            decay = f"if({_between('n', first, last)},1-(n-{first})/{length + 1},0)"
            ax = 0 if layer.get("direction") == "v" else amp
            ay = 0 if layer.get("direction") == "h" else amp
            filt = (f"crop=w=iw-{2 * amp}:h=ih-{2 * amp}:"
                    f"x='{amp}+{ax}*sin(n*2.39)*{decay}':y='{amp}+{ay}*cos(n*3.71)*{decay}',"
                    f"scale={width}:{height},setsar=1")
        else:
            peak = layer["zoom"] - 1
            fx, fy = layer["focus"]
            z = f"if({_between('in', first, last)},1+{peak:.4f}*pow(1-(in-{first})/{length + 1},2),1)"
            filt = (f"zoompan=z='{z}':x='max(0,min(iw-iw/zoom,{fx:.4f}*iw-iw/zoom/2))':"
                    f"y='max(0,min(ih-ih/zoom,{fy:.4f}*ih-ih/zoom/2))':d=1:s={width}x{height}:fps={rate},setsar=1")
        parts.append(f"[{cur}]split[{main}][{branch}];[{branch}]{filt}[{moved}];"
                     f"[{main}][{moved}]overlay=shortest=1:enable='{_between('n', first, last)}'[{out}]")
        cur = out

    parts.append(f"[{cur}]format=yuv420p[vout]")
    return ";".join(parts)


# ---------------------------------------------------------------- render

def render(input_file: Path, output: Path, raw_cues: list[dict], image: Path | None = None,
           fps_override: str | None = None, allow_intense: bool = False,
           safety_scan: bool = True) -> dict:
    source = input_file.expanduser().resolve(strict=True)
    destination = output.expanduser().absolute()
    validate_output(source, destination)
    info = read_media(source)
    fps = parse_rate(fps_override) if fps_override else info["fps"]
    resolved = resolve_cues(raw_cues, fps, info["duration"], info["width"], image)

    events = flash_events(resolved, fps)
    peak, peak_at = max_in_window(events) if events else (0, 0.0)
    if peak > 3 and not allow_intense:
        raise FramecraftError(
            f"计划在约 {peak_at:.2f}s 起的 1 秒内放 {peak} 次闪烁类效果，超过每秒 3 次的光敏安全线。"
            "请减少击点、换成 shake/zoom/hitstop/punch 这类非闪烁效果，"
            "或确认用途后加 --allow-intense。")

    images = sorted({layer["image"] for cue in resolved for layer in cue["layers"] if layer["type"] == "still"})
    rate = f"{fps.numerator}/{fps.denominator}"
    ffmpeg = tool("ffmpeg")
    cmd = [ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-n", "-i", str(source)]
    image_index = {}
    for i, img in enumerate(images, 1):
        cmd += ["-loop", "1", "-framerate", rate, "-i", img]
        image_index[img] = i
    graph = build_graph(resolved, fps, info["width"], info["height"], image_index)
    cmd += ["-filter_complex", graph, "-map", "[vout]"]
    if info["has_audio"]:
        cmd += ["-map", "0:a:0?", "-c:a", "aac", "-b:a", "192k"]
    else:
        cmd += ["-an"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "-t", f"{info['duration']:.6f}"]
    temporary = None
    report = None
    try:
        with tempfile.NamedTemporaryFile(prefix=".framecraft-", suffix=".mp4", dir=destination.parent, delete=False) as handle:
            temporary = Path(handle.name)
        temporary.unlink()  # ffmpeg -n refuses any existing target
        cmd.append(str(temporary))
        run_checked(cmd)
        rendered = read_media(temporary)
        if abs(rendered["duration"] - info["duration"]) > max(0.3, 3 / float(fps)):
            raise FramecraftError("输出视频时长与源片偏差过大，已停止发布。")
        if info["has_audio"] and not rendered["has_audio"]:
            raise FramecraftError("原视频包含音轨但输出没有音轨，已停止发布。")
        if safety_scan:
            report = flash_scan(temporary)
        safe_publish(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    result = {
        "output": str(destination), "fps": rate, "duration": info["duration"],
        "has_audio": info["has_audio"], "cfr_conversion": info["variable_rate_possible"],
        "planned_flashes_peak_per_second": peak, "cues": resolved,
    }
    if resolved and len(resolved) == 1 and resolved[0]["layers"]:
        first = resolved[0]["layers"]
        result["frame_start"] = min(l["first"] for l in first)
        result["frame_end"] = max(l["last"] for l in first)
    if report is not None:
        result["safety_scan"] = report
    return result


def apply(input_file: Path, output: Path, at: float, frames: int, style: str,
          image: Path | None = None, fps_override: str | None = None) -> dict:
    """Backward compatible single-style entry point (1.x API)."""
    if style not in LEGACY_STYLES:
        raise FramecraftError(f"样式必须是：{', '.join(LEGACY_STYLES)}")
    if style == "still":
        if not image or not Path(image).expanduser().is_file():
            raise FramecraftError("选择 still（插入冲击图）时必须提供有效的 --image PNG/JPEG 路径。")
    elif image:
        raise FramecraftError("只有 still 模式需要 --image；其他模式请移除图片参数。")
    if not isinstance(frames, int) or frames < 1:
        raise FramecraftError("持续帧数必须是至少 1 的整数。")
    source = input_file.expanduser().resolve(strict=True)
    info = read_media(source)
    fps = parse_rate(fps_override) if fps_override else info["fps"]
    plan_frames(at, frames, fps, info["duration"])
    result = render(input_file, output, [{"at": at, "layers": legacy_layers(style, frames), "recipe": style}],
                    image=image, fps_override=fps_override, allow_intense=False, safety_scan=False)
    result["style"] = style
    return result


# ---------------------------------------------------------------- analysis

def frame_stats(source: Path) -> list[dict]:
    """Per-frame luma average and frame-to-frame difference via signalstats."""
    result = subprocess.run(
        [tool("ffmpeg"), "-hide_banner", "-nostdin", "-loglevel", "info", "-i", str(source),
         "-vf", "signalstats,metadata=mode=print", "-an", "-f", "null", "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode:
        tail = "\n".join(result.stderr.strip().splitlines()[-10:])
        raise FramecraftError(f"分析失败。\n{tail}")
    frames: list[dict] = []
    current: dict | None = None
    for line in result.stderr.splitlines():
        m = re.search(r"frame:\s*(\d+)\s+pts:\s*\S+\s+pts_time:\s*([-\d.]+)", line)
        if m:
            current = {"n": int(m.group(1)), "t": float(m.group(2))}
            frames.append(current)
            continue
        if current is None:
            continue
        m = re.search(r"lavfi\.signalstats\.(YAVG|YDIF)=([-\d.]+)", line)
        if m:
            current[m.group(1)] = float(m.group(2))
    frames = [f for f in frames if "YAVG" in f]
    if not frames:
        raise FramecraftError("没有读到任何画面统计数据。")
    return frames


def _luminance(yavg: float) -> float:
    v = min(1.0, max(0.0, (yavg - 16) / 219))
    return v ** 2.2


def flash_scan(source: Path) -> dict:
    """Approximate WCAG 2.3.1-style general-flash count on the full frame."""
    stats = frame_stats(source)
    lum = [(_luminance(f["YAVG"]), f["t"]) for f in stats]
    pivots = [lum[0]]
    trend = 0
    ext = lum[0]
    for value in lum[1:]:
        x = value[0]
        if trend == 0:
            if x - ext[0] >= 0.1:
                trend, ext = 1, value
            elif ext[0] - x >= 0.1:
                trend, ext = -1, value
        elif trend == 1:
            if x > ext[0]:
                ext = value
            elif ext[0] - x >= 0.1:
                pivots.append(ext)
                trend, ext = -1, value
        else:
            if x < ext[0]:
                ext = value
            elif x - ext[0] >= 0.1:
                pivots.append(ext)
                trend, ext = 1, value
    if trend:
        pivots.append(ext)
    transitions = []
    for (a, _), (b, tb) in zip(pivots, pivots[1:]):
        if abs(a - b) >= 0.1 and min(a, b) < 0.8:
            transitions.append(tb)
    peak, at = max_in_window(transitions) if transitions else (0, 0.0)
    flashes = peak // 2
    return {
        "max_flashes_per_second": flashes,
        "worst_window_start": round(at, 3),
        "verdict": "risk" if flashes > 3 else "pass",
        "note": "全画面平均亮度的近似检测；未计算闪烁面积与红闪，不能替代专业 PSE/Harding 检测。",
    }


def detect_hits(source: Path, top: int = 8, min_gap: float = 0.3) -> list[dict]:
    """Rank sudden visual changes; good starting points for locating a hit."""
    stats = frame_stats(source)
    diffs = [f.get("YDIF", 0.0) for f in stats]
    if len(diffs) < 3:
        return []
    mean = sum(diffs) / len(diffs)
    std = (sum((d - mean) ** 2 for d in diffs) / len(diffs)) ** 0.5
    threshold = mean + 1.5 * std
    peaks = []
    for i in range(1, len(diffs) - 1):
        d = diffs[i]
        if d >= threshold and d >= diffs[i - 1] and d >= diffs[i + 1] and d > 1.0:
            peaks.append((d, i))
    peaks.sort(reverse=True)
    chosen: list[tuple[float, int]] = []
    for d, i in peaks:
        t = stats[i]["t"]
        if all(abs(t - stats[j]["t"]) >= min_gap for _, j in chosen):
            chosen.append((d, i))
        if len(chosen) >= top:
            break
    chosen.sort(key=lambda item: stats[item[1]]["t"])
    return [{"time": round(stats[i]["t"], 3), "frame": stats[i]["n"], "change": round(d, 2),
             "hint": "画面突变点：可能是命中、闪光或剪辑点，请用 sheet 复查"} for d, i in chosen]


def contact_sheet(source: Path, at: float, output: Path, span: int = 4, fps_override: str | None = None) -> dict:
    source = source.expanduser().resolve(strict=True)
    destination = output.expanduser().absolute()
    validate_output(source, destination, ".png")
    info = read_media(source)
    fps = parse_rate(fps_override) if fps_override else info["fps"]
    if not isinstance(span, int) or not (1 <= span <= 8):
        raise FramecraftError("span 必须是 1–8 的整数。")
    total = total_frames(info["duration"], fps)
    center = math.floor(at * float(fps) + 0.5)
    if not math.isfinite(at) or at < 0 or center >= total:
        raise FramecraftError("时间必须在视频范围内。")
    first, last = max(0, center - span), min(total - 1, center + span)
    count = last - first + 1
    rate = f"{fps.numerator}/{fps.denominator}"
    temporary = destination.with_name(f".framecraft-sheet-{os.getpid()}.png")
    if temporary.exists():
        raise FramecraftError("临时文件冲突，请重试。")
    try:
        run_checked([tool("ffmpeg"), "-hide_banner", "-loglevel", "error", "-nostdin", "-i", str(source),
                     "-vf", f"fps=fps={rate},setpts=PTS-STARTPTS,select='between(n,{first},{last})',"
                     f"scale=320:-2,tile={count}x1:padding=4:color=black",
                     "-frames:v", "1", "-n", str(temporary)])
        safe_publish(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    return {"output": str(destination), "frames": list(range(first, last + 1)), "hit_frame": center,
            "note": "从左到右依次是这些帧号；中间那格对应你给的秒数。"}


def preview(source: Path, at: float, folder: Path) -> list[str]:
    source = source.expanduser().resolve(strict=True)
    info = read_media(source)
    if not math.isfinite(at) or at < 0 or at >= info["duration"]:
        raise FramecraftError("预览时间必须在视频范围内。")
    folder = folder.expanduser().absolute()
    if folder.is_symlink():
        raise FramecraftError("预览文件夹不应为符号链接。")
    if not folder.exists():
        folder.mkdir(parents=True)
    elif not folder.is_dir():
        raise FramecraftError("预览输出路径不是文件夹。")
    stamps = [max(0.0, at - 1 / float(info["fps"])), at,
              min(info["duration"] - 0.001, at + 1 / float(info["fps"]))]
    paths = [folder / f"{i:02d}-{label}.png" for i, label in enumerate(("before", "hit", "after"), 1)]
    if any(p.exists() or p.is_symlink() for p in paths):
        raise FramecraftError("预览图片文件已存在；请换一个新文件夹以避免覆盖。")
    for p, t in zip(paths, stamps):
        run_checked([tool("ffmpeg"), "-hide_banner", "-loglevel", "error", "-nostdin",
                     "-ss", f"{t:.6f}", "-i", str(source), "-frames:v", "1", "-n", str(p)])
    return [str(p) for p in paths]


# ---------------------------------------------------------------- CLI

def load_cues(path: Path) -> list[dict]:
    try:
        data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FramecraftError(f"读取击点文件失败：{exc}") from exc
    cues = data.get("cues") if isinstance(data, dict) else data
    if not isinstance(cues, list):
        raise FramecraftError("击点文件应是列表，或含 cues 列表的对象。")
    return cues


def parse_times(text: str) -> list[float]:
    try:
        return [float(x) for x in str(text).replace("，", ",").split(",") if x.strip()]
    except ValueError as exc:
        raise FramecraftError("--at 应为秒数，多个击点用逗号分隔，例如 1.2,2.65") from exc


def _print(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2,
                     default=lambda v: str(v) if isinstance(v, Fraction) else v))


def menu() -> None:
    print("\n=== 冲击帧导演 2.1 · 视频处理 ===")
    print("1. 看视频信息      2. 给击点加冲击效果     3. 击点前后连帧图")
    print("4. 自动找候选击点  5. 光敏闪烁安全检查")
    option = input("请选择数字（1-5）：").strip()
    if option not in {"1", "2", "3", "4", "5"}:
        raise FramecraftError("请输入 1 到 5。")
    src = Path(input("请输入视频文件路径（可粘贴完整路径）：").strip().strip('"'))
    if option == "1":
        _print(read_media(src))
        return
    if option == "4":
        _print(detect_hits(src))
        return
    if option == "5":
        _print(flash_scan(src))
        return
    times = parse_times(input("击点秒数（多个用逗号分隔，例如 1.2,2.65）：").strip())
    if option == "3":
        suggested = src.with_name(src.stem + f"-sheet-{times[0]:.2f}.png")
        out = input(f"连帧图保存路径（直接回车={suggested}）：").strip().strip('"') or str(suggested)
        _print(contact_sheet(src, times[0], Path(out)))
        return
    names = list(RECIPES) + ["still"]
    for i, name in enumerate(names, 1):
        label = RECIPES[name]["label"] if name in RECIPES else "替换为自己画的冲击图"
        print(f"{i}. {name:9s} {label}")
    pick = input("选择效果数字（直接回车=2 重击）：").strip() or "2"
    if not pick.isdigit() or not (1 <= int(pick) <= len(names)):
        raise FramecraftError("无效的效果数字。")
    name = names[int(pick) - 1]
    image = None
    if name == "still":
        image = Path(input("输入冲击图 PNG/JPG 路径：").strip().strip('"'))
        frames = int(input("覆盖多少帧（直接回车=2）：").strip() or "2")
        cues = [{"at": t, "recipe": "still", "layers": [{"type": "still", "frames": frames}]} for t in times]
    else:
        cues = [{"at": t, "recipe": name} for t in times]
    suggested = src.with_name(src.stem + "-impact.mp4")
    output = Path(input(f"输出新视频路径（直接回车={suggested}）：").strip().strip('"') or str(suggested))
    _print(render(src, output, cues, image=image))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="冲击帧导演 2.1：按帧精准添加冲击效果（不覆盖源片）")
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("inspect", help="查看视频帧率、时长与音轨")
    p.add_argument("--input", required=True, type=Path)

    p = sub.add_parser("recipes", help="列出全部效果配方")

    p = sub.add_parser("apply", help="渲染击点效果")
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--at", help="击点秒数；多个用逗号分隔")
    p.add_argument("--recipe", choices=sorted(RECIPES), help="效果配方（默认 heavy）")
    p.add_argument("--style", choices=LEGACY_STYLES, help="单一效果（兼容 1.x）")
    p.add_argument("--frames", type=int, default=2, help="--style 的持续帧数")
    p.add_argument("--image", type=Path, help="still 用的冲击图")
    p.add_argument("--cues", type=Path, help="多击点 JSON 文件")
    p.add_argument("--focus", help="推近焦点 x,y（0–1 比例），例如 0.62,0.40")
    p.add_argument("--fps", help="可选：指定输出恒定帧率，例如 24 或 30000/1001")
    p.add_argument("--allow-intense", action="store_true", help="允许超过每秒 3 次的闪烁类效果")
    p.add_argument("--no-scan", action="store_true", help="跳过输出后的闪烁安全扫描")

    p = sub.add_parser("sheet", help="导出击点前后连帧图（PNG）")
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--at", required=True, type=float)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--span", type=int, default=4, help="击点前后各几帧（1–8）")

    p = sub.add_parser("detect", help="自动列出候选击点（画面突变）")
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--top", type=int, default=8)

    p = sub.add_parser("safety", help="光敏闪烁近似检查")
    p.add_argument("--input", required=True, type=Path)

    p = sub.add_parser("preview", help="导出击点前、中、后三张截图")
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--at", required=True, type=float)
    p.add_argument("--folder", required=True, type=Path)

    sub.add_parser("menu", help="中文数字菜单（小白推荐）")
    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            _print(read_media(args.input))
        elif args.command == "recipes":
            _print({name: r["label"] for name, r in RECIPES.items()})
        elif args.command == "apply":
            if args.cues:
                if args.at or args.recipe or args.style:
                    raise FramecraftError("使用 --cues 时不要再给 --at/--recipe/--style。")
                cues = load_cues(args.cues)
            else:
                if not args.at:
                    raise FramecraftError("请给出 --at 击点秒数，或使用 --cues。")
                if args.recipe and args.style:
                    raise FramecraftError("--recipe 与 --style 二选一。")
                times = parse_times(args.at)
                if args.style:
                    if args.style == "still" and not args.image:
                        raise FramecraftError("still 必须带 --image。")
                    if args.style != "still" and args.image:
                        raise FramecraftError("只有 still 需要 --image。")
                    if args.frames < 1:
                        raise FramecraftError("--frames 至少为 1。")
                    cues = [{"at": t, "recipe": args.style, "layers": legacy_layers(args.style, args.frames)}
                            for t in times]
                else:
                    cues = [{"at": t, "recipe": args.recipe or "heavy"} for t in times]
                if args.focus:
                    for cue in cues:
                        cue["focus"] = args.focus
            _print(render(args.input, args.output, cues, image=args.image, fps_override=args.fps,
                          allow_intense=args.allow_intense, safety_scan=not args.no_scan))
        elif args.command == "sheet":
            _print(contact_sheet(args.input, args.at, args.output, args.span))
        elif args.command == "detect":
            _print(detect_hits(args.input.expanduser().resolve(strict=True), args.top))
        elif args.command == "safety":
            _print(flash_scan(args.input.expanduser().resolve(strict=True)))
        elif args.command == "preview":
            print("\n".join(preview(args.input, args.at, args.folder)))
        else:
            menu()
        return 0
    except (FramecraftError, FileNotFoundError, PermissionError, ValueError) as exc:
        print(f"操作未完成：{exc}", file=sys.stderr)
        return 2
    except (KeyboardInterrupt, EOFError):
        print("已取消，原文件未改变。", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
