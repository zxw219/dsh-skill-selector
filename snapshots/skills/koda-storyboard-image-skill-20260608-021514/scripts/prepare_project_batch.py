#!/usr/bin/env python3
"""Create a conservative scaffold for Koda project-batch storyboard work."""

from __future__ import annotations

import argparse
import json
import math
import re
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from xml.etree import ElementTree


TEXT_EXTS = {".txt", ".md", ".csv", ".tsv", ".json", ".yaml", ".yml", ".srt", ".vtt", ".ass"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tif", ".tiff", ".heic", ".avif"}
VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".webm"}
DOC_EXTS = {".pdf", ".docx", ".pptx", ".xlsx", ".xls"}
DEFAULT_IGNORES = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    "outputs",
    "output",
    "work",
}

# Chinese strings use escapes so the script stays ASCII-safe on Windows consoles.
SCENE_PATTERNS = [
    re.compile(r"\bSC(?:ENE)?[_\-\s]*0*(\d{1,4})\b", re.IGNORECASE),
    re.compile(r"(?:^|[/\\_\-\s])S0*(\d{2,4})(?=$|[/\\_\-\s.])", re.IGNORECASE),
    re.compile(r"\u573a\u6b21\s*0*(\d{1,4})"),
    re.compile(r"\u573a\s*0*(\d{1,4})"),
    re.compile(r"\u7b2c\s*([0-9\u96f6\u3007\u4e00\u4e8c\u4e24\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343]+)\s*\u573a"),
]
CN_DIGITS = {
    "\u96f6": 0,
    "\u3007": 0,
    "\u4e00": 1,
    "\u4e8c": 2,
    "\u4e24": 2,
    "\u4e09": 3,
    "\u56db": 4,
    "\u4e94": 5,
    "\u516d": 6,
    "\u4e03": 7,
    "\u516b": 8,
    "\u4e5d": 9,
}
CN_UNITS = {"\u5341": 10, "\u767e": 100, "\u5343": 1000}
ROLE_HINTS = {
    "script": ["script", "\u5267\u672c"],
    "shotlist": ["shot", "shotlist", "storyboard", "\u5206\u955c", "\u955c\u5934"],
    "character": [
        "character",
        "characters",
        "char_",
        "actor",
        "person",
        "people",
        "hero",
        "protagonist",
        "\u89d2\u8272",
        "\u4eba\u7269",
        "\u4e3b\u89d2",
        "\u7537",
        "\u5973",
    ],
    "environment": [
        "environment",
        "environments",
        "location",
        "locations",
        "bg",
        "background",
        "room",
        "street",
        "alley",
        "forest",
        "courtyard",
        "\u573a\u666f",
        "\u73af\u5883",
        "\u5df7",
        "\u8857",
        "\u623f",
        "\u5c4b",
        "\u6797",
        "\u9662",
    ],
    "prop": [
        "prop",
        "props",
        "sword",
        "knife",
        "umbrella",
        "phone",
        "car",
        "cup",
        "bag",
        "\u9053\u5177",
        "\u5251",
        "\u5200",
        "\u4f1e",
        "\u676f",
        "\u8f66",
    ],
    "style_ref": ["style", "reference", "ref", "look", "mood", "\u98ce\u683c", "\u53c2\u8003"],
}


def category_for(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in IMAGE_EXTS:
        return "image"
    if ext in VIDEO_EXTS:
        return "video"
    if ext in TEXT_EXTS:
        return "text"
    if ext in DOC_EXTS:
        return "document"
    return "other"


def should_ignore(path: Path, root: Path, extra_ignores: set[str]) -> bool:
    ignores = DEFAULT_IGNORES | extra_ignores
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return False
    return any(part in ignores for part in parts)


def chinese_number_to_int(text: str) -> int | None:
    if not text:
        return None
    if text.isdigit():
        return int(text)
    total = 0
    number = 0
    seen = False
    for char in text:
        if char in CN_DIGITS:
            number = CN_DIGITS[char]
            seen = True
        elif char in CN_UNITS:
            unit = CN_UNITS[char]
            if number == 0:
                number = 1
            total += number * unit
            number = 0
            seen = True
        elif char.isspace():
            continue
        else:
            return None
    if not seen:
        return None
    return total + number


def normalize_scene_id(value: str | int) -> str:
    if isinstance(value, int):
        return f"SC{value:02d}"
    digits = re.findall(r"\d+", value)
    if digits:
        return f"SC{int(digits[0]):02d}"
    number = chinese_number_to_int(value)
    if number is not None:
        return f"SC{number:02d}"
    return "SC00"


def scene_id_from_text(text: str) -> str | None:
    for pattern in SCENE_PATTERNS:
        match = pattern.search(text)
        if match:
            return normalize_scene_id(match.group(1))
    return None


def read_text(path: Path, limit: int) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""
    return text[:limit]


def text_from_docx(path: Path, limit: int) -> str:
    try:
        with zipfile.ZipFile(path) as archive:
            xml = archive.read("word/document.xml")
    except Exception:
        return ""
    try:
        root = ElementTree.fromstring(xml)
    except Exception:
        return ""
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs = []
    for para in root.findall(".//w:p", ns):
        text = "".join(node.text or "" for node in para.findall(".//w:t", ns)).strip()
        if text:
            paragraphs.append(text)
    return "\n".join(paragraphs)[:limit]


def text_from_xlsx(path: Path, limit: int) -> str:
    try:
        with zipfile.ZipFile(path) as archive:
            shared: list[str] = []
            if "xl/sharedStrings.xml" in archive.namelist():
                root = ElementTree.fromstring(archive.read("xl/sharedStrings.xml"))
                for item in root.iter():
                    if item.tag.endswith("}t") and item.text:
                        shared.append(item.text)
            lines = []
            for name in sorted(n for n in archive.namelist() if n.startswith("xl/worksheets/") and n.endswith(".xml")):
                root = ElementTree.fromstring(archive.read(name))
                for row in root.iter():
                    if not row.tag.endswith("}row"):
                        continue
                    values = []
                    for cell in row:
                        if not cell.tag.endswith("}c"):
                            continue
                        cell_type = cell.attrib.get("t")
                        value_node = next((child for child in cell if child.tag.endswith("}v")), None)
                        if value_node is None or value_node.text is None:
                            continue
                        value = value_node.text
                        if cell_type == "s":
                            try:
                                value = shared[int(value)]
                            except Exception:
                                pass
                        values.append(value)
                    if values:
                        lines.append("\t".join(values))
                if len("\n".join(lines)) >= limit:
                    break
            return "\n".join(lines)[:limit]
    except Exception:
        return ""


def text_from_pdf(path: Path, limit: int) -> str:
    for module_name in ["pypdf", "PyPDF2"]:
        try:
            module = __import__(module_name)
            reader = module.PdfReader(str(path))
            pages = []
            for page in reader.pages[:30]:
                pages.append(page.extract_text() or "")
                if len("\n".join(pages)) >= limit:
                    break
            return "\n".join(pages)[:limit]
        except Exception:
            continue
    return ""


def read_source_text(path: Path, limit: int) -> str:
    ext = path.suffix.lower()
    if ext in TEXT_EXTS:
        return read_text(path, limit)
    if ext == ".docx":
        return text_from_docx(path, limit)
    if ext in {".xlsx", ".xls"}:
        return text_from_xlsx(path, limit)
    if ext == ".pdf":
        return text_from_pdf(path, limit)
    return ""


def collect_files(root: Path, extra_ignores: set[str]) -> list[dict[str, Any]]:
    files: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if path.is_dir() or should_ignore(path, root, extra_ignores):
            continue
        rel = path.relative_to(root).as_posix()
        role = classify_role(rel)
        files.append(
            {
                "path": rel,
                "name": path.name,
                "category": category_for(path),
                "role": role,
                "scene_hint": scene_id_from_text(rel),
            }
        )
    return files


def classify_role(rel: str) -> str:
    lowered = rel.lower()
    for role in ["script", "shotlist", "character", "environment", "prop", "style_ref"]:
        if any(term in lowered for term in ROLE_HINTS[role]):
            return role
    return "unknown"


def is_scene_heading(line: str) -> str | None:
    stripped = line.strip().lstrip("#").strip()
    if not stripped or len(stripped) > 140:
        return None
    return scene_id_from_text(stripped)


def extract_scene_sections(root: Path, files: list[dict[str, Any]], max_chars: int) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    for item in files:
        if item["category"] not in {"text", "document"}:
            continue
        path = root / item["path"]
        text = read_source_text(path, max_chars)
        if not text:
            continue
        lines = text.splitlines()
        headings: list[tuple[int, str, str]] = []
        for idx, line in enumerate(lines):
            scene_id = is_scene_heading(line)
            if scene_id:
                headings.append((idx, scene_id, line.strip()))
        for pos, (start, scene_id, heading) in enumerate(headings):
            end = headings[pos + 1][0] if pos + 1 < len(headings) else len(lines)
            body = "\n".join(lines[start:end]).strip()
            sections.append(
                {
                    "scene_id": scene_id,
                    "path": item["path"],
                    "start_line": start + 1,
                    "end_line": end,
                    "heading": heading,
                    "excerpt": body[:1600],
                    "shot_count_hint": estimate_shot_count(body),
                }
            )
    return sections


def estimate_shot_count(text: str) -> int:
    if not text:
        return 0
    explicit_patterns = [
        re.compile(r"^\s*(?:shot|camera|cam)\s*[:#\-\s]*0*\d+", re.IGNORECASE),
        re.compile(r"^\s*(?:\u955c\u5934|\u955c)\s*[:#\-\s]*0*\d+"),
    ]
    numbered_shot_row = re.compile(
        r"^\s*0*\d+\s*[\.\u3001,\t|,]\s*(?:shot|camera|cam|lens|wide|close|pan|tilt|track|push|\u955c\u5934|\u955c|\u666f\u522b|\u8fdc\u666f|\u4e2d\u666f|\u8fd1\u666f|\u7279\u5199|\u63a8|\u62c9|\u6447|\u79fb)",
        re.IGNORECASE,
    )
    first_lines = "\n".join(text.splitlines()[:6]).lower()
    table_has_shot_header = any(term in first_lines for term in ["shot", "camera", "lens", "\u955c\u5934", "\u666f\u522b"])
    count = 0
    for idx, line in enumerate(text.splitlines()):
        if any(pattern.search(line) for pattern in explicit_patterns):
            count += 1
        elif numbered_shot_row.search(line):
            count += 1
        elif table_has_shot_header and idx > 0 and re.search(r"^\s*0*\d+\s*[\t|,]", line):
            count += 1
    return count


def expected_sheet_count(shot_count: int, fallback: int = 2) -> int:
    if shot_count <= 0:
        return fallback
    if shot_count <= 3:
        return 1
    if shot_count <= 9:
        return 2
    return max(3, min(6, math.ceil(shot_count / 5)))


def build_scene_manifest(root: Path, files: list[dict[str, Any]], max_chars: int, global_assets_per_scene: int) -> list[dict[str, Any]]:
    sections = extract_scene_sections(root, files, max_chars)
    path_grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in files:
        if item["scene_hint"]:
            path_grouped[item["scene_hint"]].append(item)

    section_grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for section in sections:
        section_grouped[section["scene_id"]].append(section)

    scene_ids = sorted(set(path_grouped) | set(section_grouped))
    if not scene_ids:
        source_files = [item for item in files if item["category"] in {"text", "document"}]
        scene_ids = ["SC01"]
        path_grouped["SC01"] = source_files[:10]

    scenes: list[dict[str, Any]] = []
    global_assets = [item for item in files if item["category"] in {"image", "video"} and not item["scene_hint"]]
    for scene_id in scene_ids:
        scene_files = path_grouped.get(scene_id, [])
        scene_sections = section_grouped.get(scene_id, [])
        source_files = sorted({item["path"] for item in scene_files if item["category"] in {"text", "document"}})
        for section in scene_sections:
            source_files.append(f"{section['path']}:{section['start_line']}-{section['end_line']}")
        asset_candidates = [item["path"] for item in scene_files if item["category"] in {"image", "video"}]
        shot_count = max([section.get("shot_count_hint", 0) for section in scene_sections] or [0])
        scenes.append(
            {
                "scene_id": scene_id,
                "title": scene_sections[0]["heading"] if scene_sections else "",
                "source_files": source_files,
                "source_spans": scene_sections,
                "story_excerpt": "\n\n".join(section["excerpt"] for section in scene_sections)[:2400],
                "asset_candidates": asset_candidates,
                "global_asset_candidates": [item["path"] for item in global_assets[:global_assets_per_scene]],
                "shot_range": "",
                "shot_count_hint": shot_count,
                "expected_sheet_count": expected_sheet_count(shot_count),
                "status": "needs_review",
                "packet_status": "scaffold",
                "notes": "Review scene boundaries, assets, story action, and continuity locks before image generation.",
            }
        )
    return scenes


def role_buckets(paths: list[str]) -> dict[str, list[str]]:
    by_role: dict[str, list[str]] = defaultdict(list)
    for path in paths:
        by_role[classify_role(path)].append(path)
    return by_role


def write_scene_packet(out_dir: Path, scene: dict[str, Any], overwrite: bool) -> str:
    path = out_dir / f"{scene['scene_id']}.md"
    if path.exists() and not overwrite:
        return "preserved"

    scene_assets = role_buckets(scene.get("asset_candidates", []))
    global_assets = role_buckets(scene.get("global_asset_candidates", []))
    story_excerpt = scene.get("story_excerpt") or "[TODO: fill from script and shot list]"
    required_note = "Set packet_status to ready only after all TODO markers are resolved."

    lines = [
        f"# {scene['scene_id']} Scene Packet",
        "",
        "packet_status: scaffold",
        f"required: {required_note}",
        "",
        "## Source",
        f"- Scene title: {scene.get('title') or '[TODO: fill]'}",
        f"- Shot range: {scene.get('shot_range') or '[TODO: fill]'}",
        f"- Shot count hint: {scene.get('shot_count_hint', 0)}",
        f"- Expected sheets: {scene.get('expected_sheet_count', 2)}",
        "",
        "## Source Files",
    ]
    if scene["source_files"]:
        lines.extend(f"- `{path}`" for path in scene["source_files"])
    else:
        lines.append("- [TODO: fill]")

    lines.extend(["", "## Story Action", story_excerpt, "", "## Confirmed Scene Assets"])
    for role in ["character", "environment", "prop", "style_ref"]:
        values = scene_assets.get(role, [])
        lines.append(f"- {role}: " + (", ".join(f"`{value}`" for value in values) if values else "[TODO: fill or mark none]"))

    lines.extend(["", "## Shared Asset Hints"])
    for role in ["character", "environment", "prop", "style_ref"]:
        values = global_assets.get(role, [])
        if values:
            lines.append(f"- {role}: " + ", ".join(f"`{value}`" for value in values[:30]))

    uncertain = scene_assets.get("unknown", []) + global_assets.get("unknown", [])
    lines.extend(["", "## Uncertain Assets"])
    if uncertain:
        lines.extend(f"- `{value}`" for value in uncertain[:60])
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## First / Final State",
            "- First state: [TODO: fill]",
            "- Final state: [TODO: fill]",
            "",
            "## Continuity Locks",
            "- Identity/wardrobe: [TODO: fill]",
            "- Props/effects: [TODO: fill]",
            "- Geography/screen direction: [TODO: fill]",
            "- Allowed changes: [TODO: fill]",
            "",
            "## Prompt Notes",
            "- [TODO: fill before generation]",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return "written"


def load_existing_progress(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    entries = data.get("entries", [])
    return {entry.get("sheet_id"): entry for entry in entries if entry.get("sheet_id")}


def write_inventory(files: list[dict[str, Any]], root: Path, json_out: Path | None, md_out: Path | None) -> None:
    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps({"root": str(root), "total_files": len(files), "assets": files}, ensure_ascii=False, indent=2), encoding="utf-8")
    if md_out:
        by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for item in files:
            by_category[item["category"]].append(item)
        lines = ["# Asset Inventory", "", f"Root: `{root}`", f"Total files: {len(files)}", ""]
        for category in ["image", "video", "audio", "document", "text", "other"]:
            group = by_category.get(category, [])
            if not group:
                continue
            lines.extend([f"## {category.title()} Assets", ""])
            for item in group:
                bits = [f"`{item['path']}`", f"role:{item['role']}"]
                if item.get("scene_hint"):
                    bits.append(f"scene:{item['scene_hint']}")
                lines.append(f"- {' | '.join(bits)}")
            lines.append("")
        md_out.parent.mkdir(parents=True, exist_ok=True)
        md_out.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare a Koda storyboard project batch scaffold.")
    parser.add_argument("root", type=Path, help="Project root containing scripts, shotlists, and assets.")
    parser.add_argument("--out", type=Path, default=Path("work/koda_batch"), help="Output batch scaffold directory.")
    parser.add_argument("--ignore", action="append", default=[], help="Directory name to ignore. Can repeat.")
    parser.add_argument("--max-text-chars", type=int, default=300_000, help="Maximum characters to read from each text file.")
    parser.add_argument("--global-assets-per-scene", type=int, default=30, help="Maximum unassigned global assets attached to each scene.")
    parser.add_argument("--overwrite-packets", action="store_true", help="Rewrite existing scene packet markdown files.")
    parser.add_argument("--reset-progress", action="store_true", help="Discard existing batch_progress.json instead of merging.")
    parser.add_argument("--json-out", type=Path, help="Optional inventory JSON output from the same scan.")
    parser.add_argument("--md-out", type=Path, help="Optional inventory Markdown output from the same scan.")
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    out_dir = args.out.expanduser().resolve()
    scene_packet_dir = out_dir / "scene_packets"
    scene_packet_dir.mkdir(parents=True, exist_ok=True)

    files = collect_files(root, set(args.ignore))
    scenes = build_scene_manifest(root, files, args.max_text_chars, max(0, args.global_assets_per_scene))
    write_inventory(files, root, args.json_out, args.md_out)

    manifest = {
        "project_root": str(root),
        "status": "needs_review",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_files": len(files),
        "scenes": scenes,
    }
    roles = defaultdict(list)
    for item in files:
        roles[item["role"]].append(item["path"])

    bible_lines = [
        "# Continuity Bible",
        "",
        "continuity_status: scaffold",
        "required: Set continuity_status to ready after global locks are filled.",
        "",
        "## Global Character Locks",
        "- [TODO: fill identity, wardrobe, silhouette, accessories, state changes]",
        "",
        "## Global Prop Locks",
        "- [TODO: fill ownership, handoff, damage/open/closed/carried state]",
        "",
        "## Location And Timeline",
        "- [TODO: fill location geography, time of day, weather/light, story time]",
        "",
        "## Screen Direction",
        "- [TODO: fill travel direction, axis side, entrances/exits]",
        "",
        "## Asset Index Hints",
    ]
    for role in ["character", "environment", "prop", "style_ref", "script", "shotlist", "unknown"]:
        values = roles.get(role, [])
        if values:
            bible_lines.append(f"- {role}:")
            bible_lines.extend(f"  - `{path}`" for path in values[:80])
    bible_path = out_dir / "continuity_bible.md"
    if not bible_path.exists() or args.overwrite_packets:
        bible_path.write_text("\n".join(bible_lines) + "\n", encoding="utf-8")

    existing_progress = {} if args.reset_progress else load_existing_progress(out_dir / "batch_progress.json")
    prompt_lines = []
    progress_entries = []
    scene_status = []
    for scene in scenes:
        packet_write_status = write_scene_packet(scene_packet_dir, scene, overwrite=args.overwrite_packets)
        scene["packet_write_status"] = packet_write_status
        scene_status.append(
            {
                "scene_id": scene["scene_id"],
                "packet": f"scene_packets/{scene['scene_id']}.md",
                "status": "needs_review",
                "packet_write_status": packet_write_status,
            }
        )
        for sheet_num in range(1, int(scene.get("expected_sheet_count", 2)) + 1):
            sheet_id = f"{scene['scene_id']}_sheet_{sheet_num:02d}"
            output_name = f"{scene['scene_id']}/{sheet_id}.png"
            prompt_obj = {
                "scene_id": scene["scene_id"],
                "sheet_id": sheet_id,
                "shot_range": scene.get("shot_range", ""),
                "output_name": output_name,
                "asset_refs": scene.get("asset_candidates", []) + scene.get("global_asset_candidates", []),
                "prompt_notes": "Fill from scene packet before image generation.",
                "status": "needs_review",
            }
            prompt_lines.append(json.dumps(prompt_obj, ensure_ascii=False))
            prior = existing_progress.get(sheet_id, {})
            progress_entries.append(
                {
                    "scene_id": scene["scene_id"],
                    "sheet_id": sheet_id,
                    "status": prior.get("status", "pending"),
                    "output_path": prior.get("output_path"),
                    "error": prior.get("error"),
                }
            )

    (out_dir / "prompt_plan.jsonl").write_text("\n".join(prompt_lines) + ("\n" if prompt_lines else ""), encoding="utf-8")
    (out_dir / "scene_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    progress_payload = {
        "status": "needs_review",
        "project_root": str(root),
        "manifest": "scene_manifest.json",
        "continuity_bible": "continuity_bible.md",
        "scene_packets_dir": "scene_packets",
        "prompt_plan": "prompt_plan.jsonl",
        "scene_status": scene_status,
        "entries": progress_entries,
    }
    (out_dir / "batch_progress.json").write_text(json.dumps(progress_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(out_dir)


if __name__ == "__main__":
    main()
