#!/usr/bin/env bash
set -euo pipefail
# shellcheck source=_venv.sh
source "$(dirname "$0")/_venv.sh"

cd "$ROOT/job_ingestion"
exec "$VENV/bin/uvicorn" app.main:app --port 8000 --reload --timeout-graceful-shutdown 45 "$@"
