from __future__ import annotations

import argparse
import http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import re
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib import error, request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
DEFAULT_DATA_DIR = Path(
    os.environ.get("SEMANTIC_RECALL_DATA_DIR", CODEX_HOME / "semantic-recall-data")
).expanduser()
DEFAULT_MODEL = "intfloat/multilingual-e5-small"
DEFAULT_SERVER_HOST = "127.0.0.1"
DEFAULT_SERVER_PORT = 8765
SERVER_START_TIMEOUT_SECONDS = 90
EMBEDDINGS_CLASS = None
_configured_roots = os.environ.get("SEMANTIC_RECALL_ROOTS", "")
DEFAULT_ROOTS = (
    [Path(item).expanduser() for item in _configured_roots.split(os.pathsep) if item.strip()]
    if _configured_roots
    else [
        CODEX_HOME / "skills",
        CODEX_HOME / "AGENTS.md",
        CODEX_HOME / "SESSION-STATE.md",
        CODEX_HOME / "memory",
    ]
)
TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".py",
    ".ps1",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".css",
    ".html",
    ".csv",
}
SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "graphify-out",
    ".obsidian",
    ".next",
    "dist",
    "build",
}
MAX_FILE_BYTES = 512 * 1024
CHUNK_MAX_CHARS = 1200
CHUNK_OVERLAP_LINES = 4
MAX_INDEX_TEXT_CHARS = 3000
SEARCH_CANDIDATE_MULTIPLIER = 8
SEARCH_CANDIDATE_MIN = 80
SMOKE_TESTS = [
    {
        "query": "find local knowledge by meaning when exact wording is unknown",
        "expect_any": ["semantic-recall"],
    },
    {
        "query": "verify embedding matches by reading the original source file",
        "expect_any": ["semantic-recall"],
    },
    {
        "query": "use literal search for exact ids paths hashes and filenames",
        "expect_any": ["semantic-recall"],
    },
    {
        "query": "reuse a local server for fast repeated semantic queries",
        "expect_any": ["semantic-recall"],
    },
]


@dataclass
class ChunkRecord:
    path: str
    relpath: str
    chunk_index: int
    start_line: int
    end_line: int
    preview: str
    text: str
    file_signature: str
    root: str
    record_type: str = "chunk"
    heading_path: str = ""

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "relpath": self.relpath,
            "chunk_index": self.chunk_index,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "preview": self.preview,
            "text": self.text,
            "file_signature": self.file_signature,
            "root": self.root,
            "record_type": self.record_type,
            "heading_path": self.heading_path,
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None


def file_signature(path: Path) -> str:
    stat = path.stat()
    return f"{stat.st_size}:{stat.st_mtime_ns}"


def preview_text(text: str, limit: int = 180) -> str:
    cleaned = " ".join(text.split())
    return cleaned[:limit]


def clean_heading(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip(" #\t")).strip()


def semantic_payload(chunk: ChunkRecord) -> str:
    parts = [
        f"Source: {chunk.relpath}",
        f"Lines: {chunk.start_line}-{chunk.end_line}",
        f"Type: {chunk.record_type}",
    ]
    if chunk.heading_path:
        parts.append(f"Headings: {chunk.heading_path}")
    parts.append(chunk.text)
    return "\n".join(parts)


def lexical_bonus(query: str, doc: dict) -> float:
    haystack = "\n".join(
        [
            str(doc.get("relpath", "")),
            str(doc.get("heading_path", "")),
            str(doc.get("preview", "")),
            str(doc.get("text", "")),
        ]
    ).lower()
    needle = query.strip().lower()
    if not needle:
        return 0.0

    bonus = 0.0
    if needle in haystack:
        bonus += 0.18

    parts = [part for part in re.split(r"[\s,，。；;：:！？!?、]+", needle) if len(part) >= 2]
    if parts:
        matched = sum(1 for part in parts if part in haystack)
        bonus += min(0.12, 0.12 * matched / len(parts))

    return bonus


def should_keep_file(root: Path, path: Path, scope: str) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return False
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return False
    except OSError:
        return False

    root_str = str(root)
    if root_str.endswith(r"\skills") and scope != "deep":
        rel_parts = path.relative_to(root).parts
        return len(rel_parts) == 2 and rel_parts[1] == "SKILL.md"

    if root_str.endswith(r"\projects"):
        rel_parts = path.relative_to(root).parts
        if len(rel_parts) < 2:
            return path.suffix.lower() == ".md"
        if rel_parts[1] not in {
            "00_project_brief.md",
            "02_research",
            "03_prompts",
            "05_reviews",
            "06_iterations",
            "07_final",
        }:
            return False
    return True


def iter_files(roots: list[Path], scope: str) -> Iterable[tuple[Path, Path]]:
    seen: set[str] = set()
    for root in roots:
        if not root.exists():
            continue
        if root.is_file():
            candidates = [root]
            anchor = root.parent
        else:
            candidates = root.rglob("*")
            anchor = root

        for path in candidates:
            if not path.is_file():
                continue
            if not should_keep_file(root, path, scope):
                continue
            key = str(path.resolve()).lower()
            if key in seen:
                continue
            seen.add(key)
            yield anchor, path


def chunk_text(path: Path, root: Path) -> list[ChunkRecord]:
    text = safe_read_text(path)
    if not text:
        return []
    lines = text.splitlines()
    if not lines:
        return []

    relpath = str(path.relative_to(root))
    sig = file_signature(path)
    root_str = str(root)
    chunks: list[ChunkRecord] = []
    start = 0
    chunk_index = 0

    while start < len(lines):
        char_count = 0
        end = start
        while end < len(lines):
            line = lines[end]
            projected = char_count + len(line) + 1
            if end > start and projected > CHUNK_MAX_CHARS:
                break
            char_count = projected
            end += 1

        chunk_lines = lines[start:end]
        chunk_body = "\n".join(chunk_lines).strip()
        if chunk_body:
            chunks.append(
                ChunkRecord(
                    path=str(path),
                    relpath=relpath,
                    chunk_index=chunk_index,
                    start_line=start + 1,
                    end_line=end,
                    preview=preview_text(chunk_body),
                    text=chunk_body,
                    file_signature=sig,
                    root=root_str,
                    record_type="window",
                )
            )
            chunk_index += 1

        if end >= len(lines):
            break
        start = max(end - CHUNK_OVERLAP_LINES, start + 1)

    return chunks


def file_record(path: Path, root: Path) -> ChunkRecord | None:
    text = safe_read_text(path)
    if not text:
        return None
    lines = text.splitlines()
    if not lines:
        return None
    relpath = str(path.relative_to(root))
    return ChunkRecord(
        path=str(path),
        relpath=relpath,
        chunk_index=0,
        start_line=1,
        end_line=len(lines),
        preview=preview_text(text),
        text=text.strip(),
        file_signature=file_signature(path),
        root=str(root),
        record_type="file",
    )


def heading_section_records(path: Path, root: Path) -> list[ChunkRecord]:
    text = safe_read_text(path)
    if not text:
        return []
    lines = text.splitlines()
    if not lines:
        return []

    relpath = str(path.relative_to(root))
    sig = file_signature(path)
    root_str = str(root)
    sections: list[tuple[int, int, str]] = []
    current_start = 0
    heading_stack: list[str] = []

    for idx, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not match:
            continue
        if idx > current_start:
            sections.append((current_start, idx, " > ".join(heading_stack)))

        level = len(match.group(1))
        title = clean_heading(match.group(2))
        heading_stack = heading_stack[: max(0, level - 1)]
        heading_stack.append(title)
        current_start = idx

    sections.append((current_start, len(lines), " > ".join(heading_stack)))

    if len(sections) == 1 and not sections[0][2]:
        return chunk_text(path, root)

    records: list[ChunkRecord] = []
    chunk_index = 0
    for start, end, heading_path in sections:
        block = "\n".join(lines[start:end]).strip()
        if not block:
            continue
        if len(block) <= CHUNK_MAX_CHARS * 2:
            records.append(
                ChunkRecord(
                    path=str(path),
                    relpath=relpath,
                    chunk_index=chunk_index,
                    start_line=start + 1,
                    end_line=end,
                    preview=preview_text(block),
                    text=block,
                    file_signature=sig,
                    root=root_str,
                    record_type="section",
                    heading_path=heading_path,
                )
            )
            chunk_index += 1
            continue

        sublines = lines[start:end]
        substart = 0
        while substart < len(sublines):
            char_count = 0
            subend = substart
            while subend < len(sublines):
                projected = char_count + len(sublines[subend]) + 1
                if subend > substart and projected > CHUNK_MAX_CHARS * 2:
                    break
                char_count = projected
                subend += 1
            chunk_body = "\n".join(sublines[substart:subend]).strip()
            if chunk_body:
                records.append(
                    ChunkRecord(
                        path=str(path),
                        relpath=relpath,
                        chunk_index=chunk_index,
                        start_line=start + substart + 1,
                        end_line=start + subend,
                        preview=preview_text(chunk_body),
                        text=chunk_body,
                        file_signature=sig,
                        root=root_str,
                        record_type="section-window",
                        heading_path=heading_path,
                    )
                )
                chunk_index += 1
            if subend >= len(sublines):
                break
            substart = max(subend - CHUNK_OVERLAP_LINES, substart + 1)

    return records


def records_for_path(path: Path, root: Path, scope: str) -> list[ChunkRecord]:
    if path.suffix.lower() == ".md":
        return heading_section_records(path, root)
    if scope == "core":
        return chunk_text(path, root)
    return chunk_text(path, root)


def metadata_path(data_dir: Path) -> Path:
    return data_dir / "index.json"


def docs_path(data_dir: Path) -> Path:
    return data_dir / "documents.jsonl"


def txtai_path(data_dir: Path) -> Path:
    return data_dir / "txtai"


def load_metadata(data_dir: Path) -> dict | None:
    path = metadata_path(data_dir)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_metadata(data_dir: Path, metadata: dict) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    metadata_path(data_dir).write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")


def save_documents(data_dir: Path, documents: list[dict]) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    with docs_path(data_dir).open("w", encoding="utf-8") as handle:
        for doc in documents:
            handle.write(json.dumps(doc, ensure_ascii=False) + "\n")


def load_documents(data_dir: Path) -> list[dict]:
    path = docs_path(data_dir)
    if not path.exists():
        return []
    docs = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                docs.append(json.loads(line))
    return docs


def embeddings_class():
    global EMBEDDINGS_CLASS
    if EMBEDDINGS_CLASS is None:
        from txtai import Embeddings

        EMBEDDINGS_CLASS = Embeddings
    return EMBEDDINGS_CLASS


def build_embeddings(model_name: str):
    return embeddings_class()({"path": model_name, "content": True})


def format_index_text(model_name: str, text: str) -> str:
    if "e5" in model_name.lower():
        return f"passage: {text}"
    return text


def format_query_text(model_name: str, text: str) -> str:
    if "e5" in model_name.lower():
        return f"query: {text}"
    return text


def run_index(args: argparse.Namespace) -> int:
    data_dir = Path(args.data_dir)
    roots = [Path(r) for r in (args.root or [])] or DEFAULT_ROOTS
    model_name = args.model
    scope = args.scope

    documents: list[dict] = []
    rows = []
    file_count = 0
    chunk_count = 0
    missing_roots = [str(root) for root in roots if not root.exists()]

    for root, path in iter_files(roots, scope):
        file_count += 1
        chunks = records_for_path(path, root, scope)
        for chunk in chunks:
            if not chunk:
                continue
            doc = chunk.to_dict()
            doc_id = f"{chunk.path}::{chunk.chunk_index}"
            documents.append({"id": doc_id, **doc})
            rows.append((doc_id, format_index_text(model_name, semantic_payload(chunk)[:MAX_INDEX_TEXT_CHARS]), None))
            chunk_count += 1

    embeddings = build_embeddings(model_name)
    embeddings.index(rows)

    data_dir.mkdir(parents=True, exist_ok=True)
    embeddings.save(str(txtai_path(data_dir)))
    save_documents(data_dir, documents)

    metadata = {
        "generated_at": utc_now(),
        "model_name": model_name,
        "roots": [str(root) for root in roots],
        "scope": scope,
        "file_count": file_count,
        "record_count": chunk_count,
        "missing_roots": missing_roots,
        "backend": "txtai",
        "chunk_max_chars": CHUNK_MAX_CHARS,
        "chunk_overlap_lines": CHUNK_OVERLAP_LINES,
        "max_index_text_chars": MAX_INDEX_TEXT_CHARS,
        "search_candidate_multiplier": SEARCH_CANDIDATE_MULTIPLIER,
        "search_candidate_min": SEARCH_CANDIDATE_MIN,
        "record_strategy": "markdown-heading-sections",
    }
    save_metadata(data_dir, metadata)

    print(
        json.dumps(
            {
                "status": "ok",
                "mode": "index",
                "data_dir": str(data_dir),
                "file_count": file_count,
                "record_count": chunk_count,
                "model_name": model_name,
                "scope": scope,
                "backend": "txtai",
                "generated_at": metadata["generated_at"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def run_status(args: argparse.Namespace) -> int:
    data_dir = Path(args.data_dir)
    metadata = load_metadata(data_dir)
    if metadata is None:
        print(json.dumps({"status": "missing", "data_dir": str(data_dir)}, ensure_ascii=False, indent=2))
        return 0
    metadata = dict(metadata)
    metadata["runtime_search_candidate_multiplier"] = SEARCH_CANDIDATE_MULTIPLIER
    metadata["runtime_search_candidate_min"] = SEARCH_CANDIDATE_MIN
    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    return 0


def search_matches(
    embeddings,
    metadata: dict,
    documents: list[dict],
    query: str,
    top_k: int,
    read_top: int = 0,
    snippet_chars: int = 500,
) -> list[dict]:
    by_id = {doc["id"]: doc for doc in documents}
    candidate_k = min(len(documents), max(top_k, SEARCH_CANDIDATE_MIN, top_k * SEARCH_CANDIDATE_MULTIPLIER))
    results = embeddings.search(format_query_text(metadata["model_name"], query), candidate_k)

    matches = []
    for result in results:
        doc = by_id.get(str(result["id"]))
        if not doc:
            continue

        raw_score = float(result["score"])
        adjusted_score = raw_score + lexical_bonus(query, doc)
        match = {
            "score": round(adjusted_score, 4),
            "raw_score": round(raw_score, 4),
            "path": doc["path"],
            "relpath": doc["relpath"],
            "chunk_index": doc["chunk_index"],
            "start_line": doc["start_line"],
            "end_line": doc["end_line"],
            "record_type": doc.get("record_type", "chunk"),
            "heading_path": doc.get("heading_path", ""),
            "preview": doc["preview"],
            "root": doc["root"],
        }
        matches.append(match)

    matches.sort(key=lambda item: item["score"], reverse=True)
    matches = matches[:top_k]

    if read_top > 0:
        for match in matches[:read_top]:
            doc = next(
                (
                    item
                    for item in documents
                    if item["path"] == match["path"] and item["chunk_index"] == match.get("chunk_index")
                ),
                None,
            )
            if doc is None:
                doc = next(
                    (
                        item
                        for item in documents
                        if item["path"] == match["path"]
                        and item["start_line"] == match["start_line"]
                        and item["end_line"] == match["end_line"]
                    ),
                    None,
                )
            if doc is not None:
                match["text"] = str(doc.get("text", ""))[:snippet_chars]

    return matches


def load_index_for_query(data_dir: Path) -> tuple[dict, list[dict], object]:
    metadata = load_metadata(data_dir)
    documents = load_documents(data_dir)
    txtai_dir = txtai_path(data_dir)

    if metadata is None or not documents or not txtai_dir.exists():
        raise SystemExit("Index is missing. Run `index` first.")

    embeddings = embeddings_class()()
    embeddings.load(str(txtai_dir))
    return metadata, documents, embeddings


def run_query(args: argparse.Namespace) -> int:
    data_dir = Path(args.data_dir)
    metadata, documents, embeddings = load_index_for_query(data_dir)
    matches = search_matches(
        embeddings,
        metadata,
        documents,
        args.query,
        args.top_k,
        read_top=args.read_top,
        snippet_chars=args.snippet_chars,
    )

    print(
        json.dumps(
            {
                "status": "ok",
                "mode": "query",
                "query": args.query,
                "top_k": min(args.top_k, len(matches)),
                "matches": matches,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def run_smoke(args: argparse.Namespace) -> int:
    data_dir = Path(args.data_dir)
    metadata, documents, embeddings = load_index_for_query(data_dir)
    checks = []

    for test in SMOKE_TESTS:
        matches = search_matches(embeddings, metadata, documents, test["query"], args.top_k)
        joined = "\n".join(match["path"] for match in matches).lower()
        passed = any(expected.lower() in joined for expected in test["expect_any"])
        checks.append(
            {
                "query": test["query"],
                "passed": passed,
                "best": [
                    {
                        "score": match["score"],
                        "path": match["path"],
                        "start_line": match["start_line"],
                        "heading_path": match.get("heading_path", ""),
                    }
                    for match in matches[:3]
                ],
            }
        )

    print(
        json.dumps(
            {
                "status": "ok" if all(check["passed"] for check in checks) else "needs_attention",
                "mode": "smoke",
                "top_k": args.top_k,
                "passed": sum(1 for check in checks if check["passed"]),
                "total": len(checks),
                "checks": checks,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


class RecallServerState:
    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.started_at = utc_now()
        self.metadata, self.documents, self.embeddings = load_index_for_query(data_dir)


def server_url(host: str, port: int, path: str = "") -> str:
    return f"http://{host}:{port}{path}"


def post_json(url: str, payload: dict, timeout: float = 5.0) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def get_json(url: str, timeout: float = 3.0) -> dict:
    with request.urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def server_health(host: str, port: int) -> dict | None:
    try:
        return get_json(server_url(host, port, "/status"), timeout=2.0)
    except (OSError, error.URLError, TimeoutError, http.client.HTTPException):
        return None


def make_handler(state: RecallServerState):
    class RecallHandler(BaseHTTPRequestHandler):
        server_version = "SemanticRecall/1.0"

        def log_message(self, format: str, *args) -> None:  # noqa: A002
            return

        def send_json(self, payload: dict, status: int = 200) -> None:
            body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def read_payload(self) -> dict:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            return json.loads(raw.decode("utf-8"))

        def do_GET(self) -> None:
            if self.path == "/status":
                self.send_json(
                    {
                        "status": "ok",
                        "mode": "server",
                        "started_at": state.started_at,
                        "data_dir": str(state.data_dir),
                        "model_name": state.metadata.get("model_name"),
                        "record_count": len(state.documents),
                        "index_generated_at": state.metadata.get("generated_at"),
                    }
                )
                return
            self.send_json({"status": "not_found", "path": self.path}, status=404)

        def do_POST(self) -> None:
            try:
                if self.path == "/query":
                    payload = self.read_payload()
                    query = str(payload.get("query", "")).strip()
                    if not query:
                        self.send_json({"status": "error", "message": "Missing query."}, status=400)
                        return
                    top_k = int(payload.get("top_k", 8))
                    read_top = int(payload.get("read_top", 0))
                    snippet_chars = int(payload.get("snippet_chars", 700))
                    matches = search_matches(
                        state.embeddings,
                        state.metadata,
                        state.documents,
                        query,
                        top_k,
                        read_top=read_top,
                        snippet_chars=snippet_chars,
                    )
                    self.send_json(
                        {
                            "status": "ok",
                            "mode": "fast-query",
                            "query": query,
                            "top_k": min(top_k, len(matches)),
                            "matches": matches,
                        }
                    )
                    return

                if self.path == "/shutdown":
                    self.send_json({"status": "ok", "mode": "stop-server"})
                    threading.Thread(target=self.server.shutdown, daemon=True).start()
                    return

                self.send_json({"status": "not_found", "path": self.path}, status=404)
            except KeyboardInterrupt:
                raise
            except Exception as exc:
                self.send_json({"status": "error", "message": str(exc)}, status=500)

    return RecallHandler


def run_serve(args: argparse.Namespace) -> int:
    data_dir = Path(args.data_dir)
    state = RecallServerState(data_dir)
    httpd = ThreadingHTTPServer((args.host, args.port), make_handler(state))
    print(
        json.dumps(
            {
                "status": "ok",
                "mode": "serve",
                "url": server_url(args.host, args.port),
                "data_dir": str(data_dir),
                "record_count": len(state.documents),
                "model_name": state.metadata.get("model_name"),
                "index_generated_at": state.metadata.get("generated_at"),
            },
            ensure_ascii=False,
            indent=2,
        ),
        flush=True,
    )
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
    return 0


def start_server(args: argparse.Namespace) -> None:
    script_path = Path(__file__).resolve()
    data_dir = Path(args.data_dir)
    log_path = data_dir / "semantic-recall-server.log"
    data_dir.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        str(script_path),
        "--data-dir",
        str(data_dir),
        "serve",
        "--host",
        args.host,
        "--port",
        str(args.port),
    ]
    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS

    with log_path.open("a", encoding="utf-8") as log:
        subprocess.Popen(
            command,
            cwd=str(script_path.parent),
            stdout=log,
            stderr=log,
            stdin=subprocess.DEVNULL,
            creationflags=creationflags,
            close_fds=os.name != "nt",
        )


def wait_for_server(host: str, port: int, timeout_seconds: float) -> dict:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        health = server_health(host, port)
        if health and health.get("status") == "ok":
            return health
        time.sleep(0.5)
    raise SystemExit("Semantic recall server did not become ready in time.")


def run_fast_query(args: argparse.Namespace) -> int:
    health = server_health(args.host, args.port)
    started = False
    if not health:
        start_server(args)
        started = True
        health = wait_for_server(args.host, args.port, SERVER_START_TIMEOUT_SECONDS)

    result = post_json(
        server_url(args.host, args.port, "/query"),
        {
            "query": args.query,
            "top_k": args.top_k,
            "read_top": args.read_top,
            "snippet_chars": args.snippet_chars,
        },
        timeout=30.0,
    )
    result["server_started"] = started
    result["server"] = health
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def run_server_status(args: argparse.Namespace) -> int:
    health = server_health(args.host, args.port)
    if not health:
        health = {"status": "missing", "mode": "server-status", "url": server_url(args.host, args.port)}
    print(json.dumps(health, ensure_ascii=False, indent=2))
    return 0


def run_stop_server(args: argparse.Namespace) -> int:
    try:
        result = post_json(server_url(args.host, args.port, "/shutdown"), {}, timeout=3.0)
    except (OSError, error.URLError, TimeoutError, http.client.HTTPException):
        result = {"status": "missing", "mode": "stop-server", "url": server_url(args.host, args.port)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local semantic recall for Codex workflow artifacts.")
    parser.add_argument("--data-dir", default=str(DEFAULT_DATA_DIR))
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--host", default=DEFAULT_SERVER_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_SERVER_PORT)

    subparsers = parser.add_subparsers(dest="command", required=True)

    index_parser = subparsers.add_parser("index")
    index_parser.add_argument("--root", action="append", help="Root folder to include. Repeatable.")
    index_parser.add_argument("--scope", choices=["core", "deep"], default="core")
    index_parser.set_defaults(func=run_index)

    status_parser = subparsers.add_parser("status")
    status_parser.set_defaults(func=run_status)

    query_parser = subparsers.add_parser("query")
    query_parser.add_argument("query")
    query_parser.add_argument("--top-k", type=int, default=8)
    query_parser.add_argument("--read-top", type=int, default=0, help="Include source text for the first N matches.")
    query_parser.add_argument("--snippet-chars", type=int, default=700)
    query_parser.set_defaults(func=run_query)

    smoke_parser = subparsers.add_parser("smoke")
    smoke_parser.add_argument("--top-k", type=int, default=8)
    smoke_parser.set_defaults(func=run_smoke)

    serve_parser = subparsers.add_parser("serve")
    serve_parser.add_argument("--host", default=DEFAULT_SERVER_HOST)
    serve_parser.add_argument("--port", type=int, default=DEFAULT_SERVER_PORT)
    serve_parser.set_defaults(func=run_serve)

    fast_query_parser = subparsers.add_parser("fast-query")
    fast_query_parser.add_argument("query")
    fast_query_parser.add_argument("--top-k", type=int, default=8)
    fast_query_parser.add_argument("--read-top", type=int, default=0)
    fast_query_parser.add_argument("--snippet-chars", type=int, default=700)
    fast_query_parser.set_defaults(func=run_fast_query)

    server_status_parser = subparsers.add_parser("server-status")
    server_status_parser.set_defaults(func=run_server_status)

    stop_server_parser = subparsers.add_parser("stop-server")
    stop_server_parser.set_defaults(func=run_stop_server)

    return parser


def main() -> int:
    parser = make_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
