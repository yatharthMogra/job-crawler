#!/usr/bin/env bash
set -euo pipefail
# shellcheck source=_venv.sh
source "$(dirname "$0")/_venv.sh"

export ENABLE_NOTIFICATION_SCHEDULER="${ENABLE_NOTIFICATION_SCHEDULER:-true}"
# Set APP_BASE_URL in recommendation_service/.env (e.g. https://job-scout.dev) for email footer links.

cd "$ROOT/recommendation_service"
exec "$VENV/bin/uvicorn" app.main:app --host 127.0.0.1 --port 8002 "$@"
