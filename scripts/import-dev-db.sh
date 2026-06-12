#!/usr/bin/env bash
# Restore a jobingestion database dump produced by export-dev-db.sh.
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <path-to.dump>"
  echo ""
  echo "Examples:"
  echo "  $0 exports/jobingestion-lite-2026-06-10.dump"
  echo "  $0 exports/jobingestion-full-2026-06-10.dump"
  exit 1
fi

DUMP_PATH="$1"
if [[ ! -f "$DUMP_PATH" ]]; then
  echo "Dump file not found: $DUMP_PATH"
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT/job-crawler"

PGUSER="${PGUSER:-postgres}"
PGDATABASE="${PGDATABASE:-jobingestion}"

IS_LITE=false
if [[ "$(basename "$DUMP_PATH")" == *-lite-* ]]; then
  IS_LITE=true
fi

echo "==> Starting Postgres"
cd "$ROOT/job_ingestion"
docker compose up -d postgres
for _ in $(seq 1 30); do
  if docker compose exec -T postgres pg_isready -U postgres >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

echo "==> Recreating database $PGDATABASE"
docker compose exec -T postgres psql -U "$PGUSER" -d postgres -c \
  "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$PGDATABASE' AND pid <> pg_backend_pid();" \
  >/dev/null || true
docker compose exec -T postgres dropdb -U "$PGUSER" --if-exists "$PGDATABASE"
docker compose exec -T postgres createdb -U "$PGUSER" "$PGDATABASE"

if $IS_LITE; then
  echo "==> Lite dump: creating schema via Alembic"
  if [[ ! -x "$VENV/bin/alembic" ]]; then
    echo "Lite imports require the repo venv. Run: ./scripts/setup-env.sh"
    exit 1
  fi
  cd "$ROOT/job_ingestion" && "$VENV/bin/alembic" upgrade head
  cd "$ROOT/profile_service" && "$VENV/bin/alembic" upgrade head
  cd "$ROOT/recommendation_service" && "$VENV/bin/alembic" upgrade head
fi

echo "==> Restoring $DUMP_PATH"
cd "$ROOT/job_ingestion"
CONTAINER_DUMP="/tmp/$(basename "$DUMP_PATH")"
docker compose cp "$DUMP_PATH" "postgres:$CONTAINER_DUMP"
RESTORE_ARGS=(--no-owner --no-privileges)
if $IS_LITE; then
  RESTORE_ARGS+=(--data-only --disable-triggers)
fi
docker compose exec -T postgres pg_restore -U "$PGUSER" -d "$PGDATABASE" \
  "${RESTORE_ARGS[@]}" "$CONTAINER_DUMP"
docker compose exec -T postgres rm -f "$CONTAINER_DUMP"

echo "==> Sanity check"
docker compose exec -T postgres psql -U "$PGUSER" -d "$PGDATABASE" -c "
SELECT 'companies' AS table_name, count(*) FROM companies
UNION ALL SELECT 'normalized_jobs_success', count(*) FROM normalized_jobs WHERE processing_state = 'success'
UNION ALL SELECT 'candidates_with_profile', count(DISTINCT candidate_id) FROM candidate_profiles
UNION ALL SELECT 'user_pool_subscriptions', count(*) FROM user_pool_subscriptions;
"

echo ""
echo "Done. Start services:"
echo "  ./scripts/dev-profile-service.sh"
echo "  ./scripts/dev-recommendation-service.sh"
echo ""
echo "Candidate IDs: see exports/manifest-*.json (recommended_candidates)."
