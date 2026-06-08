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
```

Or manually after activating the venv:

```bash
cd job_ingestion && uvicorn app.main:app --port 8000 --reload
cd profile_service && uvicorn app.main:app --port 8001 --reload
cd recommendation_service && uvicorn app.main:app --port 8002 --reload
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

See [`testing.md`](testing.md) for end-to-end recommendation testing.
