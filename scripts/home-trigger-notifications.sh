#!/usr/bin/env bash
set -euo pipefail
# shellcheck source=_home-remote.sh
source "$(dirname "$0")/_home-remote.sh"

home_remote_require_tunnel

if ! curl -sf "${NOTIFICATION_WORKER_URL}/health" >/dev/null 2>&1; then
  echo "Cannot reach notification worker at ${NOTIFICATION_WORKER_URL}/health" >&2
  echo "Ensure tunnel forwards port 8002 (see deploy/ssh/config.example)" >&2
  exit 1
fi

echo "POST ${NOTIFICATION_WORKER_URL}/notifications/run"
curl -sf -X POST "${NOTIFICATION_WORKER_URL}/notifications/run"
echo ""
