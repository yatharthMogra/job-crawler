**Short answer:** There is no single “7,269 / 7,269 complete” progress bar. Ingestion is a **scheduled, batched pipeline** (~200 companies per 10‑minute tick, with sharding and tier intervals), so after one morning you’ve only touched a fraction of the list. `GET /stats` is the high-level health view; for “what’s working, what’s dead, domains, pools, locations” you need **pipeline run details + DB queries + a few scripts**.

---

## Why it’s still running (and what “done” means)

You don’t run “ingest all 7,269 once.” The scheduler does:

1. Every **10 minutes** (default), pick up to **`batch_cap` = 200** companies that are **due**
2. **Shard** by platform/tier so not every due company runs every tick
3. Optionally **skip tier 3** when enrichment backpressure is active

Never-fetched companies are **prioritized** (`last_successful_fetch_at IS NULL` sorts first), but with 7k+ boards, first contact still spreads over **many hours/days**, not one morning.

So “done” per company means:

- `last_successful_fetch_at` is set (fetch attempted successfully at least once)
- Optionally: has active jobs in `normalized_jobs`
- Optionally: jobs enriched (`processing_state = 'success'`) with `job_domain`, `retrieval_pools`, etc.

---

## What you already have (beyond `/stats`)

### 1. `GET /stats` — aggregate snapshot

```bash
curl -s http://localhost:8000/stats | jq
```

Also written to `exports/ingestion_stats.json` every ~5 minutes.

Useful fields:

| Section | What it tells you |
|--------|-------------------|
| `jobs` | Active / enriched / pending / failed job counts |
| `fetch.last_24h` | Rollup across all pipeline runs today |
| `fetch.latest_run` | Last batch only (~200 companies max) |
| `recent_company_polls` | Last **40** companies fetched (not full picture) |
| `fetch_backpressure` | Whether tier‑3 fetches are being skipped |
| `enrichment.queue` | Enrichment backlog |

**Limitation:** No per-platform breakdown, no “never fetched vs fetched,” no domains/pools.

---

### 2. `scripts/full_ingest_enrich_status.py` — better CLI summary

```bash
python scripts/full_ingest_enrich_status.py
```

Prints:

- `companies: active=X with_jobs=Y awaiting_first_fetch=Z` ← **closest built-in “progress” metric**
- Job enrichment %, domain %, role_intent %, queue depth
- Latest pipeline run success/fail counts

`awaiting_first_fetch` = active companies with **zero** active jobs (includes never-fetched + fetched-but-empty boards).

---

### 3. Pipeline APIs — per-run company detail

```bash
# Last 20 runs
curl -s 'http://localhost:8000/pipeline/runs?limit=20' | jq

# One run: every company in that batch + error_message
curl -s 'http://localhost:8000/pipeline/runs/<RUN_ID>' | jq
```

Each scheduled tick ≈ one run with `total_companies` ≤ 200. Expand a run in the **job-ingestion dashboard → Pipeline tab** for the same data.

`company_run_results` stores per company: `status`, `jobs_fetched`, `jobs_new`, `error_message`.

---

### 4. Companies API — health per source (paginated)

```bash
curl -s 'http://localhost:8000/companies?include_job_counts=true&limit=500&offset=0' | jq
```

Fields: `consecutive_fetch_failures`, `last_successful_fetch_at`, `last_failure_at`, `active_jobs_count`, `is_active`, `requires_review`.

**Limitation:** `limit` max **500**; dashboard Sources tab only loads **200**. For 7k companies you need pagination or SQL.

---

### 5. Events API — failures and warnings

```bash
curl -s 'http://localhost:8000/events?category=source&severity=error&limit=100' | jq
curl -s 'http://localhost:8000/events/summary' | jq
```

Filter by `platform`, `company_id`, `since`.

---

### 6. Jobs API — browse enriched jobs (not aggregate stats)

```bash
curl -s 'http://localhost:8000/jobs?platform=greenhouse&processing_state=success&limit=100' | jq
```

Good for spot-checking titles/locations; not for rollup by domain/pool (use SQL below).

---

## SQL for the detail you want (run against `jobingestion` DB)

Connect however you usually do (psql, TablePlus, etc.).

### Fetch progress: who’s been touched?

```sql
-- Overall company fetch state
SELECT
  COUNT(*) FILTER (WHERE is_active) AS active_companies,
  COUNT(*) FILTER (WHERE is_active AND last_successful_fetch_at IS NULL) AS never_fetched,
  COUNT(*) FILTER (WHERE is_active AND last_successful_fetch_at IS NOT NULL) AS fetched_at_least_once,
  COUNT(*) FILTER (WHERE is_active AND consecutive_fetch_failures > 0) AS with_failures,
  COUNT(*) FILTER (WHERE is_active AND consecutive_fetch_failures >= 3) AS likely_broken,
  COUNT(*) FILTER (
    WHERE is_active AND EXISTS (
      SELECT 1 FROM normalized_jobs nj
      WHERE nj.company_id = companies.id AND nj.is_active
    )
  ) AS companies_with_jobs,
  COUNT(*) FILTER (
    WHERE is_active AND NOT EXISTS (
      SELECT 1 FROM normalized_jobs nj
      WHERE nj.company_id = companies.id AND nj.is_active
    )
  ) AS companies_without_jobs
FROM companies;
```

### By platform

```sql
SELECT
  platform,
  COUNT(*) FILTER (WHERE is_active) AS active,
  COUNT(*) FILTER (WHERE is_active AND last_successful_fetch_at IS NULL) AS never_fetched,
  COUNT(*) FILTER (WHERE is_active AND consecutive_fetch_failures > 0) AS failing,
  COUNT(*) FILTER (
    WHERE is_active AND EXISTS (
      SELECT 1 FROM normalized_jobs nj WHERE nj.company_id = companies.id AND nj.is_active
    )
  ) AS with_jobs,
  SUM((
    SELECT COUNT(*) FROM normalized_jobs nj
    WHERE nj.company_id = companies.id AND nj.is_active
  )) AS total_active_jobs
FROM companies
GROUP BY platform
ORDER BY active DESC;
```

### Broken boards (likely CC junk)

```sql
SELECT name, platform, board_token, consecutive_fetch_failures,
       last_failure_at, last_successful_fetch_at
FROM companies
WHERE is_active AND consecutive_fetch_failures >= 3
ORDER BY consecutive_fetch_failures DESC, last_failure_at DESC NULLS LAST
LIMIT 100;
```

### Fetched today (since ~5am — adjust timestamp)

```sql
SELECT COUNT(*) AS companies_fetched_today
FROM companies
WHERE is_active
  AND last_successful_fetch_at >= '2026-06-22 05:00:00+00';
```

### Job domains, pools, locations (enriched jobs only)

```sql
-- Domains
SELECT job_domain, COUNT(*) AS jobs
FROM normalized_jobs
WHERE is_active AND processing_state = 'success'
GROUP BY job_domain
ORDER BY jobs DESC;

-- Retrieval pools (unnest array)
SELECT pool, COUNT(*) AS jobs
FROM normalized_jobs nj, UNNEST(nj.retrieval_pools) AS pool
WHERE nj.is_active AND nj.processing_state = 'success'
GROUP BY pool
ORDER BY jobs DESC;

-- Countries
SELECT job_country, COUNT(*) AS jobs
FROM normalized_jobs
WHERE is_active AND processing_state = 'success'
GROUP BY job_country
ORDER BY jobs DESC;

-- Early career signals
SELECT
  COUNT(*) FILTER (WHERE is_new_grad) AS new_grad,
  COUNT(*) FILTER (WHERE is_internship) AS internship,
  COUNT(*) FILTER (WHERE role_intent IS NOT NULL) AS has_role_intent
FROM normalized_jobs
WHERE is_active AND processing_state = 'success';
```

### Enrichment pipeline lag

```sql
SELECT processing_state, COUNT(*)
FROM normalized_jobs
WHERE is_active
GROUP BY processing_state;

SELECT status, COUNT(*)
FROM enrichment_queue
GROUP BY status;
```

---

## Heavy audit: live-fetch every company

`scripts/platform_fetch_split.py` probes **every** active company in `companies.json` and writes:

`exports/platform_fetch_split.json` — per-platform OK/fail/timeout + job counts.

**Warning:** This is a **live** fetch of all boards (hours for 7k+, not the same as scheduled ingestion). Use for a one-off health audit, not normal monitoring.

```bash
python scripts/platform_fetch_split.py --concurrency 8 --timeout-s 120
```

---

## Practical monitoring workflow

| Question | Where to look |
|----------|----------------|
| Is the service healthy? | `GET /stats`, `exports/ingestion_stats.json` |
| How many companies still never fetched? | `full_ingest_enrich_status.py` or SQL above |
| What happened in the last batch? | `GET /pipeline/runs` → expand run |
| Which companies are failing? | SQL on `consecutive_fetch_failures`, or `/events` |
| Domains / pools / locations? | SQL on `normalized_jobs` (after enrichment) |
| UI | job-ingestion dashboard (Pipeline + Sources; Sources capped at 200) |

---

## Expectations with 7,269 companies

Many CC-discovered boards will:

- Fetch **0 jobs** (empty/dead)
- **Fail** (`consecutive_fetch_failures` increments)
- Produce jobs that **fail enrichment** or never match your early-career pools

That’s normal. The useful follow-up is SQL to find `companies_without_jobs` + high `consecutive_fetch_failures`, then set `is_active: false` in `companies.json` and re-seed.

If you want a single “ingestion progress report” script that runs all these SQL rollups to a JSON/CSV file, switch to Agent mode and we can add it.