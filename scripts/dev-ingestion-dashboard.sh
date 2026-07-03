#!/usr/bin/env bash
set -euo pipefail
# shellcheck source=_home-remote.sh
source "$(dirname "$0")/_home-remote.sh"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/job-ingestion-dashboard"

home_remote_require_tunnel

if [[ ! -f .env.local ]]; then
  if [[ -f .env.example ]]; then
    cp .env.example .env.local
    echo "Created .env.local from .env.example"
  else
    echo 'NEXT_PUBLIC_JOB_INGESTION_API_URL=http://127.0.0.1:8000' > .env.local
    echo "Created .env.local with default API URL"
  fi
fi

if [[ -f pnpm-lock.yaml ]] && command -v pnpm >/dev/null 2>&1; then
  exec pnpm dev
fi

exec npm run dev
