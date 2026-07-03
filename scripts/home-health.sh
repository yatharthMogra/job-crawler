#!/usr/bin/env bash
set -euo pipefail
# shellcheck source=_home-remote.sh
source "$(dirname "$0")/_home-remote.sh"

home_remote_require_tunnel

json_get() {
  local json="$1"
  local path="$2"
  if command -v jq >/dev/null 2>&1; then
    echo "$json" | jq -r "$path"
  else
    echo "(install jq for formatted output)"
    return 1
  fi
}

echo "=== Home machine health @ $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo ""

# Ingestion
ingestion_health="$(curl -sf "${JOB_INGESTION_URL}/health")"
echo "job_ingestion (${JOB_INGESTION_URL}): ${ingestion_health}"

stats="$(curl -sf "${JOB_INGESTION_URL}/stats")"
if command -v jq >/dev/null 2>&1; then
  echo ""
  echo "--- /stats ---"
  echo "generated_at: $(json_get "$stats" '.generated_at')"
  echo "enrichment_workers: $(json_get "$stats" '.enrichment_workers')"
  echo "fetch_backpressure.active: $(json_get "$stats" '.fetch_backpressure.active')"
  echo "fetch_backpressure.depth: $(json_get "$stats" '.fetch_backpressure.depth')"
  echo "jobs.active: $(json_get "$stats" '.jobs.active')"
  echo "jobs.enriched: $(json_get "$stats" '.jobs.enriched')"
  echo "jobs.pending_enrichment: $(json_get "$stats" '.jobs.pending_enrichment')"
  echo "jobs.failed: $(json_get "$stats" '.jobs.failed')"
  echo "fetch.last_24h.pipeline_runs: $(json_get "$stats" '.fetch.last_24h.pipeline_runs')"
  echo "fetch.last_24h.jobs_new: $(json_get "$stats" '.fetch.last_24h.jobs_new')"
  latest_status="$(json_get "$stats" '.fetch.latest_run.status // "none"')"
  latest_started="$(json_get "$stats" '.fetch.latest_run.started_at // "n/a"')"
  echo "fetch.latest_run: status=${latest_status} started_at=${latest_started}"
  echo "enrichment.completed_last_5m: $(json_get "$stats" '.enrichment.completed_last_5m')"
  echo "enrichment.completed_last_1h: $(json_get "$stats" '.enrichment.completed_last_1h')"
  echo "enrichment.failed_last_1h: $(json_get "$stats" '.enrichment.failed_last_1h')"
else
  echo ""
  echo "--- /stats (raw) ---"
  echo "$stats"
fi

echo ""
echo "--- recent pipeline runs ---"
runs="$(curl -sf "${JOB_INGESTION_URL}/pipeline/runs?limit=5")"
if command -v jq >/dev/null 2>&1; then
  echo "$runs" | jq -r '.[] | "\(.started_at)  \(.status)  companies=\(.successful_companies)/\(.total_companies)  jobs_new=\(.jobs_new)"'
else
  echo "$runs"
fi

# Notification worker
echo ""
if worker_health="$(curl -sf "${NOTIFICATION_WORKER_URL}/health" 2>/dev/null)"; then
  echo "notification worker (${NOTIFICATION_WORKER_URL}): ${worker_health}"
else
  echo "notification worker (${NOTIFICATION_WORKER_URL}): unreachable"
  echo "  (tunnel must forward port 8002; see deploy/ssh/config.example)"
  exit 1
fi
