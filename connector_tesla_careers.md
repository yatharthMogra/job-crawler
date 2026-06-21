# Tesla Careers Connector — Integration Guide

## Overview

Tesla's careers site (`tesla.com/careers/search`) is a client-rendered React SPA backed by
JSON APIs under `/cua-api/`. The search UI filters a preloaded global job catalog
client-side; there is **no paginated search API**.

**Implementation:** [`job_ingestion/app/ingestion/connectors/tesla_careers.py`](job_ingestion/app/ingestion/connectors/tesla_careers.py)

**Ingestion mode:** Manual browser bridge (push-only). Automated fetch is blocked by Akamai;
see [`tesla_akamai_troubleshooting_log.md`](../tesla_akamai_troubleshooting_log.md) for history.

---

## Confirmed API

### List catalog — single global payload

```
GET https://www.tesla.com/cua-api/apps/careers/state
Accept: application/json
```

Response shape:

```json
{
  "lookup": { "locations": {...}, "departments": {...}, "sites": {...} },
  "geo": [...],
  "listings": [
    { "id": "224501", "t": "AI Engineer...", "l": "401022", "dp": "5", "y": 1 }
  ]
}
```

Site filtering (`site=US` → ~4,387 jobs) is replicated server-side via `filter_listings_by_site()`.

### Job detail — required for new postings

```
GET https://www.tesla.com/cua-api/careers/job/{id}
```

Detail fields feed `build_tesla_careers_html()` → `raw_html` → enrichment pipeline.

---

## Manual Browser Bridge Architecture

```
You, in real Chrome
    → Tampermonkey userscript (scripts/tesla_careers_bridge.user.js)
    → fetch state + detail APIs (same-origin, your session)
    → POST /ingest/tesla/plan and /ingest/tesla/push (localhost:8000)
    → process_company_raw_jobs() → enrichment → scoring
```

### Setup (one-time)

1. Install [Tampermonkey](https://www.tampermonkey.net/)
2. Copy [`scripts/tesla_careers_bridge.user.js`](../scripts/tesla_careers_bridge.user.js) into a new userscript
3. Ensure job-ingestion is running on `localhost:8000`
4. Optionally set `TESLA_INGEST_TOKEN` in `.env` and matching `INGEST_TOKEN` in the userscript

### Operating routine

1. Open `https://www.tesla.com/careers/search/?site=US`
2. Wait for job results to render (script auto-runs, or click **Push to ingestion**)
3. First run: ~4,400 detail fetches at 300ms ≈ 20–25 minutes
4. Subsequent runs: only new job IDs are detail-fetched (seconds to minutes)
5. Repeat every 2–4 hours

### Ingestion API

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/ingest/tesla/known-ids` | External IDs already in DB |
| `POST` | `/ingest/tesla/plan` | `{ "state": {...} }` → pending detail IDs for configured sites |
| `POST` | `/ingest/tesla/push` | `{ "state": {...}, "details": [...] }` → run pipeline |

Optional header: `X-Ingest-Token` when `TESLA_INGEST_TOKEN` is set.

---

## platform_config

```json
{
  "sites": ["US"],
  "ingestion_mode": "manual_push",
  "expected_push_interval_hours": 4
}
```

| Key | Default | Purpose |
|---|---|---|
| `sites` | `["US"]` | Site codes for `filter_listings_by_site` |
| `ingestion_mode` | — | Must be `"manual_push"` to exclude from fetch-tick |
| `expected_push_interval_hours` | `4` | Staleness alert threshold (×2 intervals → alert) |

Tesla is **not** polled by the scheduled fetch loop. Freshness is measured by push time
(`last_successful_fetch_at` updated on each successful push).

---

## Testing

```bash
pytest job_ingestion/tests/test_tesla_careers_connector.py -v
pytest job_ingestion/tests/test_manual_ingest_api.py -v
```

Fixtures: `job_ingestion/tests/fixtures/tesla_careers/`

---

## Operational Notes

- **Do not** re-enable automated Playwright/curl fetch — Akamai blocks it (see troubleshooting log)
- **First push** is slow; incremental pushes are fast (known-ID skip)
- Staleness alerts append to `alerts.json` if no push within ~8h (default)
- Pipeline trigger for Tesla company ID will fail with a clear push-only error
