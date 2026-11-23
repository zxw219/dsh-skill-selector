#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path


PRESETS = {
    "ai-media-tech": ["AI", "影像", "科技"],
    "business-markets": ["商业", "财经", "公司"],
    "creator-growth": ["内容创作", "平台趋势", "品牌营销"],
    "product-builder": ["AI 产品", "开发工具", "开源项目"],
    "world-brief": ["国际", "政策", "经济"],
    "consumer-digital": ["消费电子", "互联网产品", "生活方式"],
}


def state_dir() -> Path:
    override = os.environ.get("SIGNAL_RADAR_HOME")
    return Path(override).expanduser() if override else Path.home() / ".codex" / "state" / "track-cross-platform-hotspots"


def profile_path() -> Path:
    return state_dir() / "profile.json"


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return list(dict.fromkeys(part.strip() for part in value.replace("，", ",").split(",") if part.strip()))


def parse_weights(value: str | None) -> dict[str, float]:
    result = {}
    for part in split_csv(value):
        if "=" not in part:
            raise ValueError(f"weight must use name=value: {part}")
        name, raw = (x.strip() for x in part.split("=", 1))
        weight = float(raw)
        if not name or not 0.1 <= weight <= 2.0:
            raise ValueError(f"invalid direction weight: {part}")
        result[name.casefold()] = weight
    return result


def base_profile(directions: list[str]) -> dict:
    return {
        "version": 1,
        "directions": [{"name": name, "weight": 1.0} for name in directions],
        "languages": ["zh", "en"],
        "region": "global",
        "exclusions": [],
        "window_hours": 24,
    }


def validate(profile: dict) -> dict:
    directions = profile.get("directions")
    if not isinstance(directions, list) or not directions:
        raise ValueError("profile requires at least one direction")
    seen = set()
    cleaned = []
    for item in directions:
        if isinstance(item, str):
            item = {"name": item, "weight": 1.0}
        name = str(item.get("name", "")).strip()
        weight = float(item.get("weight", 1.0))
        key = name.casefold()
        if not name or key in seen:
            continue
        if not 0.1 <= weight <= 2.0:
            raise ValueError(f"direction weight out of range: {name}")
        seen.add(key)
        cleaned.append({"name": name, "weight": weight})
    if not cleaned:
        raise ValueError("profile requires at least one valid direction")
    profile["directions"] = cleaned
    profile["languages"] = split_csv(",".join(profile.get("languages", ["zh", "en"]))) or ["zh", "en"]
    profile["exclusions"] = split_csv(",".join(profile.get("exclusions", [])))
    profile["region"] = str(profile.get("region", "global")).strip() or "global"
    profile["window_hours"] = max(1, min(168, int(profile.get("window_hours", 24))))
    profile["version"] = 1
    return profile


def load() -> dict | None:
    path = profile_path()
    if not path.exists():
        return None
    return validate(json.loads(path.read_text(encoding="utf-8")))


def save(profile: dict) -> Path:
    profile = validate(profile)
    path = profile_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)
    return path


def init_profile(preset: str, force: bool) -> dict:
    current = load()
    if current and not force:
        return current
    if preset not in PRESETS:
        raise ValueError(f"unknown preset: {preset}")
    profile = base_profile(PRESETS[preset])
    save(profile)
    return profile


def set_profile(args: argparse.Namespace) -> dict:
    profile = load() or base_profile(PRESETS["ai-media-tech"])
    existing_weights = {item["name"].casefold(): item["weight"] for item in profile["directions"]}
    if args.directions:
        profile["directions"] = [{"name": name, "weight": existing_weights.get(name.casefold(), 1.0)} for name in split_csv(args.directions)]
    if args.add_directions:
        seen = {item["name"].casefold() for item in profile["directions"]}
        profile["directions"].extend({"name": name, "weight": existing_weights.get(name.casefold(), 1.0)} for name in split_csv(args.add_directions) if name.casefold() not in seen)
    weights = parse_weights(args.weights)
    for item in profile["directions"]:
        if item["name"].casefold() in weights:
            item["weight"] = weights[item["name"].casefold()]
    if args.languages:
        profile["languages"] = split_csv(args.languages)
    if args.region:
        profile["region"] = args.region
    if args.exclude is not None:
        profile["exclusions"] = split_csv(args.exclude)
    if args.add_exclusions:
        profile["exclusions"] = list(dict.fromkeys([*profile["exclusions"], *split_csv(args.add_exclusions)]))
    if args.window_hours:
        profile["window_hours"] = args.window_hours
    save(profile)
    return profile


def self_test() -> None:
    old = os.environ.get("SIGNAL_RADAR_HOME")
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["SIGNAL_RADAR_HOME"] = tmp
        created = init_profile("ai-media-tech", False)
        assert [x["name"] for x in created["directions"]] == ["AI", "影像", "科技"]
        args = argparse.Namespace(directions="游戏,出海", add_directions=None, weights="游戏=1.5", languages="zh", region="CN", exclude="八卦", add_exclusions="明星", window_hours=48)
        changed = set_profile(args)
        assert [x["name"] for x in changed["directions"]] == ["游戏", "出海"]
        assert changed["directions"][0]["weight"] == 1.5
        assert changed["exclusions"] == ["八卦", "明星"]
        args = argparse.Namespace(directions=None, add_directions="机器人", weights=None, languages=None, region=None, exclude=None, add_exclusions=None, window_hours=None)
        changed = set_profile(args)
        assert [x["name"] for x in changed["directions"]] == ["游戏", "出海", "机器人"]
        assert changed["languages"] == ["zh"] and load() == changed
    if old is None:
        os.environ.pop("SIGNAL_RADAR_HOME", None)
    else:
        os.environ["SIGNAL_RADAR_HOME"] = old
    print("profile self-test: ok")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Manage the cross-platform hotspot focus profile")
    sub = p.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--preset", choices=sorted(PRESETS), default="ai-media-tech")
    init.add_argument("--force", action="store_true")
    show = sub.add_parser("show")
    show.add_argument("--json", action="store_true")
    set_cmd = sub.add_parser("set")
    set_cmd.add_argument("--directions")
    set_cmd.add_argument("--add-directions")
    set_cmd.add_argument("--weights", help="Comma-separated name=value pairs; allowed range 0.1-2.0")
    set_cmd.add_argument("--languages")
    set_cmd.add_argument("--region")
    set_cmd.add_argument("--exclude")
    set_cmd.add_argument("--add-exclusions")
    set_cmd.add_argument("--window-hours", type=int)
    sub.add_parser("presets")
    sub.add_parser("self-test")
    return p


def main() -> None:
    args = parser().parse_args()
    if args.command == "self-test":
        self_test()
        return
    if args.command == "presets":
        print(json.dumps(PRESETS, ensure_ascii=False, indent=2))
        return
    if args.command == "init":
        profile = init_profile(args.preset, args.force)
    elif args.command == "set":
        profile = set_profile(args)
    else:
        profile = load()
        if profile is None:
            raise SystemExit("No profile. Run: profile.py init --preset ai-media-tech")
    print(json.dumps(profile, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
