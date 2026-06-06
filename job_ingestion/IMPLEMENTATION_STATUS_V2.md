# Job Ingestion v2 Status (External Snapshot)

This document is the external-facing status of `job_ingestion` as of the dashboard integration phase: what exists, what changed, what has been validated, and what remains.

Context source: prior development transcript [Pipeline And Company Sync Work](dd5ce549-c615-4ed8-95a0-57483a017f19) plus latest integration and runtime validation.

## 1) Delivered scope

### Core outcomes

- Multi-source ATS ingestion with normalized persistence.
- Pipeline run tracking at aggregate and per-company levels.
- Raw payload persistence (`raw_jobs`) plus normalized jobs (`normalized_jobs`).
- Event stream and summary APIs for observability.
- Decoupled enrichment queue + batch processing with token/latency accounting.
- Reprocessing APIs for targeted reruns.

### Connector coverage

- **Greenhouse**: implemented and validated.
- **Ashby**: implemented and validated.
- **Lever (public boards)**: implemented and validated via public postings endpoint.

### Company source-of-truth behavior

- `data/companies.json` is source of truth.
- `POST /companies/seed` performs strict sync:
  - upsert companies present in file
  - delete companies absent from file
  - return inserted/updated/deleted counters

### Pipeline status semantics

- Pipeline terminal statuses:
  - `completed`
  - `partial_success`
  - `failed`
- Per-company failures are isolated so healthy sources can still complete.

## 2) Dashboard integration phase (new since prior snapshot)

Dashboard contract from `job-ingestion-dashboard` is now supported by backend and live data wiring.

### Backend API additions for dashboard actions

- `POST /companies/{company_id}/flag`
  - marks company `requires_review=true`
  - stores `flagged_for_review_at`
  - emits review event
- `PATCH /jobs/{job_id}`
  - reviewer edit endpoint for normalized enrichment fields + required comment
  - sets `processing_state=manually_corrected`
  - stores `last_manual_review_at`, `last_review_comment`
  - emits review event
- `POST /jobs/{job_id}/flag`
  - marks job `processing_state=requires_review` with required comment
  - stores review timestamp/comment
  - emits review event

### Backend API additions for cost tab

- `GET /enrichments/usage`
- `GET /enrichments/usage/trend`

These are compatibility endpoints for dashboard cost views, computed from enrichment history and batch records.

### Query/pagination/filter enhancements

- `GET /companies`:
  - added `include_job_counts`, `limit`, `offset`
- `GET /events`:
  - added `platform`, `offset`
- `GET /jobs`:
  - added `company`, `title`, multi-state `processing_state`, `sort_by`, `sort_dir`, `offset`
- `GET /pipeline/runs`:
  - added `offset` support

### Cross-origin/browser integration fixes

- Added FastAPI CORS middleware to allow dashboard origin(s) during local development.
- Corrected route mounting so `/enrichments/*` resolves at app root (not nested).
- Frontend API client now sets `Content-Type: application/json` only when request has a body, reducing unnecessary preflights.

## 3) Data model/migration changes for review workflows

### `companies` additions

- `requires_review` (bool)
- `flagged_for_review_at` (timestamp, nullable)
- `last_failure_at` (timestamp, nullable)

### `normalized_jobs` additions

- `last_manual_review_at` (timestamp, nullable)
- `last_review_comment` (text, nullable)

### Migration

- Added migration `20260528_0006_dashboard_review_fields.py` for the above persisted fields.

## 4) LLM enrichment hardening update

### Problem observed

- Some jobs were marked `partial_success` with `failure_reason=llm_schema_mismatch`.
- Root cause in production traces: Gemini occasionally returned JSON wrapped in markdown fences (for example ```json ... ```), causing strict JSON parsing failure.

### Fix implemented

- Gemini response parsing now:
  1. attempts strict parse on raw response
  2. retries with sanitized text after stripping fenced markdown JSON blocks
- Strict schema validation remains in place after sanitization.

### Validation result

- Added regression test for fenced JSON parsing in `tests/test_llm_gemini.py`.
- Previously failed `partial_success` jobs were successfully re-enriched via `POST /jobs/{id}/enrich-now` and transitioned to `processing_state=success`.

## 5) Current configured company set

- Active curated set: **12 companies**
  - Greenhouse + Ashby baseline
  - Lever additions: `basis`, `achievers`, `palantir`, `slate`

## 6) Technical footprint confirmed in code

### Data and schema foundations

- `raw_html` hardening migration in place (`20260525_0002_raw_html_hardening.py`).
- `normalized_jobs` includes pipeline/enrichment health fields:
  - `processing_state`
  - `failure_reason`
  - `last_failure_at`
  - plus review metadata fields from dashboard phase

### Decoupled enrichment architecture

- `job_enrichments` for enrichment history.
- Queue/batch orchestration:
  - `enrichment_queue`
  - `enrichment_batches`
  - `enrichment_batch_items`
- Ingestion persistence is decoupled from enrichment quality.

### Observability/event model

- Event APIs:
  - `GET /events`
  - `GET /events/summary`
- Review actions now also emit review-category events.

### Throughput and operations

- Concurrent per-company fetching with bounded concurrency.
- Scheduled pipeline runs via APScheduler.
- Manual trigger and reprocessing APIs available.

## 7) Validation status

### Automated tests (targeted)

- Ashby connector:
  - success path
  - GraphQL error handling
- Lever connector:
  - success path
  - malformed payload handling
  - upstream HTTP error wrapping
- Strict company sync:
  - drift deletion behavior
- Gemini provider tests:
  - normal JSON parse
  - client error wrapping
  - fenced JSON parse regression

### Manual API and integration validation

- Strict company sync behavior verified (remove/restore flow).
- Full pipeline runs verified with successful 12-company runs.
- Dashboard endpoints validated against live UI/API usage:
  - preflight/CORS checks
  - list/filter/sort/pagination reads
  - company pause/flag actions
  - job review/flag actions
  - cost usage/trend endpoints
- Re-enrichment validation confirms fenced-JSON parsing fix works in runtime.

## 8) Current operational state

- Backend APIs required by dashboard are implemented and reachable.
- Dashboard frontend can run against live backend data (no mock dependency required for core views).
- Pipeline, events, sources, jobs, and cost surfaces are now integrated end-to-end in local validation.

## 9) Known risks / remaining validation

- LLM provider quota/availability pressure (429/503) can still degrade enrichment completeness, though ingestion remains durable.
- External ATS payload/schema drift remains a standing risk and should be monitored through events/failure trends.
- Large-scale reliability/performance (100+ company load profile) is not yet fully benchmarked in this phase.

## 10) Architectural note: enrichment queue and batching

The queue/batching design (`enrichment_queue`, `enrichment_batches`, `enrichment_batch_items`) remains intentionally richer than simple decoupling.

### Why this remains the right approach

- Handles provider throttling and transient failures with controlled retries/cooldowns.
- Preserves visibility with per-item and per-batch observability.
- Enables cost/performance tracking via token and latency accounting at multiple levels.

### Product impact

- Ingestion throughput remains stable even when enrichment quality temporarily degrades.
- Failure isolation and auditability are stronger, supporting safe scale-up and future tuning.
