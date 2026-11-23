#!/usr/bin/env python3
"""Build and verify display-referred creative RGB .cube LUTs (NumPy + FFmpeg).

The neutral default is identity. This is not a camera Log/HDR transform, a colour
space converter, a learned match, or a spatial/semantic image operation.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np

W = np.array([0.2126, 0.7152, 0.0722], dtype=np.float64)
DEFAULT_RECIPE = {
    "schema_version": 1,
    "working_space": "Rec709",
    "description": "Neutral identity; edit only after inspecting reference and target frames.",
    "curve": [[0.0, 0.0], [1.0, 1.0]],
    "gain": [1.0, 1.0, 1.0],
    "offset": [0.0, 0.0, 0.0],
    "saturation": 1.0,
    "hue_selections": [],
    "tints": {"shadows": [0.0, 0.0, 0.0], "midtones": [0.0, 0.0, 0.0],
              "highlights": [0.0, 0.0, 0.0]},
    "near_black": {"start": 0.0, "end": 0.06, "amount": 1.0},
    "skin_protection": {"amount": 0.0, "center": 35.0, "width": 30.0},
    "strength": 1.0,
}


def _object(value, keys, label):
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    unknown = set(value) - set(keys)
    if unknown:
        raise ValueError(f"{label}: unknown keys: {sorted(unknown)}")


def _number(value, low, high, label):
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise ValueError(f"{label} must be a number")
    if not low <= value <= high or not math.isfinite(value):
        raise ValueError(f"{label} must be finite and in [{low}, {high}]")


def _vector(value, low, high, label):
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{label} must be a three-number RGB list")
    for i, v in enumerate(value):
        _number(v, low, high, f"{label}[{i}]")


def normalize_recipe(value):
    """Validate strict schema; return a full copy with defaults for omitted controls."""
    _object(value, DEFAULT_RECIPE, "recipe")
    if type(value.get("schema_version")) is not int or value["schema_version"] != 1:
        raise ValueError("schema_version must be integer 1")
    if value.get("working_space") not in ("Rec709", "sRGB"):
        raise ValueError("working_space must explicitly be Rec709 or sRGB")
    result = copy.deepcopy(DEFAULT_RECIPE)
    for k, v in value.items():
        if k in ("tints", "near_black", "skin_protection"):
            _object(v, DEFAULT_RECIPE[k], k)
            result[k].update(copy.deepcopy(v))
        else:
            result[k] = copy.deepcopy(v)
    if not isinstance(result["description"], str) or len(result["description"]) > 2000:
        raise ValueError("description must be a string of at most 2000 characters")
    curve = result["curve"]
    if not isinstance(curve, list) or not 2 <= len(curve) <= 32:
        raise ValueError("curve must contain 2..32 [input, output] knots")
    for i, point in enumerate(curve):
        if not isinstance(point, list) or len(point) != 2:
            raise ValueError(f"curve[{i}] must be [input, output]")
        for j, v in enumerate(point):
            _number(v, 0, 1, f"curve[{i}][{j}]")
    if curve[0][0] != 0 or curve[-1][0] != 1:
        raise ValueError("curve input domain must start at 0 and end at 1")
    if any(b[0] - a[0] < 1e-5 or b[1] < a[1] for a, b in zip(curve, curve[1:])):
        raise ValueError("curve inputs must strictly increase (gap >= 1e-5); outputs must not decrease")
    if curve[-1][1] - curve[0][1] < 0.1:
        raise ValueError("curve output range must span at least 0.1; a flat/collapsed LUT is rejected")
    _vector(result["gain"], 0.25, 4, "gain")
    _vector(result["offset"], -0.25, 0.25, "offset")
    _number(result["saturation"], 0, 2, "saturation")
    _number(result["strength"], 0, 1, "strength")
    selections = result["hue_selections"]
    if not isinstance(selections, list) or len(selections) > 12:
        raise ValueError("hue_selections must be a list of at most 12 selections")
    for i, sel in enumerate(selections):
        label = f"hue_selections[{i}]"
        _object(sel, ("center", "width", "hue_shift", "saturation"), label)
        if "center" not in sel or "width" not in sel:
            raise ValueError(f"{label} requires center and width in degrees")
        sel.setdefault("hue_shift", 0.0)
        sel.setdefault("saturation", 1.0)
        for key, lo, hi in (("center", 0, 360), ("width", 5, 180),
                            ("hue_shift", -90, 90), ("saturation", 0, 2)):
            _number(sel[key], lo, hi, f"{label}.{key}")
    for key, tint in result["tints"].items():
        _vector(tint, -0.2, 0.2, f"tints.{key}")
    black = result["near_black"]
    _number(black["start"], 0, 0.1, "near_black.start")
    _number(black["end"], 0.005, 0.25, "near_black.end")
    _number(black["amount"], 0, 1, "near_black.amount")
    if black["end"] - black["start"] < 0.005:
        raise ValueError("near_black.end must exceed start by at least 0.005")
    skin = result["skin_protection"]
    for key, lo, hi in (("amount", 0, 1), ("center", 0, 360), ("width", 5, 90)):
        _number(skin[key], lo, hi, f"skin_protection.{key}")
    return result


def load_recipe(path):
    def no_duplicate(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    with Path(path).open(encoding="utf-8-sig") as f:
        return normalize_recipe(json.load(f, object_pairs_hook=no_duplicate))


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def pchip(x, knots):
    """Fritsch-Carlson/PCHIP-style shape preserving cubic interpolation, no SciPy."""
    points = np.asarray(knots, dtype=np.float64)
    xp, fp = points[:, 0], points[:, 1]
    h = np.diff(xp)
    d = np.diff(fp) / h
    m = np.zeros(len(xp))
    if len(xp) == 2:
        m[:] = d[0]
    else:
        for k in range(1, len(xp) - 1):
            if d[k - 1] * d[k] > 0:
                w1, w2 = 2 * h[k] + h[k - 1], h[k] + 2 * h[k - 1]
                m[k] = (w1 + w2) / (w1 / d[k - 1] + w2 / d[k])
        for k, hn, hp, dn, dp in ((0, h[0], h[1], d[0], d[1]),
                                  (-1, h[-1], h[-2], d[-1], d[-2])):
            z = ((2 * hn + hp) * dn - hn * dp) / (hn + hp)
            m[k] = 0 if z * dn <= 0 else min(abs(z), 3 * abs(dn)) * np.sign(z)
    i = np.clip(np.searchsorted(xp, x, side="right") - 1, 0, len(xp) - 2)
    t = np.clip((x - xp[i]) / h[i], 0, 1)
    return ((2*t**3 - 3*t**2 + 1)*fp[i] + (t**3 - 2*t**2 + t)*h[i]*m[i]
            + (-2*t**3 + 3*t**2)*fp[i+1] + (t**3 - t**2)*h[i]*m[i+1])


def rgb_hsv(rgb):
    mx, mn = rgb.max(-1), rgb.min(-1)
    delta = mx - mn
    den = np.maximum(delta, 1e-12)
    hue = np.zeros_like(mx)
    for k in (2, 1, 0):
        v = ((rgb[..., 1] - rgb[..., 2]) / den if k == 0 else
             (rgb[..., 2] - rgb[..., 0]) / den + 2 if k == 1 else
             (rgb[..., 0] - rgb[..., 1]) / den + 4)
        hue = np.where((delta > 1e-12) & (rgb[..., k] == mx), v, hue)
    return (hue / 6) % 1, delta / np.maximum(mx, 1e-12), mx


def hsv_rgb(h, s, v):
    k = (h[..., None] * 6 + np.array([0, 4, 2])) % 6
    base = np.clip(np.abs(k - 3) - 1, 0, 1)
    return v[..., None] * (1 - s[..., None] + s[..., None] * base)


def hue_weight(h, center, width):
    distance = np.abs((h * 360 - center + 180) % 360 - 180)
    return 1 - smoothstep(0, width, distance)


def gamut_compress(rgb):
    """Project out-of-gamut chroma toward its luma anchor, not per-channel clipping."""
    y = np.clip(rgb @ W, 0, 1)
    c = rgb - (rgb @ W)[..., None]
    lower = np.where(c < 0, y[..., None] / np.maximum(-c, 1e-12), 1e12).min(-1)
    upper = np.where(c > 0, (1-y[..., None]) / np.maximum(c, 1e-12), 1e12).min(-1)
    factor = np.clip(np.minimum(lower, upper), 0, 1)
    return np.clip(y[..., None] + c * factor[..., None], 0, 1)


def grade(rgb, recipe):
    """Apply a previously validated recipe to RGB (...,3), encoded samples 0..1."""
    rgb = np.asarray(rgb, dtype=np.float64)
    if rgb.shape[-1:] != (3,) or not np.isfinite(rgb).all():
        raise ValueError("RGB input must be finite with final dimension 3")
    if rgb.min() < -1e-9 or rgb.max() > 1 + 1e-9:
        raise ValueError("RGB input must be display-referred values in 0..1")
    rgb = np.clip(rgb, 0, 1)
    balanced = gamut_compress(rgb * np.asarray(recipe["gain"]) + np.asarray(recipe["offset"]))
    y = balanced @ W
    tone = pchip(y, recipe["curve"])
    h, s, v = rgb_hsv(balanced)
    shift, sat = np.zeros_like(h), np.ones_like(h)
    for selection in recipe["hue_selections"]:
        weight = hue_weight(h, selection["center"], selection["width"]) * smoothstep(.04, .25, s)
        shift += weight * selection["hue_shift"] / 360
        sat *= 1 + weight * (selection["saturation"] - 1)
    shifted = hsv_rgb((h + shift) % 1, s, v)
    chroma = shifted - (shifted @ W)[..., None]
    chroma *= (sat * recipe["saturation"] * tone / np.maximum(y, 1e-12))[..., None]
    shadow_weight = 1 - smoothstep(.15, .5, y)
    highlight_weight = smoothstep(.5, .85, y)
    mid_weight = 1 - shadow_weight - highlight_weight
    tint = (shadow_weight[..., None] * np.asarray(recipe["tints"]["shadows"])
            + mid_weight[..., None] * np.asarray(recipe["tints"]["midtones"])
            + highlight_weight[..., None] * np.asarray(recipe["tints"]["highlights"]))
    tint -= (tint @ W)[..., None]
    result = tone[..., None] + chroma + tint
    original_y = rgb @ W
    baseline = tone[..., None] + (rgb-original_y[..., None]) * (tone/np.maximum(original_y, 1e-12))[..., None]
    nb = recipe["near_black"]
    color_amount = 1 - nb["amount"] * (1-smoothstep(nb["start"], nb["end"], original_y))
    skin = recipe["skin_protection"]
    oh, os, _ = rgb_hsv(rgb)
    skin_mask = (hue_weight(oh, skin["center"], skin["width"])
                 * smoothstep(.06, .22, os) * (1-smoothstep(.65, .95, os)))
    color_amount *= 1 - skin["amount"] * skin_mask
    result = gamut_compress(baseline + (result-baseline)*color_amount[..., None])
    return np.clip(rgb + recipe["strength"] * (result-rgb), 0, 1)


def _ensure_new(path, overwrite):
    path = Path(path)
    if path.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite {path}; use --overwrite intentionally")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _protect_inputs(output, inputs):
    resolved = Path(output).resolve()
    for source in inputs:
        source_path = Path(source).resolve()
        if resolved == source_path or (resolved.exists() and source_path.exists() and resolved.samefile(source_path)):
            raise ValueError(f"Output cannot replace an input file, even with --overwrite: {output}")


def write_cube(recipe, size, path, overwrite=False):
    recipe = normalize_recipe(recipe)
    if size not in (33, 65):
        raise ValueError("Only 33 and 65 lattice sizes are supported")
    path = _ensure_new(path, overwrite)
    axis = np.linspace(0, 1, size)
    bb, gg, rr = np.meshgrid(axis, axis, axis, indexing="ij")
    output = grade(np.stack([rr, gg, bb], -1), recipe).reshape(-1, 3)
    with path.open("w" if overwrite else "x", encoding="ascii", newline="\n") as f:
        f.write("# Creative display-referred RGB LUT. No Log/HDR/transfer conversion.\n")
        f.write(f"# Working space: {recipe['working_space']}. Domain 0..1. Red varies fastest.\n")
        f.write(f'TITLE "Creative {recipe["working_space"]} {size}"\nLUT_3D_SIZE {size}\n')
        f.write("DOMAIN_MIN 0.0 0.0 0.0\nDOMAIN_MAX 1.0 1.0 1.0\n")
        np.savetxt(f, output, fmt="%.9f")
    return path


def read_cube(path):
    rows, header = [], {}
    for index, raw in enumerate(Path(path).read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        key = line.split()[0]
        if key == "TITLE":
            continue
        if key in ("LUT_3D_SIZE", "DOMAIN_MIN", "DOMAIN_MAX"):
            if key in header:
                raise ValueError(f"Repeated .cube directive: {key}")
            header[key] = line.split()[1:]
        else:
            try:
                values = [float(v) for v in line.split()]
            except ValueError as e:
                raise ValueError(f"Unknown or malformed .cube line {index}") from e
            if len(values) != 3:
                raise ValueError(f"Expected three .cube samples at line {index}")
            rows.append(values)
    size_header = header.get("LUT_3D_SIZE", [])
    if len(size_header) != 1 or size_header[0] not in ("33", "65"):
        raise ValueError(".cube must declare one LUT_3D_SIZE of 33 or 65")
    size = int(size_header[0])
    for key, default in (("DOMAIN_MIN", [0, 0, 0]), ("DOMAIN_MAX", [1, 1, 1])):
        if [float(x) for x in header.get(key, default)] != default:
            raise ValueError(f"{key} must be {default}")
    data = np.asarray(rows, dtype=np.float64)
    if data.shape != (size**3, 3) or not np.isfinite(data).all():
        raise ValueError(".cube must contain exactly size^3 finite RGB entries")
    if data.min() < 0 or data.max() > 1:
        raise ValueError(".cube output entries must be in 0..1")
    return size, data


def validate_lut(recipe, cube_path, ffmpeg="ffmpeg", seed=20260928,
                 max_mae8=.35, max_p99_8=1.5, max_error8=12):
    recipe = normalize_recipe(recipe)
    cube_path = Path(cube_path).resolve()
    size, data = read_cube(cube_path)
    executable = shutil.which(ffmpeg)
    if not executable:
        raise FileNotFoundError("FFmpeg not found; add it to PATH or pass --ffmpeg /path/to/ffmpeg")
    random_count, ramp_count = 65536, 4096
    random = np.random.default_rng(seed).random((random_count, 3))
    ramp = np.repeat(np.linspace(0, 1, ramp_count)[:, None], 3, axis=1)
    # gbrpf32le avoids lossy RGB/YUV conversions and 8-bit quantization in the test.
    frame = np.vstack([random, ramp]).reshape(68, 1024, 3).astype("<f4")
    packed = frame[..., [1, 2, 0]].transpose(2, 0, 1).copy().tobytes()
    with tempfile.TemporaryDirectory(prefix="lut-verify-") as tmp:
        shutil.copyfile(cube_path, Path(tmp)/"check.cube")
        command = [executable, "-hide_banner", "-loglevel", "error", "-f", "rawvideo",
                   "-pixel_format", "gbrpf32le", "-video_size", "1024x68", "-i", "pipe:0",
                   "-vf", "lut3d=file=check.cube:interp=tetrahedral", "-frames:v", "1",
                   "-pix_fmt", "gbrpf32le", "-f", "rawvideo", "pipe:1"]
        process = subprocess.run(command, input=packed, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, cwd=tmp, check=False)
    if process.returncode:
        raise RuntimeError("FFmpeg LUT validation failed: " + process.stderr.decode("utf-8", errors="replace")[-4000:])
    if len(process.stdout) != len(packed):
        raise RuntimeError("FFmpeg returned an unexpected frame byte count")
    actual = np.frombuffer(process.stdout, dtype="<f4").reshape(3, 68, 1024).transpose(1, 2, 0)[..., [2, 0, 1]].reshape(-1, 3)
    expected = grade(frame, recipe).reshape(-1, 3)
    error = np.abs(actual[:random_count]-expected[:random_count])*255
    ramp_actual = actual[random_count:].astype(np.float64)
    ramp_expected = expected[random_count:]
    luma_diffs = np.diff(ramp_actual @ W)
    channel_diffs = np.diff(ramp_actual, axis=0)
    mae, p99, max_error = float(error.mean()), float(np.quantile(error, .99)), float(error.max())
    finite = bool(np.isfinite(actual).all())
    in_bounds = finite and bool(actual.min() >= -1e-6 and actual.max() <= 1+1e-6)
    monotonic = bool((luma_diffs >= -2e-6).all())
    passed = finite and in_bounds and monotonic and mae <= max_mae8 and p99 <= max_p99_8 and max_error <= max_error8
    return {
        "passed": passed, "method": "Actual .cube loaded by FFmpeg lut3d; tetrahedral; planar float RGB",
        "working_space": recipe["working_space"], "lut": str(cube_path), "size": size,
        "entries": len(data), "sha256": hashlib.sha256(cube_path.read_bytes()).hexdigest(),
        "recipe_normalized_sha256": hashlib.sha256(json.dumps(recipe, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "lattice_bounds": [float(data.min()), float(data.max())],
        "rendered_bounds": [float(actual.min()), float(actual.max())],
        "rendered_finite": finite, "rendered_in_bounds": in_bounds,
        "random_samples": random_count, "seed": seed,
        "interpolation_error_8bit_units": {"mean": mae, "p99": p99, "max": max_error},
        "thresholds_8bit_units": {"mean": max_mae8, "p99": max_p99_8, "max": max_error8},
        "gray_ramp": {"samples": ramp_count, "luma_monotonic": monotonic,
                      "minimum_luma_step": float(luma_diffs.min()),
                      "rgb_monotonic_diagnostic": [bool(x) for x in (channel_diffs >= -2e-6).all(axis=0)],
                      "maximum_error_8bit_units": float(np.abs(ramp_actual-ramp_expected).max()*255),
                      "black_rgb": ramp_actual[0].tolist(), "white_rgb": ramp_actual[-1].tolist()},
        "limitations": "Numerical format/interpolation checks do not establish an aesthetic match. Inspect rendered target frames and gradients; hue-dependent channel curves need not each be monotonic."
    }


def _write_json(path, value, overwrite=False):
    path = _ensure_new(path, overwrite)
    with path.open("w" if overwrite else "x", encoding="utf-8", newline="\n") as f:
        json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="Write a neutral identity recipe")
    init.add_argument("--out", required=True)
    init.add_argument("--working-space", choices=("Rec709", "sRGB"), default="Rec709")
    build = sub.add_parser("build", help="Bake .cube files (red-fastest)")
    build.add_argument("--recipe", required=True)
    build.add_argument("--out-dir", required=True)
    build.add_argument("--name", required=True)
    build.add_argument("--sizes", nargs="+", type=int, choices=(33, 65), default=[33, 65])
    validate = sub.add_parser("validate", help="Load the actual .cube in FFmpeg and verify it")
    validate.add_argument("--recipe", required=True)
    validate.add_argument("--lut", required=True)
    validate.add_argument("--report", required=True)
    validate.add_argument("--ffmpeg", default="ffmpeg")
    validate.add_argument("--max-mae8", type=float, default=.35)
    validate.add_argument("--max-p99-8", type=float, default=1.5)
    validate.add_argument("--max-error8", type=float, default=12)
    for command in (init, build, validate):
        command.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "init":
            recipe = copy.deepcopy(DEFAULT_RECIPE)
            recipe["working_space"] = args.working_space
            _write_json(args.out, recipe, args.overwrite)
            print(json.dumps({"recipe": str(Path(args.out).resolve())}))
        elif args.command == "build":
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,99}", args.name) or args.name.endswith("."):
                raise ValueError("--name must be a simple ASCII filename stem, 1..100 characters")
            if args.name.split(".")[0].upper() in {"CON", "PRN", "AUX", "NUL", *[f"COM{i}" for i in range(1, 10)], *[f"LPT{i}" for i in range(1, 10)]}:
                raise ValueError("--name is a reserved Windows device name")
            recipe = load_recipe(args.recipe)
            paths = [Path(args.out_dir)/f"{args.name}_{size}.cube" for size in dict.fromkeys(args.sizes)]
            for path in paths:
                _protect_inputs(path, [args.recipe])
                if path.exists() and not args.overwrite:
                    raise FileExistsError(f"Refusing to overwrite {path}; use --overwrite intentionally")
            for size, path in zip(dict.fromkeys(args.sizes), paths):
                write_cube(recipe, size, path, args.overwrite)
            print(json.dumps({"luts": [str(p.resolve()) for p in paths]}))
        else:
            _protect_inputs(args.report, [args.recipe, args.lut])
            _ensure_new(args.report, args.overwrite)
            for value in (args.max_mae8, args.max_p99_8, args.max_error8):
                _number(value, 0, 255, "validation threshold")
            report = validate_lut(load_recipe(args.recipe), args.lut, args.ffmpeg,
                                  max_mae8=args.max_mae8, max_p99_8=args.max_p99_8, max_error8=args.max_error8)
            _write_json(args.report, report, args.overwrite)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 0 if report["passed"] else 2
        return 0
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
