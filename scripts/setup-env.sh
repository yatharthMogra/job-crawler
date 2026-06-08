#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT/job-crawler"

cd "$ROOT"

if [[ ! -d "$VENV/bin" ]]; then
  echo "Creating virtualenv at $VENV"
  python3.11 -m venv "$VENV"
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
