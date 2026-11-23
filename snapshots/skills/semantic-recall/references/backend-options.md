# Backend Options

This skill starts with a lightweight local backend, but there are real GitHub options if the recall layer grows.

## Current Choice

- **Primary backend:** `neuml/txtai`
- **Why now:** mature GitHub semantic-search stack, local file-based deployment, better long-term fit than a hand-rolled flat-vector script.

GitHub:

- [neuml/txtai](https://github.com/neuml/txtai)

## Upgrade Paths

### 1. `neuml/txtai`

Current default.

Why it is interesting:

- semantic search is the core feature;
- broader framework surface if this grows into richer retrieval workflows.

Tradeoff:

- heavier install;
- pulls a larger transformer/runtime stack.

### 2. `asg017/sqlite-vec`

Use when you want a very local SQLite-native vector layer and tighter integration with a small portable store.

Why it is interesting:

- tiny SQLite extension;
- good fit if we later want one-file local storage plus FTS-style hybrid workflows.

Tradeoff:

- lower-level integration work;
- pre-v1 and more manual than the current script.

GitHub:

- [asg017/sqlite-vec](https://github.com/asg017/sqlite-vec)

### 3. `lancedb/lancedb`

Use when this recall layer becomes larger, more multimodal, or needs a stronger embedded retrieval store.

Why it is interesting:

- production-oriented embedded vector search;
- stronger scaling path than a flat `.npy` index.

Tradeoff:

- heavier than needed for first deployment;
- more moving parts than the current workflow needs.

GitHub:

- [lancedb/lancedb](https://github.com/lancedb/lancedb)

## Decision Rule

Stay on `txtai` while:

- the corpus is mainly local text artifacts;
- a file-based local stack is enough;
- you want a mature semantic-search framework without starting a separate service.

Reconsider the backend when:

- SQLite-native storage becomes a hard requirement;
- the corpus grows enough that a stronger embedded vector database becomes worth the extra complexity;
- multimodal or more advanced filtering/storage needs become central.
