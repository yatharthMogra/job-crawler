#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/web"

if [[ ! -f .env.local && -f .env.example ]]; then
  echo "No .env.local found — copy .env.example and set NEXT_PUBLIC_PROFILE_API_KEY"
fi

exec pnpm dev
