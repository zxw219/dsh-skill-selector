#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON="$SKILL_DIR/.venv/bin/python"

if [[ ! -x "$PYTHON" ]]; then
  printf 'Missing local environment. Run scripts/setup.sh first.\n' >&2
  exit 1
fi

exec "$PYTHON" -X utf8 "$SCRIPT_DIR/semantic_recall.py" "$@"
