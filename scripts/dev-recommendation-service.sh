#!/usr/bin/env bash
set -euo pipefail
# shellcheck source=_venv.sh
source "$(dirname "$0")/_venv.sh"

cd "$ROOT/recommendation_service"
exec "$VENV/bin/uvicorn" app.main:app --port 8002 --reload "$@"
