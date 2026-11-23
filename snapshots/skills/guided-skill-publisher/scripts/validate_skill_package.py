#!/usr/bin/env python3
"""Validate a Skill directory or ZIP before registry upload."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
import zipfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

try:
    import yaml
except ImportError:  # pragma: no cover - handled as a structured validation error
    yaml = None


SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
IGNORED_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}
IGNORED_PARTS = {".git", ".hg", ".svn", ".venv", "node_modules", "__pycache__"}


@dataclass
class Report:
    source: str
    profile: str
    errors: list[dict[str, str]] = field(default_factory=list)
    warnings: list[dict[str, str]] = field(default_factory=list)
    facts: dict[str, object] = field(default_factory=dict)

    def add_error(self, code: str, message: str) -> None:
        self.errors.append({"code": code, "message": message})

    def add_warning(self, code: str, message: str) -> None:
        self.warnings.append({"code": code, "message": message})

    def payload(self) -> dict[str, object]:
        return {
            "ok": not self.errors,
            "source": self.source,
            "profile": self.profile,
            "facts": self.facts,
            "errors": self.errors,
            "warnings": self.warnings,
        }


def safe_archive_name(name: str) -> bool:
    normalized = name.replace("\\", "/")
    if (
        not normalized
        or "\x00" in normalized
        or normalized.startswith("/")
        or re.match(r"^[A-Za-z]:", normalized)
    ):
        return False
    return all(part not in {"", ".", ".."} for part in normalized.split("/"))


def normalized_key(name: str) -> str:
    return unicodedata.normalize("NFC", name.replace("\\", "/")).casefold().rstrip("/")


def parse_frontmatter(text: str) -> dict[str, object]:
    if text.startswith("\ufeff"):
        text = text[1:]
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must begin with YAML frontmatter")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise ValueError("SKILL.md frontmatter is not closed") from exc
    if yaml is None:
        raise ValueError("PyYAML is required for strict frontmatter validation")

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
    source = "\n".join(lines[1:end])
    try:
        values = yaml.load(source, Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML: {exc}") from exc
    if not isinstance(values, dict):
        raise ValueError("SKILL.md frontmatter must be a YAML mapping")
    if any(not isinstance(key, str) for key in values):
        raise ValueError("SKILL.md frontmatter keys must be strings")
    return values


def slugify(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    return re.sub(r"-+", "-", slug)


def is_semver(value: str) -> bool:
    match = SEMVER.fullmatch(value)
    if not match:
        return False
    prerelease = match.group(4)
    if prerelease:
        for identifier in prerelease.split("."):
            if identifier.isdigit() and len(identifier) > 1 and identifier.startswith("0"):
                return False
    return True


def inspect_metadata(report: Report, skill_bytes: bytes) -> None:
    try:
        text = skill_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        report.add_error("SKILL_MD_ENCODING", "SKILL.md must be valid UTF-8 text.")
        return
    try:
        metadata = parse_frontmatter(text)
    except ValueError as exc:
        report.add_error("SKILL_MD_FRONTMATTER", str(exc))
        return

    def text_field(key: str) -> str:
        value = metadata.get(key, "")
        if value is None or value == "":
            return ""
        if not isinstance(value, str):
            report.add_error(f"{key.upper()}_TYPE", f"{key} must be a YAML string.")
            return ""
        return value.strip()

    name = text_field("name")
    description = text_field("description")
    version = text_field("version")
    report.facts["metadata"] = {
        "name": name,
        "slug": slugify(name) if name else "",
        "version": version,
        "description_length": len(description),
    }

    if not name:
        report.add_error("NAME_REQUIRED", "SKILL.md frontmatter requires name.")
    elif report.profile == "moke" and not 2 <= len(name) <= 100:
        report.add_error("NAME_LENGTH", "MOKE requires name to contain 2-100 characters.")
    if name and not slugify(name):
        report.add_error("SLUG_INVALID", "name does not produce a usable ASCII slug.")

    if not description:
        report.add_error("DESCRIPTION_REQUIRED", "SKILL.md frontmatter requires description.")
    elif report.profile == "moke" and len(description) > 1000:
        report.add_error("DESCRIPTION_LENGTH", "MOKE limits description to 1000 characters.")

    if report.profile == "moke":
        if not version:
            report.add_error("VERSION_REQUIRED", "MOKE requires a semantic version in SKILL.md.")
        elif not is_semver(version):
            report.add_error("VERSION_INVALID", "version must use semantic version format, such as 1.0.0.")
    elif version and not is_semver(version):
        report.add_warning("VERSION_NON_SEMVER", "version is present but is not semantic version format.")


def iter_directory(source: Path) -> tuple[list[tuple[str, int]], bytes | None]:
    entries: list[tuple[str, int]] = []
    skill_data: bytes | None = None
    for path in sorted(source.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"symbolic link is not allowed: {path}")
        if not path.is_file():
            continue
        relative = path.relative_to(source).as_posix()
        entries.append((relative, path.stat().st_size))
        if relative == "SKILL.md":
            skill_data = path.read_bytes()
    return entries, skill_data


def validate_directory(source: Path, report: Report, max_expanded: int) -> None:
    try:
        entries, top_skill_data = iter_directory(source)
    except ValueError as exc:
        report.add_error("SYMLINK_NOT_ALLOWED", str(exc))
        return
    skill_paths = [name for name, _ in entries if PurePosixPath(name).name == "SKILL.md"]
    total = sum(size for _, size in entries)
    report.facts.update({"kind": "directory", "file_count": len(entries), "expanded_bytes": total})
    if total > max_expanded:
        report.add_error("EXPANDED_TOO_LARGE", f"Expanded files exceed {max_expanded} bytes.")
    if len(skill_paths) != 1:
        report.add_error("SKILL_MD_COUNT", f"Expected exactly one SKILL.md; found {len(skill_paths)}.")
    elif skill_paths[0] != "SKILL.md":
        report.add_warning("SKILL_MD_NESTED", "Place SKILL.md at the package root for broad registry compatibility.")
    skill_data = top_skill_data
    if skill_data is None and len(skill_paths) == 1:
        skill_data = (source / Path(skill_paths[0])).read_bytes()
    if skill_data is not None:
        inspect_metadata(report, skill_data)
    for name, _ in entries:
        parts = PurePosixPath(name).parts
        if PurePosixPath(name).name in IGNORED_NAMES or any(part in IGNORED_PARTS for part in parts):
            report.add_warning("UNNEEDED_FILE", f"Exclude non-delivery content: {name}")


def validate_zip(source: Path, report: Report, max_archive: int, max_expanded: int) -> None:
    archive_size = source.stat().st_size
    report.facts.update({"kind": "zip", "archive_bytes": archive_size})
    report.facts["sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
    if archive_size > max_archive:
        report.add_error("ARCHIVE_TOO_LARGE", f"ZIP exceeds {max_archive} bytes.")
    try:
        with zipfile.ZipFile(source) as zf:
            infos = [info for info in zf.infolist() if not info.is_dir()]
            report.facts["file_count"] = len(infos)
            report.facts["expanded_bytes"] = sum(info.file_size for info in infos)
            if report.facts["expanded_bytes"] > max_expanded:
                report.add_error("EXPANDED_TOO_LARGE", f"Expanded ZIP exceeds {max_expanded} bytes.")
            seen: set[str] = set()
            skill_infos: list[zipfile.ZipInfo] = []
            readable_skill_data: bytes | None = None
            for info in infos:
                if not safe_archive_name(info.filename):
                    report.add_error("UNSAFE_PATH", f"Unsafe ZIP path: {info.filename}")
                key = normalized_key(info.filename)
                if key in seen:
                    report.add_error("DUPLICATE_PATH", f"Duplicate ZIP path: {info.filename}")
                seen.add(key)
                if info.flag_bits & 0x1:
                    report.add_error("ENCRYPTED_ENTRY", f"Encrypted ZIP entry: {info.filename}")
                unix_mode = (info.external_attr >> 16) & 0o170000
                if unix_mode == 0o120000:
                    report.add_error("SYMLINK_NOT_ALLOWED", f"Symbolic-link ZIP entry: {info.filename}")
                if info.compress_type not in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}:
                    message = f"Compression method may be unsupported: {info.filename}"
                    if report.profile == "moke":
                        report.add_error("UNSUPPORTED_COMPRESSION", message)
                    else:
                        report.add_warning("UNSUPPORTED_COMPRESSION", message)
                if info.compress_size and info.file_size / info.compress_size > 100:
                    message = f"High compression ratio: {info.filename}"
                    if report.profile == "moke":
                        report.add_error("HIGH_COMPRESSION_RATIO", message)
                    else:
                        report.add_warning("HIGH_COMPRESSION_RATIO", message)
                if PurePosixPath(info.filename).name == "SKILL.md":
                    skill_infos.append(info)
                parts = PurePosixPath(info.filename).parts
                if PurePosixPath(info.filename).name in IGNORED_NAMES or any(part in IGNORED_PARTS for part in parts):
                    report.add_warning("UNNEEDED_FILE", f"Exclude non-delivery content: {info.filename}")

            # Read every eligible entry to verify local headers, decompression, size, and CRC.
            for info in infos:
                if info.flag_bits & 0x1:
                    continue
                if info.compress_type not in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}:
                    continue
                try:
                    chunks: list[bytes] | None = [] if info in skill_infos else None
                    bytes_read = 0
                    with zf.open(info, "r") as stream:
                        while True:
                            chunk = stream.read(1024 * 1024)
                            if not chunk:
                                break
                            bytes_read += len(chunk)
                            if bytes_read > max_expanded:
                                raise ValueError("entry expands beyond the configured package limit")
                            if chunks is not None:
                                chunks.append(chunk)
                    if bytes_read != info.file_size:
                        raise ValueError(
                            f"expanded size mismatch (expected {info.file_size}, read {bytes_read})"
                        )
                    if chunks is not None:
                        readable_skill_data = b"".join(chunks)
                except (zipfile.BadZipFile, RuntimeError, NotImplementedError, OSError, EOFError, ValueError) as exc:
                    report.add_error("ENTRY_READ_ERROR", f"Cannot verify ZIP entry {info.filename}: {exc}")
            if len(skill_infos) != 1:
                report.add_error("SKILL_MD_COUNT", f"Expected exactly one SKILL.md; found {len(skill_infos)}.")
            else:
                if skill_infos[0].filename != "SKILL.md":
                    report.add_warning("SKILL_MD_NESTED", "Place SKILL.md at the ZIP root for broad registry compatibility.")
                if readable_skill_data is not None:
                    inspect_metadata(report, readable_skill_data)
    except (zipfile.BadZipFile, OSError) as exc:
        report.add_error("ZIP_INVALID", f"Cannot read ZIP: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Skill directory or ZIP file")
    parser.add_argument("--profile", choices=("generic", "moke"), default="generic")
    parser.add_argument("--max-archive-mb", type=float, default=None)
    parser.add_argument("--max-expanded-mb", type=float, default=None)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    max_archive_mb = args.max_archive_mb if args.max_archive_mb is not None else (5 if args.profile == "moke" else 100)
    max_expanded_mb = args.max_expanded_mb if args.max_expanded_mb is not None else (50 if args.profile == "moke" else 500)
    max_archive = int(max_archive_mb * 1024 * 1024)
    max_expanded = int(max_expanded_mb * 1024 * 1024)
    report = Report(str(source), args.profile)

    if not source.exists():
        report.add_error("SOURCE_NOT_FOUND", f"Source does not exist: {source}")
    elif source.is_dir():
        validate_directory(source, report, max_expanded)
    elif source.is_file() and source.suffix.lower() == ".zip":
        validate_zip(source, report, max_archive, max_expanded)
    else:
        report.add_error("SOURCE_TYPE", "Source must be a directory or .zip file.")

    payload = report.payload()
    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("PASS" if payload["ok"] else "FAIL")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
