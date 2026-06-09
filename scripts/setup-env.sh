#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT/job-crawler"

cd "$ROOT"

if [[ ! -d "$VENV/bin" ]]; then
  PYTHON=""
  for candidate in python3.12 python3.11 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
      ver="$("$candidate" -c 'import sys; print(sys.version_info.minor)')"
      if [[ "$ver" -ge 11 ]]; then
        PYTHON="$candidate"
        break
      fi
    fi
  done
  [[ -n "$PYTHON" ]] || { echo "Need Python 3.11+ (found only older python3)"; exit 1; }
  echo "Creating virtualenv at $VENV using $PYTHON"
  "$PYTHON" -m venv "$VENV"
fi

"$VENV/bin/pip" install --upgrade pip
"$VENV/bin/pip" install -e ".[dev]"

echo ""
echo "Virtualenv ready. Activate with:"
echo "  source $VENV/bin/activate"
echo ""
echo "Or run services via:"
echo "  ./scripts/dev-job-ingestion.sh"
echo "  ./scripts/dev-profile-service.sh"
echo "  ./scripts/dev-recommendation-service.sh"
