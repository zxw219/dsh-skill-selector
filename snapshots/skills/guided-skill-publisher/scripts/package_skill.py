#!/usr/bin/env python3
"""Create a clean, deterministic ZIP from a Skill directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import zipfile
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - reported when rewriting frontmatter
    yaml = None


EXCLUDED_DIRS = {".git", ".hg", ".svn", ".venv", "node_modules", "__pycache__"}
EXCLUDED_FILES = {".DS_Store", "Thumbs.db", "desktop.ini"}
FIXED_TIME = (2020, 1, 1, 0, 0, 0)
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def collect(source: Path, output: Path) -> list[Path]:
    files: list[Path] = []
    for root, dirnames, filenames in os.walk(source):
        dirnames[:] = sorted(name for name in dirnames if name not in EXCLUDED_DIRS)
        root_path = Path(root)
        for filename in sorted(filenames):
            if filename in EXCLUDED_FILES:
                continue
            path = root_path / filename
            if path.resolve() == output:
                continue
            if path.is_symlink():
                raise ValueError(f"symbolic link is not allowed: {path}")
            files.append(path)
    return sorted(files, key=lambda item: item.relative_to(source).as_posix())


def is_semver(value: str) -> bool:
    match = SEMVER.fullmatch(value)
    if not match:
        return False
    prerelease = match.group(4)
    return not prerelease or all(
        not (part.isdigit() and len(part) > 1 and part.startswith("0"))
        for part in prerelease.split(".")
    )


def set_frontmatter_scalar(data: bytes, field: str, value: str) -> bytes:
    text = data.decode("utf-8-sig")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"SKILL.md must begin with YAML frontmatter before setting {field}")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise ValueError("SKILL.md frontmatter is not closed") from exc
    if yaml is None:
        raise ValueError("PyYAML is required when rewriting SKILL.md frontmatter")

    class UniqueKeyLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader, node, deep=False):
        mapping = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"duplicate key: {key!r}",
                    key_node.start_mark,
                )
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping

    UniqueKeyLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping,
    )
    try:
        parsed = yaml.load("\n".join(lines[1:end]), Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid SKILL.md YAML: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("SKILL.md frontmatter must be a YAML mapping")
    if any(not isinstance(key, str) for key in parsed):
        raise ValueError("SKILL.md frontmatter keys must be strings")

    field_line = f"{field}: {json.dumps(value, ensure_ascii=False)}"
    existing = [i for i in range(1, end) if lines[i].startswith(f"{field}:")]
    if len(existing) > 1:
        raise ValueError(f"SKILL.md contains duplicate top-level {field} fields")
    if existing:
        current = lines[existing[0]].split(":", 1)[1].strip()
        if not current or current in {">", "|", ">-", "|-", ">+", "|+"}:
            raise ValueError(f"Cannot safely rewrite multiline or nested top-level {field}")
        lines[existing[0]] = field_line
    else:
        lines.insert(end, field_line)
        end += 1

    rewritten_source = "\n".join(lines[1:end])
    try:
        rewritten = yaml.load(rewritten_source, Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        raise ValueError(f"rewriting {field} would produce invalid YAML: {exc}") from exc
    expected = dict(parsed)
    expected[field] = value
    if rewritten != expected:
        raise ValueError(f"Cannot safely rewrite complex top-level {field}; other metadata would change")
    return ("\n".join(lines) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Skill directory")
    parser.add_argument("--output", type=Path, required=True, help="Destination ZIP")
    parser.add_argument(
        "--set-version",
        help="Set or replace a top-level semantic version in the packaged SKILL.md without editing the source",
    )
    parser.add_argument(
        "--set-name",
        help="Set or replace the packaged top-level Skill name without editing the source",
    )
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if not source.is_dir():
        print(json.dumps({"ok": False, "error": f"Not a directory: {source}"}, ensure_ascii=False))
        return 1
    if output.suffix.lower() != ".zip":
        print(json.dumps({"ok": False, "error": "Output path must end in .zip."}, ensure_ascii=False))
        return 1
    if output.exists() and output.is_dir():
        print(json.dumps({"ok": False, "error": "Output path is a directory."}, ensure_ascii=False))
        return 1
    if args.set_version and not is_semver(args.set_version):
        print(json.dumps({"ok": False, "error": "--set-version must be valid SemVer."}, ensure_ascii=False))
        return 1
    try:
        files = collect(source, output)
    except ValueError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1
    if not files:
        print(json.dumps({"ok": False, "error": "Skill directory is empty."}, ensure_ascii=False))
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.unlink(missing_ok=True)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for path in files:
                relative = path.relative_to(source).as_posix()
                info = zipfile.ZipInfo(relative, date_time=FIXED_TIME)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                data = path.read_bytes()
                if relative == "SKILL.md" and args.set_name:
                    data = set_frontmatter_scalar(data, "name", args.set_name)
                if relative == "SKILL.md" and args.set_version:
                    data = set_frontmatter_scalar(data, "version", args.set_version)
                zf.writestr(info, data)
        temporary.replace(output)
    except (OSError, UnicodeDecodeError, ValueError, zipfile.BadZipFile) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1
    finally:
        temporary.unlink(missing_ok=True)

    payload = {
        "ok": True,
        "source": str(source),
        "output": str(output),
        "file_count": len(files),
        "bytes": output.stat().st_size,
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "packaged_version": args.set_version,
        "packaged_name": args.set_name,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
