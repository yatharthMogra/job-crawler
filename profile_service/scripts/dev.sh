#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ ! -x .venv/bin/uvicorn ]]; then
  echo "Missing .venv. Create it with:"
  echo "  python3.11 -m venv .venv && source .venv/bin/activate && pip install -e '.[dev]'"
  exit 1
fi

exec .venv/bin/uvicorn app.main:app --port 8001 --reload "$@"
