#!/usr/bin/env bash
# Export the shared jobingestion Postgres database for local dev bootstrap.
# Produces a full dump, a lite data-only dump, and manifest.json.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXPORT_DIR="${EXPORT_DIR:-$ROOT/exports}"
DATE_TAG="$(date -u +%Y-%m-%d)"

PGUSER="${PGUSER:-postgres}"
PGDATABASE="${PGDATABASE:-jobingestion}"

FULL_NAME="jobingestion-full-${DATE_TAG}.dump"
LITE_NAME="jobingestion-lite-${DATE_TAG}.dump"

# Lite = data only for tables needed to run recommendations (schema from Alembic on import).
LITE_DATA_TABLES=(
  companies
  raw_jobs
  normalized_jobs
  candidates
  candidate_resumes
  candidate_profiles
  candidate_capabilities
  candidate_evidence
  candidate_patches
  user_pool_subscriptions
)

mkdir -p "$EXPORT_DIR"

echo "==> Ensuring Postgres is up"
cd "$ROOT/job_ingestion"
docker compose up -d postgres >/dev/null
for _ in $(seq 1 30); do
  if docker compose exec -T postgres pg_isready -U postgres -d jobingestion >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

docker_pg_dump() {
  local out_file="$1"
  shift
  docker compose exec -T postgres pg_dump -Fc -U "$PGUSER" -d "$PGDATABASE" "$@" >"$out_file"
}

echo "==> Exporting full database to $EXPORT_DIR/$FULL_NAME"
docker_pg_dump "$EXPORT_DIR/$FULL_NAME"

echo "==> Exporting lite data-only dump to $EXPORT_DIR/$LITE_NAME"
LITE_ARGS=(--data-only --disable-triggers)
for table in "${LITE_DATA_TABLES[@]}"; do
  LITE_ARGS+=(-t "$table")
done
docker_pg_dump "$EXPORT_DIR/$LITE_NAME" "${LITE_ARGS[@]}"

echo "==> Writing manifest"
GIT_COMMIT="$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
GIT_BRANCH="$(git -C "$ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"

MANIFEST="$EXPORT_DIR/manifest-${DATE_TAG}.json"
python3 - "$MANIFEST" "$EXPORT_DIR/$FULL_NAME" "$EXPORT_DIR/$LITE_NAME" "$GIT_COMMIT" "$GIT_BRANCH" "$ROOT/job_ingestion" <<'PY'
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

manifest_path, full_path, lite_path, git_commit, git_branch, compose_dir = sys.argv[1:7]

def docker_psql(sql: str) -> list[str]:
    result = subprocess.run(
        ["docker", "compose", "exec", "-T", "postgres", "psql", "-U", "postgres", "-d", "jobingestion", "-t", "-A", "-c", sql],
        capture_output=True,
        text=True,
        check=True,
        cwd=compose_dir,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def query_one(sql: str, default: str = "0") -> str:
    try:
        rows = docker_psql(sql)
        return rows[0] if rows else default
    except subprocess.CalledProcessError:
        return default


def file_meta(path: str) -> dict:
    p = Path(path)
    return {
        "path": str(p),
        "filename": p.name,
        "bytes": p.stat().st_size,
        "sha256": subprocess.check_output(["shasum", "-a", "256", str(p)], text=True).split()[0],
    }


alembic = {}
for table, key in [
    ("alembic_version", "job_ingestion"),
    ("alembic_version_profile", "profile_service"),
    ("alembic_version_recommendation", "recommendation_service"),
]:
    alembic[key] = query_one(f"SELECT version_num FROM {table}")

counts = {}
for label, sql in [
    ("companies", "SELECT count(*) FROM companies"),
    ("normalized_jobs", "SELECT count(*) FROM normalized_jobs"),
    ("normalized_jobs_success", "SELECT count(*) FROM normalized_jobs WHERE processing_state = 'success'"),
    ("raw_jobs", "SELECT count(*) FROM raw_jobs"),
    ("candidates", "SELECT count(*) FROM candidates"),
    ("candidate_profiles", "SELECT count(*) FROM candidate_profiles"),
    ("candidate_capabilities", "SELECT count(*) FROM candidate_capabilities"),
    ("user_pool_subscriptions", "SELECT count(*) FROM user_pool_subscriptions"),
]:
    counts[label] = int(query_one(sql))

candidates = []
for row in docker_psql(
    "SELECT id::text, email, name FROM candidates "
    "WHERE email IN ('alice.dev@example.com', 'bob.fullstack@example.com', "
    "'yatharthmogra@gmail.com', 'ramparekh208@gmail.com') "
    "ORDER BY email"
):
    cid, email, name = row.split("|", 2)
    candidates.append({"id": cid, "email": email, "name": name})

lite_tables = [
    "companies", "raw_jobs", "normalized_jobs",
    "candidates", "candidate_resumes", "candidate_profiles",
    "candidate_capabilities", "candidate_evidence", "candidate_patches",
    "user_pool_subscriptions",
]

manifest = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "git_commit": git_commit,
    "git_branch": git_branch,
    "database": "jobingestion",
    "alembic_heads": alembic,
    "row_counts": counts,
    "recommended_candidates": candidates,
    "dumps": {
        "full": file_meta(full_path),
        "lite": file_meta(lite_path),
    },
    "lite_includes_data_only": lite_tables,
    "import": "./scripts/import-dev-db.sh exports/jobingestion-lite-YYYY-MM-DD.dump",
    "notes": [
        "Full dump: schema + all data — import without running migrations.",
        "Lite dump: data only for job index + profiles — import runs Alembic first.",
        "Resume PDF files are not included; profile rows reference local paths only.",
        "Contains real user emails — distribute privately.",
    ],
}

Path(manifest_path).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {manifest_path}")
PY

echo ""
echo "Export complete:"
ls -lh "$EXPORT_DIR/$FULL_NAME" "$EXPORT_DIR/$LITE_NAME" "$MANIFEST"
echo ""
echo "Share the lite dump (smaller) for most dev setups:"
echo "  exports/$LITE_NAME"
echo ""
echo "Import on another machine:"
echo "  ./scripts/import-dev-db.sh exports/$LITE_NAME"
