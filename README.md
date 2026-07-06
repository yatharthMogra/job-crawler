# Job Crawler Monorepo

Shared Python environment and backend services for job ingestion, candidate profiles, and recommendations.

## Python environment (one venv for all services)

From the repo root:

```bash
./scripts/setup-env.sh
source job-crawler/bin/activate
```

The virtualenv lives at `job-crawler/` (gitignored). Dependencies are defined in the root [`pyproject.toml`](pyproject.toml) — a union of all three backend services.

**Do not** use per-service venvs unless you have a specific reason. Each service still runs from its own directory (they all use an `app` package name).

## Run services

Use the helper scripts (recommended):

```bash
./scripts/dev-job-ingestion.sh          # http://localhost:8000
./scripts/dev-profile-service.sh      # http://localhost:8001
./scripts/dev-recommendation-service.sh  # http://localhost:8002
./scripts/dev-web.sh                     # http://localhost:3000 (unified dashboard + profile UI)
```

**Home machine on Linux, ops from Mac** (Tailscale + SSH tunnel — see [`deploy/TAILSCALE.md`](deploy/TAILSCALE.md) and [`DEPLOYMENT.md`](DEPLOYMENT.md) Phase 6.9):

```bash
# Tailscale connected on Mac and Linux (home machine: 100.111.129.27)
./scripts/tunnel-home-services.sh        # Terminal 1 — keep open
./scripts/home-health.sh                 # status via tunneled APIs
./scripts/home-trigger-ingestion.sh
./scripts/dev-ingestion-dashboard.sh     # internal ops UI → http://localhost:3000
```

Or manually after activating the venv:

```bash
cd job_ingestion && uvicorn app.main:app --port 8000 --reload
cd profile_service && uvicorn app.main:app --port 8001 --reload
cd recommendation_service && uvicorn app.main:app --port 8002 --reload
```

## Database snapshot (skip ingestion + enrichment)

To bootstrap from a shared dump instead of running the full pipeline:

```bash
./scripts/import-dev-db.sh exports/jobingestion-lite-YYYY-MM-DD.dump
```

See [`snapshots/README.md`](snapshots/README.md) for details. To create a new export:

```bash
./scripts/export-dev-db.sh
```

## Migrations

Each service has its own Alembic config and version table:

```bash
source job-crawler/bin/activate
cd job_ingestion && alembic upgrade head
cd profile_service && alembic upgrade head
cd recommendation_service && alembic upgrade head
```

## Tests

```bash
source job-crawler/bin/activate
cd job_ingestion && pytest
cd profile_service && pytest
cd recommendation_service && pytest
```

See [`testing.md`](testing.md) for end-to-end recommendation testing and [`web/README.md`](web/README.md) for the user-facing frontend.

See [`RECOMMENDATION_SYSTEM.md`](RECOMMENDATION_SYSTEM.md) for how personalized recommendations work end-to-end (architecture, filters, scoring, key files).

See [`DEPLOYMENT.md`](DEPLOYMENT.md) for hybrid cloud + home machine deployment (Supabase, Cloud Run, Vercel, Tailscale).

## Frontend apps

| App | Purpose |
|-----|---------|
| [`web/`](web/) | User-facing job dashboard + profile review (Career Match AI) |
| [`job-ingestion-dashboard/`](job-ingestion-dashboard/) | Internal ops dashboard for the job ingestion pipeline |
