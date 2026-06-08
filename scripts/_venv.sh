#!/usr/bin/env bash
# shellcheck disable=SC2034
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$ROOT/job-crawler"

if [[ ! -x "$VENV/bin/python" ]]; then
  echo "Missing virtualenv at $VENV" >&2
  echo "Run: ./scripts/setup-env.sh" >&2
  exit 1
fi
