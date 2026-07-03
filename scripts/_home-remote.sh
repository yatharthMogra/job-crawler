#!/usr/bin/env bash
# Shared config for remote home-machine ops from a dev Mac.
# shellcheck disable=SC2034

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

HOME_SSH_HOST="${HOME_SSH_HOST:-job-crawler-home}"
JOB_INGESTION_URL="${JOB_INGESTION_URL:-http://127.0.0.1:8000}"
NOTIFICATION_WORKER_URL="${NOTIFICATION_WORKER_URL:-http://127.0.0.1:8002}"

if [[ -f "$ROOT/deploy/home-remote.env" ]]; then
  # shellcheck source=/dev/null
  source "$ROOT/deploy/home-remote.env"
fi

home_remote_require_tunnel() {
  if ! curl -sf "${JOB_INGESTION_URL}/health" >/dev/null 2>&1; then
    echo "Cannot reach job ingestion at ${JOB_INGESTION_URL}/health" >&2
    echo "Start the tunnel in another terminal: ./scripts/tunnel-home-services.sh" >&2
    exit 1
  fi
}
