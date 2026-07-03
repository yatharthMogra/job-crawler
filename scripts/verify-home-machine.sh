#!/usr/bin/env bash
# Run on the Linux home machine to verify systemd services and local health endpoints.
set -euo pipefail

fail=0

check_unit() {
  local unit="$1"
  if systemctl is-active --quiet "$unit"; then
    echo "OK  systemd ${unit} is active"
  else
    echo "FAIL systemd ${unit} is not active" >&2
    systemctl status "$unit" --no-pager -l || true
    fail=1
  fi
}

check_health() {
  local name="$1"
  local url="$2"
  if response="$(curl -sf "$url" 2>/dev/null)"; then
    echo "OK  ${name}: ${response}"
  else
    echo "FAIL ${name}: no response from ${url}" >&2
    fail=1
  fi
}

echo "=== Home machine verification @ $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo ""

if ! command -v systemctl >/dev/null 2>&1; then
  echo "WARN systemctl not found — skipping unit checks" >&2
else
  check_unit job-ingestion
  check_unit recommendation-worker
fi

echo ""
check_health "job_ingestion" "http://127.0.0.1:8000/health"
check_health "notification_worker" "http://127.0.0.1:8002/health"

echo ""
if [[ -f job_ingestion/.env ]]; then
  echo "OK  job_ingestion/.env exists"
else
  echo "FAIL job_ingestion/.env missing" >&2
  fail=1
fi

if [[ -f recommendation_service/.env ]]; then
  echo "OK  recommendation_service/.env exists"
else
  echo "FAIL recommendation_service/.env missing" >&2
  fail=1
fi

echo ""
if [[ "$fail" -eq 0 ]]; then
  echo "All checks passed."
else
  echo "Some checks failed. See deploy/systemd/ and DEPLOYMENT.md Phase 6." >&2
  exit 1
fi
