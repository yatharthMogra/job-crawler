#!/usr/bin/env bash
set -euo pipefail
# shellcheck source=_home-remote.sh
source "$(dirname "$0")/_home-remote.sh"

echo "Forwarding local ports to home machine via ${HOME_SSH_HOST}:"
echo "  ${JOB_INGESTION_URL} -> job_ingestion"
echo "  ${NOTIFICATION_WORKER_URL} -> notification worker"
echo ""
echo "Keep this terminal open. Press Ctrl+C to disconnect."
echo "In another terminal: ./scripts/home-health.sh"
exec ssh -N "$HOME_SSH_HOST"
