#!/usr/bin/env bash
# Fetch C3.ai jobs into DB, then enrich via parallel Gemini workers (no built-in worker).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=_venv.sh
source "$ROOT/scripts/_venv.sh"

BOARD_TOKEN="${1:-c3ai}"
KEYS_ENV="${PARALLEL_GEMINI_ENV_FILE:-$ROOT/scripts/parallel_gemini_drain.env}"

echo "==> Waiting for Docker (start Docker Desktop if needed)..."
if ! docker ps >/dev/null 2>&1; then
  open -a Docker 2>/dev/null || open -a "Docker Desktop" 2>/dev/null || true
fi
for _ in $(seq 1 150); do
  if docker ps >/dev/null 2>&1; then
    break
  fi
  sleep 2
done
docker ps >/dev/null 2>&1 || {
  echo "Docker is not running. Open Docker Desktop, wait until it is ready, then rerun:"
  echo "  ./scripts/ingest_c3ai_parallel_enrich.sh c3ai"
  exit 1
}

echo "==> Postgres"
cd "$ROOT/job_ingestion"
docker compose up -d postgres
for _ in $(seq 1 45); do
  if docker compose exec -T postgres pg_isready -U postgres -d jobingestion >/dev/null 2>&1; then
    break
  fi
  sleep 1
done
docker compose exec -T postgres pg_isready -U postgres -d jobingestion

if [[ ! -f .env ]]; then
  cp .env.example .env
fi

echo "==> Migrations"
"$VENV/bin/alembic" upgrade head

echo "==> Fetch $BOARD_TOKEN (pipeline only — no built-in enrichment drain)"
"$VENV/bin/python" << PY
import asyncio
import json
from pathlib import Path

from sqlalchemy import text

from app.config import Settings
from app.database import AsyncSessionLocal
from app.ingestion.pipeline import run_pipeline
from app.utils.seed import seed_companies

ROOT = Path("$ROOT")
COMPANIES_JSON = ROOT / "job_ingestion" / "data" / "companies.json"
TOKEN = "$BOARD_TOKEN"

async def main() -> None:
    payload = json.loads(COMPANIES_JSON.read_text(encoding="utf-8"))
    json_active = {
        item["board_token"]
        for item in payload
        if item.get("board_token") and item.get("is_active", True)
    }
    if TOKEN not in json_active:
        raise SystemExit(f"Unknown or inactive board_token: {TOKEN}")

    async with AsyncSessionLocal() as db:
        seed = await seed_companies(db)
        print("seed:", seed)
        await db.execute(
            text("UPDATE companies SET is_active = (board_token = :token)"),
            {"token": TOKEN},
        )
        await db.commit()
        active_count = await db.scalar(text("SELECT COUNT(*) FROM companies WHERE is_active"))
        print(f"fetch_scope: active_companies={active_count} token={TOKEN}")

    settings = Settings()
    async with AsyncSessionLocal() as db:
        snapshot = await run_pipeline(db=db, run_type="manual", settings=settings)
        print("pipeline:", snapshot.__dict__)

    async with AsyncSessionLocal() as db:
        await seed_companies(db)
        row = (
            await db.execute(
                text(
                    """
                    SELECT
                      COUNT(nj.id) AS total_jobs,
                      COUNT(*) FILTER (WHERE eq.status IN ('queued','cooldown','in_progress')) AS queue_pending
                    FROM companies c
                    LEFT JOIN normalized_jobs nj ON nj.company_id = c.id AND nj.is_active
                    LEFT JOIN enrichment_queue eq ON eq.normalized_job_id = nj.id
                    WHERE c.board_token = :token
                    """
                ),
                {"token": TOKEN},
            )
        ).one()
        print(f"after_fetch: total_jobs={row.total_jobs} queue_pending={row.queue_pending}")

asyncio.run(main())
PY

if [[ ! -f "$KEYS_ENV" ]]; then
  echo "Missing $KEYS_ENV — copy from parallel_gemini_drain.env.example"
  exit 1
fi

echo "==> Parallel Gemini enrichment (4 workers from $KEYS_ENV)"
echo "    Ensure job_ingestion API is NOT running on :8000 (avoids queue contention)."
if lsof -i :8000 >/dev/null 2>&1; then
  echo "WARNING: port 8000 in use — stop dev-job-ingestion.sh before drain competes for queue rows."
fi

cd "$ROOT"
"$VENV/bin/python" scripts/parallel_gemini_drain_today.py \
  --launch-all \
  --reset-stuck \
  --worker-count 4

echo "==> Done. Check status:"
"$VENV/bin/python" scripts/parallel_gemini_drain_status.py
