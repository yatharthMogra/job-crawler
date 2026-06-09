#!/usr/bin/env bash
# Start Postgres + profile + recommendation + web for full local E2E testing.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT/job-crawler"

echo "==> 1. Postgres (Docker)"
cd "$ROOT/job_ingestion"
docker compose up -d postgres
echo "    Waiting for Postgres..."
for i in $(seq 1 30); do
  if docker compose exec -T postgres pg_isready -U postgres -d jobingestion >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

echo "==> 2. Python venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  PYTHON=""
  for candidate in python3.12 python3.11 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
      PYTHON="$candidate"
      break
    fi
  done
  [[ -n "$PYTHON" ]] || { echo "Need Python 3.11+"; exit 1; }
  "$PYTHON" -m venv "$VENV"
  "$VENV/bin/pip" install -e "$ROOT/.[dev]"
fi

echo "==> 3. Migrations"
cd "$ROOT/profile_service"
"$VENV/bin/alembic" upgrade head
cd "$ROOT/recommendation_service"
"$VENV/bin/alembic" upgrade head

echo "==> 4. Start backends (new terminals)"
echo "    Terminal A: $ROOT/scripts/dev-profile-service.sh"
echo "    Terminal B: $ROOT/scripts/dev-recommendation-service.sh"
echo "    Terminal C: cd $ROOT/web && npm run dev"
echo ""
echo "Set in web/.env.local:"
echo "  NEXT_PUBLIC_USE_MOCK_DATA=false"
echo "  NEXT_PUBLIC_PROFILE_API_KEY=dev-key-change-me"
echo ""
echo "Optional: add GEMINI_API_KEY to profile_service/.env for real resume parsing."
