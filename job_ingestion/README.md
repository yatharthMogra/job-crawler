# Job Ingestion

Multi-platform job ingestion service: fetch jobs from ATS boards, detect changes, normalize deterministically, and enrich asynchronously with Gemini. Runs on port **8000**.

Uses the shared repo-root Python env — see [`../README.md`](../README.md).

## Quick start

```bash
# from repo root
./scripts/dev-job-ingestion.sh
```

First-time setup:

```bash
cd job_ingestion
cp .env.example .env          # set DATABASE_URL, GEMINI_API_KEYS (or GEMINI_API_KEY for single worker)
alembic upgrade head
curl -X POST http://localhost:8000/companies/seed
curl -X POST http://localhost:8000/pipeline/trigger   # batch (due companies only)
```

## Architecture

```
APScheduler
  ├── fetch-tick (every tick_minutes)  → select due companies (shard + tier) → pipeline batch
  └── waas-fetch (every 30 min)        → WorkAtStartup only

Pipeline (per company)
  Fetch → Change detect → RawJob → Deterministic extract → NormalizedJob → Enrichment queue

EnrichmentWorkerPool (N workers, always on)
  Queue (partitioned by job id) → batched Gemini calls per key → update NormalizedJob
```

Ingestion and enrichment are **decoupled**. Fetch failures block a company run; enrichment failures do not roll back ingested jobs.

### Fetch scheduling

The scheduler no longer fetches every active company on each tick. Instead:

1. Each company has a **`fetch_tier`** (1, 2, or 3) in [`data/companies.json`](data/companies.json).
2. **`FETCH_SCHEDULE_JSON`** in `.env` defines how often each `(platform, tier)` should be checked, plus tick size and throttles.
3. On each tick, companies are selected if they are **due** (past their interval since `last_successful_fetch_at`) and their **shard** matches the current tick (deterministic spread by `board_token`).
4. WorkAtStartup runs on a **separate dedicated job** when `waas.dedicated_job` is true (default).

This spreads load across time, reduces ATS rate-limit risk, and keeps tier-1 boards fresher than tier-3 enterprise Workday tenants.

## Supported platforms

| Platform | Notes |
|----------|-------|
| `greenhouse` | Single API call per board (`content=true`) |
| `lever` | Single public postings API call |
| `ashby` | List + per-job detail (global host rate limit + incremental cache) |
| `workday` | List + incremental detail fetch |
| `oracle_hcm` | Paginated list + detail |
| `icims` | Sitemap + detail |
| `workable` | Public API |
| `workatastartup` | YC bulk source (dedicated schedule) |

See [`CONNECTOR_GUIDE.md`](CONNECTOR_GUIDE.md) for connector details.

## Company source of truth

[`data/companies.json`](data/companies.json) is the source of truth for companies.

```json
{
  "company": "Notion",
  "platform": "ashby",
  "board_token": "notion",
  "fetch_tier": 1,
  "is_active": true
}
```

| Field | Description |
|-------|-------------|
| `company` | Display name |
| `platform` | ATS connector key |
| `board_token` | Platform-specific identifier |
| `fetch_tier` | `1` = highest freshness priority, `3` = lowest |
| `is_active` | Whether to include in fetch runs |
| `platform_config` | Optional connector config (Workday tenant, careers URLs, etc.) |

Sync to database:

```bash
curl -X POST http://localhost:8000/companies/seed
```

Strict sync: companies in the DB but not in the file are deleted.

### Fetch tiers (guidance)

| Tier | Typical use |
|------|-------------|
| **1** | YC / WorkAtStartup, high-priority startups |
| **2** | Default for most Greenhouse, Lever, Ashby |
| **3** | Workday, Oracle HCM, ICIMS, large enterprise |

## Configuration

### `FETCH_SCHEDULE_JSON`

Single JSON object in `.env`. When unset, built-in defaults apply (10-minute tick, 200 company batch cap).

```json
{
  "tick_minutes": 10,
  "batch_cap": 200,
  "default_fetch_tier": 2,
  "waas": {
    "dedicated_job": true,
    "interval_minutes": 30
  },
  "intervals": {
    "workatastartup": {"1": 30},
    "greenhouse": {"1": 45, "2": 180, "3": 720},
    "lever": {"1": 45, "2": 180, "3": 720},
    "ashby": {"1": 120, "2": 480, "3": 1440},
    "workday": {"1": 240, "2": 720, "3": 2880},
    "oracle_hcm": {"1": 360, "2": 1440, "3": 2880},
    "icims": {"1": 360, "2": 1440, "3": 2880},
    "workable": {"1": 180, "2": 720, "3": 1440}
  },
  "throttles": {
    "default_concurrency": 8,
    "platforms": {
      "ashby": {"concurrency": 1, "inter_company_seconds": 3},
      "workday": {"concurrency": 3, "inter_company_seconds": 1},
      "oracle_hcm": {"concurrency": 2},
      "icims": {"concurrency": 1}
    }
  }
}
```

| Key | Meaning |
|-----|---------|
| `tick_minutes` | Scheduler wake interval |
| `batch_cap` | Max companies per tick |
| `default_fetch_tier` | Used when `fetch_tier` omitted from companies.json |
| `intervals` | Minutes between fetches per `(platform, tier)` |
| `throttles` | Per-platform concurrency and post-fetch cooldown |

Shard count is derived: `ceil(interval / tick_minutes)`.

### Fetch backpressure

When pending enrichment work (`queued` + `cooldown` + `in_progress`) reaches the threshold, fetch ingress is throttled so enrichment can catch up.

| Variable | Default | Meaning |
|----------|---------|---------|
| `FETCH_BACKPRESSURE_ENABLED` | `true` | Master switch |
| `FETCH_BACKPRESSURE_QUEUE_THRESHOLD` | `2000` | Activate when pending depth >= this |
| `FETCH_BACKPRESSURE_MODE` | `skip_tiers` | `skip_tiers` or `halt_all` |
| `FETCH_BACKPRESSURE_SKIP_TIERS` | `3` | Tiers excluded in `skip_tiers` mode |
| `FETCH_BACKPRESSURE_ALLOW_WAAS` | `true` | Keep WAAS dedicated job under `halt_all` |

In `skip_tiers` mode (default), tier-3 companies are dropped from the batch while tier 1/2 continue. In `halt_all` mode, scheduled fetch ticks run no companies unless they are WorkAtStartup and `ALLOW_WAAS` is true.

`GET /stats` includes `fetch_backpressure.active` and current queue depth. Pipeline runs record backpressure details in `schedule_metadata`.

Manual backfills that must ignore backpressure: `POST /pipeline/trigger?scope=full&force=true`.

### `JOB_MAX_AGE_DAYS`

Single freshness window for the active job corpus (default `7`). Must match `JOB_MAX_AGE_DAYS` in `recommendation_service/.env`.

| Stage | Layer | Effect |
|-------|-------|--------|
| 1 | Fetch (all connectors) | Skip jobs with verifiably stale `posted_at` before pipeline |
| 2a | Pipeline | Skip DB write / enrichment queue for stale jobs that slip through fetch |
| 2b | Pre-enrichment | Purge stale jobs before Gemini calls |
| 3 | Post-enrichment | Purge if posting date becomes verifiably stale after enrichment |
| 4 | Nightly cleanup (2 AM) | Delete any remaining jobs with `posted_at` older than N days (active or inactive) |
| — | Recommendation emails | Only jobs posted within N days (recommendation service) |

Jobs with unknown posting dates pass stages 1–3 and are not removed by cleanup (v1).

### Enrichment (N-worker pool)

Enrichment runs in-process as a pool of workers, each with its own Gemini API key. Queue rows are partitioned by `normalized_job_id` so workers do not claim the same jobs.

| Variable | Meaning |
|----------|---------|
| `GEMINI_API_KEYS` | Comma-separated API keys (primary config) |
| `GEMINI_API_KEY` | Fallback for a single worker when `GEMINI_API_KEYS` is unset |
| `ENRICHMENT_WORKER_COUNT` | Optional cap; defaults to number of keys |
| `ENRICHMENT_LLM_MAX_RPM` | Per-worker RPM cap (total throughput ≈ N × this value) |

Other tuning: `ENRICHMENT_MAX_JOBS_PER_WINDOW`, `ENRICHMENT_MICRO_BATCH_SIZE`, etc. See [`.env.example`](.env.example).

Ashby fetch tuning: `ASHBY_HOST_RATE_PER_SECOND`, `ASHBY_HOST_BURST`, `ASHBY_FULL_REFRESH_DAYS`.

Reset stuck queue rows: `POST /maintenance/enrichment/reset-stuck`

Monitor `enrichment_queue` depth via `GET /stats` (`fetch_backpressure.active`). Tune `FETCH_BACKPRESSURE_QUEUE_THRESHOLD` or tier assignments if enrichment falls behind.

## API surface

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/pipeline/trigger` | Run due batch (default) |
| `POST` | `/pipeline/trigger?company_id={uuid}` | Fetch one company by ID |
| `POST` | `/pipeline/trigger?scope=full` | Fetch all active companies (backfill) |
| `POST` | `/pipeline/trigger?scope=full&force=true` | Full fetch ignoring enrichment backpressure |
| `GET` | `/pipeline/runs` | List pipeline runs |
| `GET` | `/pipeline/runs/{id}` | Run detail + per-company results |
| `POST` | `/companies/seed` | Sync from companies.json |
| `GET` | `/companies` | List companies (includes `fetch_tier`) |
| `PATCH` | `/companies/{id}` | Update company (including `fetch_tier`) |
| `GET` | `/jobs` | List/filter normalized jobs |
| `GET` | `/stats` | Aggregate ops snapshot (fetch + enrichment stats) |
| `GET` | `/enrichments/usage` | LLM cost usage |
| `POST` | `/maintenance/enrichment/reset-stuck` | Re-queue failed/quota_blocked enrichment rows |

Swagger UI: `http://localhost:8000/docs`

## Operations

### Manual fetch

```bash
# Due companies only (same as scheduled tick)
curl -X POST http://localhost:8000/pipeline/trigger

# One company (lookup id via GET /companies)
curl -X POST 'http://localhost:8000/pipeline/trigger?company_id=61d1676b-c381-499c-bebd-61813b76e571&force=true'

# All active companies
curl -X POST 'http://localhost:8000/pipeline/trigger?scope=full'
```

### Monitoring freshness

- **`GET /stats`** — live aggregate snapshot (jobs, fetch 24h, enrichment queue, recent company polls)
- **`exports/ingestion_stats.json`** — same snapshot written on startup, after each pipeline run, and every 5 minutes (configurable via `INGESTION_STATS_INTERVAL_MINUTES`)
- Structured log line `ingestion_stats {...}` on each publish (stdout)
- `companies.last_successful_fetch_at` — last successful fetch per company
- `pipeline_runs.schedule_metadata` — tick, batch cap, companies due/selected per run
- Enrichment queue: `SELECT status, COUNT(*) FROM enrichment_queue GROUP BY status`

### Production (home machine)

See [`../DEPLOYMENT.md`](../DEPLOYMENT.md) Phase 6. Run via `./scripts/run-job-ingestion-prod.sh`.

## Related docs

- [`CONNECTOR_GUIDE.md`](CONNECTOR_GUIDE.md) — connector interface and platform notes
- [`IMPLEMENTATION_STATUS_V2.md`](IMPLEMENTATION_STATUS_V2.md) — feature status snapshot
- [`../DEPLOYMENT.md`](../DEPLOYMENT.md) — production deployment
