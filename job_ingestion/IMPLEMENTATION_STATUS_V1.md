# Job Ingestion v1 Working State

This document is an outsider-friendly status snapshot of what has been implemented, validated, and learned during bring-up of the `job_ingestion` service.

## 1) Implemented features

### Core platform

- Python project with editable install support and dev dependency group.
- FastAPI service with startup/shutdown lifespan hooks.
- PostgreSQL persistence via Docker Compose.
- SQLAlchemy async DB layer and Alembic migration setup.

### Data model and ingestion

- Company, raw job, normalized job, pipeline run, and company-run-result models.
- Company seed flow from `data/companies.json`.
- Pipeline flow per active company:
  - fetch jobs from Greenhouse board API
  - classify as new/updated/unchanged/removed
  - write raw jobs
  - upsert normalized jobs
  - update run/company stats

### APIs

- Companies:
  - `GET /companies`
  - `GET /companies/{company_id}`
  - `PATCH /companies/{company_id}`
  - `POST /companies/seed`
- Pipeline:
  - `POST /pipeline/trigger`
  - `GET /pipeline/runs`
  - `GET /pipeline/runs/{run_id}`

### Run status semantics

Pipeline terminal run status now supports three outcomes:

- `completed` when all companies succeed
- `partial_success` when some succeed and some fail
- `failed` when all companies fail

### Alerting and failure tracking

- Each company tracks `consecutive_fetch_failures`.
- Failure alert records are appended to `alerts.json` when failures reach threshold (`MAX_CONSECUTIVE_FAILURES_BEFORE_ALERT`) and on subsequent failures.

### LLM integration

- LLM enrichment path is integrated.
- Gemini client migrated from deprecated `google.generativeai` to `google.genai`.
- HTML cleanup (`BeautifulSoup`) is applied before sending job text to LLM.

### Scheduling and logging

- APScheduler interval job is configured from `FETCH_CADENCE_HOURS`.
- Scheduler starts automatically during FastAPI startup and stops on shutdown.
- Structured logging is configured via `structlog` with JSON rendering when available.

## 2) Major issues encountered and resolved

### Issue A: Docker Postgres could not start on 5432

- Cause: local machine Postgres service already occupied host port 5432.
- Resolution: released/confined port conflict and brought Docker Postgres up.

### Issue B: Alembic migration failures (env + driver mismatch)

- Cause:
  - global Python/Alembic was being used instead of project venv
  - Alembic sync engine path was fed async URL (`+asyncpg`)
- Resolution:
  - standardized venv-pinned invocation (`job-crawler/bin/python -m ...`)
  - migration URL conversion for Alembic to sync driver (`+psycopg`)
  - added sync driver dependency
- Result: `alembic upgrade head` succeeds.

### Issue C: runtime `greenlet` missing for async SQLAlchemy session operations

- Cause: `greenlet` not installed in project deps.
- Resolution: add/install `greenlet`.
- Result: seed and runtime DB calls succeed in the async path.

### Issue D: OpenAI source returned Greenhouse 404

- Cause: OpenAI jobs are not on Greenhouse board token used (`openai`).
- Resolution:
  - added Greenhouse board source (`board_token: greenhouse`) via seed
  - kept OpenAI row but set `is_active=false`
- Result: pipeline now runs cleanly with valid active sources.

## 3) What has been validated

### Environment and startup

- venv and dependency installation validated.
- Uvicorn startup validated with venv interpreter.
- Scheduler startup observed in logs during app startup.

### Database and migrations

- Migration path validated against local Postgres.
- migration/env and driver compatibility validated.

### Manual API validation

- companies seed/list/patch paths verified.
- pipeline trigger/list/detail paths verified.
- repeated trigger runs verified with persisted historical runs.

### Pipeline behavior validation

- Mixed success/failure path verified as `partial_success`.
- All-success path verified as `completed` after data source correction.
- Rerun behavior validated (`jobs_unchanged` dominance after initial ingestion).

### Alerting validation

- `alerts.json` contains entries at threshold and beyond (e.g., consecutive failures 3 and 4).

### `consecutive_misses` end-to-end validation (stateful path)

This non-trivial stateful behavior has been manually validated end-to-end:

- test threshold used: `consecutive_misses_before_inactive = 2` (in test settings)
- run 1 result for targeted normalized job: `consecutive_misses=1`, `is_active=true`
- run 2 result for same job: `consecutive_misses=2`, `is_active=false`
- test mutation was restored back to original values afterward

### Automated tests

Targeted test suite passing includes:

- pipeline trigger API status behavior (including `partial_success`)
- terminal status resolution logic
- Gemini provider response parsing and exception wrapping

## 4) Current operational state

- Active companies are valid Greenhouse sources (`anthropic`, `greenhouse`).
- OpenAI record remains in DB but inactive to avoid expected source mismatch failures.
- Pipeline currently completes successfully with active sources.

## 5) Contributor notes

- Always use venv-pinned commands (`python -m ...`) to avoid global shim mismatches.
- Seeding keys on `board_token`; changing source tokens generally adds/updates by token, not by company name.
- If swapping out a source token, patch old company row inactive when appropriate.
- Use `alerts.json` and run detail endpoints as primary observability artifacts for failure behavior.
