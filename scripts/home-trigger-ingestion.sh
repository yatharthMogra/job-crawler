#!/usr/bin/env bash
set -euo pipefail
# shellcheck source=_home-remote.sh
source "$(dirname "$0")/_home-remote.sh"

home_remote_require_tunnel

echo "POST ${JOB_INGESTION_URL}/pipeline/trigger"
curl -sf -X POST "${JOB_INGESTION_URL}/pipeline/trigger"
echo ""
