---
name: semantic-recall
description: 本地语义召回工具：在Codex技能、记忆笔记、项目文档、研究资料和工作记录中按含义检索相关内容。用于记得概念但记不清原句、寻找旧方案或复用历史经验。
version: 1.0.0
---

# Semantic Recall

Find local knowledge by meaning, then verify the best matches in their original files. Embedding hits are routing evidence, not final truth.

## Decision Rule

Use semantic recall for:

- remembered meaning with uncertain wording;
- similar past cases or habits;
- related rules spread across multiple files;
- cross-project or cross-thread durable knowledge;
- discovery before a narrower literal search.

Use literal search first for:

- exact strings;
- filenames and extensions;
- IDs, hashes, symbols, and error codes;
- known paths.

## Setup

The package excludes its virtual environment and search index. Install locally after copying the skill into the Codex skills directory.

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup.ps1
```

macOS/Linux:

```bash
bash scripts/setup.sh
```

Setup creates `.venv` inside the skill and installs the pinned local-search dependencies. The first index build downloads the embedding model.

## Default Locations

```text
CODEX_HOME                 default: ~/.codex
SEMANTIC_RECALL_DATA_DIR   default: $CODEX_HOME/semantic-recall-data
SEMANTIC_RECALL_ROOTS      optional OS-path-separated root list
```

Default roots are intentionally narrow:

- `$CODEX_HOME/skills`
- `$CODEX_HOME/AGENTS.md`
- `$CODEX_HOME/SESSION-STATE.md`
- `$CODEX_HOME/memory`

Pass project/workspace roots explicitly when needed.

## Commands

Windows wrapper:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/semantic_recall.ps1 status
powershell -ExecutionPolicy Bypass -File scripts/semantic_recall.ps1 index
powershell -ExecutionPolicy Bypass -File scripts/semantic_recall.ps1 index --root C:\path\to\workspace
powershell -ExecutionPolicy Bypass -File scripts/semantic_recall.ps1 query "the remembered idea" --top-k 8 --read-top 3
powershell -ExecutionPolicy Bypass -File scripts/semantic_recall.ps1 fast-query "the remembered idea" --top-k 8
powershell -ExecutionPolicy Bypass -File scripts/semantic_recall.ps1 smoke
```

macOS/Linux wrapper:

```bash
bash scripts/semantic_recall.sh status
bash scripts/semantic_recall.sh index --root /path/to/workspace
bash scripts/semantic_recall.sh fast-query "the remembered idea" --top-k 8
```

## Workflow

1. Inventory the likely source layer: current files, project state, skills, memory, research, or archives.
2. Run `status` when index freshness is unknown.
3. Run `index` when the index is missing, stale, or important roots changed.
4. Run `fast-query` for normal repeated use; it starts a localhost search server when needed.
5. Inspect the top source files directly.
6. Confirm important claims with literal search or file reading.
7. Answer from verified source content, not from similarity scores alone.

## Indexing

Core mode indexes each skill's `SKILL.md` and common text-like files from explicitly supplied non-skill roots.

```powershell
powershell -ExecutionPolicy Bypass -File scripts/semantic_recall.ps1 index --scope core
```

Deep mode includes skill references and scripts when architecture-level recall is required.

```powershell
powershell -ExecutionPolicy Bypass -File scripts/semantic_recall.ps1 index --scope deep
```

The indexer skips common dependency, build, cache, and VCS directories. Add large archives only when the current task needs them.

## Query Modes

### Cold query

Loads the model for one request:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/semantic_recall.ps1 query "reference-role isolation" --top-k 10
```

### Fast query

Reuses a local server and loaded model:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/semantic_recall.ps1 fast-query "reference-role isolation" --top-k 10 --read-top 3
```

Server controls:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/semantic_recall.ps1 server-status
powershell -ExecutionPolicy Bypass -File scripts/semantic_recall.ps1 stop-server
```

The server binds to `127.0.0.1` by default.

## Verification Rules

- Read the returned source before making a claim.
- Prefer the most authoritative and current local source.
- Distinguish user-confirmed facts, formal policy, project state, and inference.
- Do not let an older memory note override current project truth.
- Do not index secrets, credential stores, browser profiles, private keys, or raw auth files.
- Do not present similarity score as confidence or truth probability.

## Backend

The default backend is `txtai` with `intfloat/multilingual-e5-small`, stored entirely in the configured local data directory after model download.

Read [backend-options.md](references/backend-options.md) before replacing the backend or scaling to a much larger corpus.

## Output Contract

```text
Index state:
Query:
Best matches:
Verified takeaway:
```

Keep the user-facing result concise and omit internal search logs.
