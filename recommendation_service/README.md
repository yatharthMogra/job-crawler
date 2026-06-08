# Recommendation Service

FastAPI service for job dashboard retrieval, pool subscriptions, and scheduled email notifications.

## Setup

Uses the shared repo-root virtualenv (`job-crawler/`). From the monorepo root:

```bash
./scripts/setup-env.sh
source job-crawler/bin/activate
cp recommendation_service/.env.example recommendation_service/.env
cd recommendation_service && alembic upgrade head
./scripts/dev-recommendation-service.sh
```

Requires the shared `jobingestion` PostgreSQL database with job ingestion and profile service migrations applied.

## APIs

- `GET /dashboard/jobs?candidate_id=...`
- `GET /dashboard/jobs/{job_id}?candidate_id=...`
- `POST /subscriptions`
- `GET /subscriptions/{candidate_id}`
- `PATCH /subscriptions/{candidate_id}`
- `POST /notifications/run` — manual notification pipeline trigger

## Migrations

Uses Alembic version table `alembic_version_recommendation`.
