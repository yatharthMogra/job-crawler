# Job Ingestion System — V2.1 Implementation Blueprint
## (Non-UI Infrastructure Layer)

---

## 1. What V2.1 Builds

V2.1 transforms the V1 prototype into a multi-platform, operationally observable ingestion platform. No UI is included — the focus is getting the data layer, pipeline architecture, and event infrastructure correct before a UI reads from it.

**V2.1 delivers:**
- Multi-platform connectors (Lever + Ashby alongside Greenhouse)
- 100+ company coverage with concurrent fetching
- Decoupled ingestion and enrichment (enrichment failure never blocks job visibility)
- Structured processing states replacing boolean flags
- Failure reason taxonomy with constants-driven extensibility
- Structured event system (queryable operational log in DB)
- Separate enrichment table with token usage tracking
- Engineering-level reprocessing capability
- raw_html hardening prerequisite

---

## 2. Prerequisite Task (Do First)

### raw_html Hardening

Before building reprocessing, harden the raw storage layer.

**Step 1 — Backfill:**
```sql
UPDATE raw_jobs
SET raw_html = raw_api_response->>'content'
WHERE raw_html IS NULL
  AND raw_api_response->>'content' IS NOT NULL;
```

**Step 2 — Ingestion guard:**
In the pipeline, before inserting a raw_jobs row, always populate `raw_html` from `job.get("content")`. Log a warning if content is absent (some jobs legitimately have no description).

**Step 3 — Add NOT NULL with a fallback default:**
Once backfill is confirmed clean, add a DB-level NOT NULL constraint with empty string default so the column is always populated.

**Reprocessing read path (for safety):**
```python
html = raw_job.raw_html or raw_job.raw_api_response.get("content", "")
```
Keep this fallback even after the migration. Costs nothing, handles edge cases.

---

## 3. Platform APIs

All three platforms expose public job board APIs — no authentication required.

### Greenhouse (existing)
```
GET https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true
```
Returns: `jobs[]` with `id`, `title`, `location.name`, `departments[]`, `absolute_url`, `updated_at`, `content` (HTML)

### Lever (new)
```
GET https://api.lever.co/v1/postings/{company}?mode=published
```
Returns array of postings with:
- `id` — external job ID
- `text` — job title
- `categories.team`, `categories.department`, `categories.location`, `categories.commitment` (employment type)
- `descriptionPlain` — plain text description
- `description` — HTML description
- `hostedUrl` — posting URL
- `createdAt` — epoch ms timestamp

### Ashby (new)
```
GET https://api.ashbyhq.com/posting-public/v1/job-board/{organization_slug}
```
Returns `jobPostings[]` with:
- `id`
- `title`
- `departmentName`
- `locationName`
- `employmentType`
- `descriptionHtml`
- `externalLink` — posting URL
- `publishedAt`

---

## 4. Schema Changes

### 4.1 `companies` table — add `platform_config`

Add a nullable JSONB column for platform-specific metadata. For V2.1 all three platforms are public (no auth needed), but this column future-proofs auth config storage.

```
platform_config  JSONB  nullable
```

Example value for a future authenticated platform:
```json
{"requires_auth": false}
```

---

### 4.2 `normalized_jobs` — replace boolean flags with `processing_state`

**Remove:** no new boolean columns added. Existing `is_active` is retained (it's structural, not a processing state).

**Add:**
```
processing_state     VARCHAR     not null, default 'pending'
failure_reason       VARCHAR     nullable
last_failure_at      TIMESTAMP   nullable
```

**Processing states (from `app/ingestion/constants.py`):**

| State | Meaning |
|---|---|
| `pending` | Fetched, awaiting extraction |
| `success` | Fully extracted and enriched |
| `partial_success` | Extracted but enrichment failed |
| `extraction_failed` | Deterministic extraction failed |
| `enrichment_failed` | LLM enrichment failed |
| `malformed_source` | Source payload was unparseable |
| `requires_review` | Flagged for manual inspection |
| `manually_corrected` | Reviewer has edited this record |

---

### 4.3 New table: `job_enrichments`

Decouples enrichment from the normalized job record. One row per enrichment attempt.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| normalized_job_id | UUID FK → normalized_jobs | |
| raw_job_id | UUID FK → raw_jobs | Which raw snapshot was used |
| llm_provider | VARCHAR | e.g. "gemini" |
| llm_model | VARCHAR | e.g. "gemini-1.5-flash" |
| extraction_version | VARCHAR | e.g. "v1" |
| seniority | VARCHAR | |
| is_internship | BOOLEAN | |
| is_new_grad | BOOLEAN | |
| sponsorship_status | VARCHAR | |
| sponsorship_confidence | VARCHAR | |
| remote_type | VARCHAR | |
| tech_stack | VARCHAR[] | |
| skills | VARCHAR[] | |
| input_tokens | INTEGER | |
| output_tokens | INTEGER | |
| latency_ms | INTEGER | |
| status | VARCHAR | "success / failed" |
| failure_reason | VARCHAR | nullable |
| created_at | TIMESTAMP | |

The most recent successful enrichment row drives what's shown in search/display. `normalized_jobs` no longer carries enrichment fields directly.

---

### 4.4 New table: `ingestion_events`

Structured operational event log. Queryable, filterable, lightweight.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| event_type | VARCHAR | e.g. "pipeline_completed" |
| event_category | VARCHAR | "pipeline / source / enrichment / review / system" |
| severity | VARCHAR | "info / warning / error / critical" |
| platform | VARCHAR | nullable |
| company_id | UUID FK → companies | nullable |
| pipeline_run_id | UUID FK → pipeline_runs | nullable |
| normalized_job_id | UUID FK → normalized_jobs | nullable |
| metadata | JSONB | event-specific payload |
| created_at | TIMESTAMP | |

Index on `(event_category, created_at)` and `(company_id, created_at)` for dashboard queries.

---

## 5. Constants File

`app/ingestion/constants.py` — single source of truth for all string taxonomies.

```python
# Processing states
class ProcessingState:
    PENDING = "pending"
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    EXTRACTION_FAILED = "extraction_failed"
    ENRICHMENT_FAILED = "enrichment_failed"
    MALFORMED_SOURCE = "malformed_source"
    REQUIRES_REVIEW = "requires_review"
    MANUALLY_CORRECTED = "manually_corrected"

# Failure reasons
class FailureReason:
    JSON_PARSE_FAILURE = "json_parse_failure"
    MALFORMED_HTML = "malformed_html"
    MISSING_REQUIRED_FIELDS = "missing_required_fields"
    LLM_TIMEOUT = "llm_timeout"
    LLM_SCHEMA_MISMATCH = "llm_schema_mismatch"
    LLM_EMPTY_RESPONSE = "llm_empty_response"
    HTTP_ERROR = "http_error"
    NETWORK_TIMEOUT = "network_timeout"
    MALFORMED_SOURCE_RESPONSE = "malformed_source_response"
    TOKEN_LIMIT_EXCEEDED = "token_limit_exceeded"

# Event types
class EventType:
    # Pipeline
    PIPELINE_STARTED = "pipeline_started"
    PIPELINE_COMPLETED = "pipeline_completed"
    PIPELINE_PARTIAL_SUCCESS = "pipeline_partial_success"
    PIPELINE_FAILED = "pipeline_failed"
    # Source
    SOURCE_FETCH_FAILED = "source_fetch_failed"
    SOURCE_FAILURE_THRESHOLD_REACHED = "source_failure_threshold_reached"
    SOURCE_RECOVERED = "source_recovered"
    MALFORMED_SOURCE_RESPONSE = "malformed_source_response"
    # Enrichment
    LLM_EXTRACTION_FAILED = "llm_extraction_failed"
    MALFORMED_LLM_RESPONSE = "malformed_llm_response"
    ENRICHMENT_SKIPPED = "enrichment_skipped"
    TOKEN_SPIKE_DETECTED = "token_spike_detected"
    # Review
    REVIEWER_EDITED_JOB = "reviewer_edited_job"
    REVIEWER_DISABLED_JOB = "reviewer_disabled_job"
    JOB_MARKED_REQUIRES_REVIEW = "job_marked_requires_review"
    # System
    SCHEDULER_STARTED = "scheduler_started"
    SCHEDULER_STOPPED = "scheduler_stopped"

# Event categories
class EventCategory:
    PIPELINE = "pipeline"
    SOURCE = "source"
    ENRICHMENT = "enrichment"
    REVIEW = "review"
    SYSTEM = "system"

# Severity
class EventSeverity:
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
```

All pipeline, extractor, and event writer code imports from this file. No inline string literals for these values anywhere else.

---

## 6. Updated Project Structure

Changes from V1 shown with `[NEW]` and `[CHANGED]`.

```
app/
├── main.py
├── config.py
├── database.py
├── scheduler.py
│
├── models/
│   ├── company.py
│   ├── raw_job.py
│   ├── normalized_job.py         [CHANGED] add processing_state, failure_reason
│   ├── job_enrichment.py         [NEW]
│   ├── pipeline_run.py
│   └── ingestion_event.py        [NEW]
│
├── schemas/
│   ├── company.py
│   ├── pipeline.py
│   ├── job.py
│   └── enrichment.py             [NEW]
│
├── api/
│   ├── companies.py
│   ├── pipeline.py
│   └── reprocessing.py           [NEW]
│
├── ingestion/
│   ├── constants.py              [NEW]
│   ├── pipeline.py               [CHANGED] decoupled enrichment, event writes
│   ├── fetcher.py                [CHANGED] now dispatcher → platform connector
│   ├── change_detector.py
│   ├── alerts.py
│   ├── events.py                 [NEW] event writer helpers
│   ├── reprocessor.py            [NEW]
│   │
│   ├── connectors/               [NEW] replaces fetcher.py direct Greenhouse logic
│   │   ├── base.py               abstract Connector interface
│   │   ├── greenhouse.py
│   │   ├── lever.py
│   │   └── ashby.py
│   │
│   └── extractor/
│       ├── deterministic.py      [CHANGED] platform-aware field mapping
│       ├── llm.py                [CHANGED] returns token usage, decoupled
│       └── text_cleaner.py
│
├── llm/
│   ├── base.py
│   ├── gemini.py
│   └── factory.py
│
└── utils/
    ├── hashing.py
    ├── logging.py
    └── seed.py
```

---

## 7. Connector Architecture

### Abstract Interface (`connectors/base.py`)

Each connector implements one method:

```python
class BaseConnector:
    async def fetch_jobs(self, company: Company) -> list[dict]:
        """
        Returns a list of raw job dicts in platform-native format.
        Raises ConnectorFetchError on failure.
        """
        raise NotImplementedError
```

The pipeline calls `connector.fetch_jobs(company)` — it never knows which platform it's talking to.

### Connector Registry (`ingestion/fetcher.py`)

The fetcher module becomes a dispatcher:

```python
CONNECTORS = {
    "greenhouse": GreenhouseConnector,
    "lever": LeverConnector,
    "ashby": AshbyConnector,
}

def get_connector(platform: str) -> BaseConnector:
    cls = CONNECTORS.get(platform)
    if not cls:
        raise UnsupportedPlatformError(platform)
    return cls()
```

### Platform-Specific Normalization

Each connector returns raw platform-native dicts. The deterministic extractor handles platform-specific field mapping:

```python
# deterministic.py
FIELD_MAPS = {
    "greenhouse": {
        "external_id": lambda j: str(j["id"]),
        "title": lambda j: j["title"],
        "location": lambda j: j.get("location", {}).get("name"),
        "department": lambda j: j["departments"][0]["name"] if j.get("departments") else None,
        "posting_url": lambda j: j.get("absolute_url"),
        "posted_at": lambda j: j.get("updated_at"),
        "html_content": lambda j: j.get("content"),
    },
    "lever": {
        "external_id": lambda j: j["id"],
        "title": lambda j: j["text"],
        "location": lambda j: j.get("categories", {}).get("location"),
        "department": lambda j: j.get("categories", {}).get("department"),
        "posting_url": lambda j: j.get("hostedUrl"),
        "posted_at": lambda j: ...,  # convert epoch ms to datetime
        "html_content": lambda j: j.get("description"),
    },
    "ashby": {
        "external_id": lambda j: j["id"],
        "title": lambda j: j["title"],
        "location": lambda j: j.get("locationName"),
        "department": lambda j: j.get("departmentName"),
        "posting_url": lambda j: j.get("externalLink"),
        "posted_at": lambda j: j.get("publishedAt"),
        "html_content": lambda j: j.get("descriptionHtml"),
    },
}
```

Downstream of extraction, everything is platform-agnostic.

---

## 8. Decoupled Ingestion and Enrichment

### V1 behavior (tightly coupled):
```
fetch → raw store → extract → enrich → store normalized
         ↑ if enrich fails, job record is incomplete or not written
```

### V2.1 behavior (decoupled):
```
fetch → raw store → extract deterministic → store normalized (processing_state: pending)
                                  ↓
                           enrich (best-effort)
                                  ↓
                    success → update normalized (processing_state: success)
                    failure → update normalized (processing_state: partial_success)
                              write job_enrichments row with status: failed
                              write ingestion_event: llm_extraction_failed
                              job remains visible with core fields
```

### Pipeline logic change:

```python
# Pseudocode — pipeline.py per-job flow

# Step 1: always store raw
raw_job = await store_raw_job(job, company)

# Step 2: deterministic extraction (if this fails → extraction_failed, stop)
try:
    det_fields = deterministic_extractor.extract(job, platform=company.platform)
except ExtractionError as e:
    await upsert_normalized_job(det_fields_partial, state=ProcessingState.EXTRACTION_FAILED,
                                failure_reason=e.reason)
    await write_event(EventType.SOURCE_FETCH_FAILED, ...)
    continue

# Step 3: upsert normalized with core fields (state: pending)
normalized_job = await upsert_normalized_job(det_fields, state=ProcessingState.PENDING)

# Step 4: enrichment (best-effort — never raises to caller)
try:
    enrichment = await llm_extractor.enrich(clean_text, raw_job)
    await store_enrichment(normalized_job.id, enrichment, status="success")
    await update_normalized_state(normalized_job.id, ProcessingState.SUCCESS)
except EnrichmentError as e:
    await store_enrichment(normalized_job.id, None, status="failed",
                           failure_reason=e.reason)
    await update_normalized_state(normalized_job.id, ProcessingState.PARTIAL_SUCCESS,
                                  failure_reason=e.reason)
    await write_event(EventType.LLM_EXTRACTION_FAILED, metadata={"reason": e.reason})
```

---

## 9. Concurrent Fetching

At 100+ companies, sequential fetching is too slow. V2.1 introduces semaphore-limited concurrent fetching.

```python
# pipeline.py
FETCH_CONCURRENCY = 10  # configurable via settings

semaphore = asyncio.Semaphore(FETCH_CONCURRENCY)

async def fetch_company_with_limit(company):
    async with semaphore:
        return await run_company_pipeline(company)

results = await asyncio.gather(
    *[fetch_company_with_limit(c) for c in companies],
    return_exceptions=True
)
```

`FETCH_CONCURRENCY` is added to `config.py` with a default of 10. This keeps Greenhouse/Lever/Ashby from seeing burst traffic while parallelizing the slow network I/O.

---

## 10. Event System

### Event Writer (`ingestion/events.py`)

A thin helper that all pipeline components call:

```python
async def write_event(
    db: AsyncSession,
    event_type: str,
    category: str,
    severity: str,
    platform: str | None = None,
    company_id: UUID | None = None,
    pipeline_run_id: UUID | None = None,
    normalized_job_id: UUID | None = None,
    metadata: dict | None = None,
) -> None:
    event = IngestionEvent(
        event_type=event_type,
        event_category=category,
        severity=severity,
        platform=platform,
        company_id=company_id,
        pipeline_run_id=pipeline_run_id,
        normalized_job_id=normalized_job_id,
        metadata=metadata or {},
    )
    db.add(event)
    await db.flush()
```

Events are written within the same DB session as the pipeline transaction — no separate event service, no async queue.

### Where events are written:

| Trigger | Event type | Severity |
|---|---|---|
| Pipeline starts | `pipeline_started` | info |
| Pipeline completes (all success) | `pipeline_completed` | info |
| Pipeline completes (mixed) | `pipeline_partial_success` | warning |
| Pipeline all failed | `pipeline_failed` | error |
| Company fetch fails | `source_fetch_failed` | error |
| Company hits K failure threshold | `source_failure_threshold_reached` | critical |
| Company recovers after failures | `source_recovered` | info |
| Malformed platform response | `malformed_source_response` | warning |
| LLM enrichment fails | `llm_extraction_failed` | warning |
| Malformed LLM response | `malformed_llm_response` | warning |
| Scheduler starts | `scheduler_started` | info |
| Scheduler stops | `scheduler_stopped` | info |

---

## 11. Reprocessing

Engineering-level reprocessing of extraction and enrichment without refetching source jobs.

### API endpoint:
```
POST /reprocessing/jobs
```

Request body:
```json
{
  "filters": {
    "processing_state": ["extraction_failed", "partial_success"],
    "extraction_version": "v1",
    "company_id": "optional-uuid",
    "platform": "optional-platform"
  },
  "target_version": "v2",
  "dry_run": true
}
```

With `dry_run: true`, the endpoint returns the count of jobs that would be reprocessed without actually running. Set to `false` to execute.

### Reprocessor (`ingestion/reprocessor.py`)

```python
async def reprocess_jobs(filters: ReprocessingFilters, target_version: str) -> ReprocessingResult:
    # 1. Query normalized_jobs matching filters
    # 2. For each: load associated raw_job
    # 3. Read html = raw_job.raw_html or raw_api_response.get("content", "")
    # 4. Re-run deterministic extraction
    # 5. Re-run LLM enrichment with target_version
    # 6. Write new job_enrichments row
    # 7. Update normalized_job.extraction_version, processing_state
    # 8. Write reprocessing event to ingestion_events
```

Reprocessing always writes a new `job_enrichments` row — it does not overwrite the previous enrichment. Historical enrichment attempts are preserved.

---

## 12. LLM Changes

### Token usage capture

`llm/base.py` interface change — `complete()` now returns both the parsed response and usage:

```python
@dataclass
class LLMResult:
    output: BaseModel
    input_tokens: int
    output_tokens: int
    latency_ms: int
```

Gemini's response object exposes `usage_metadata.prompt_token_count` and `usage_metadata.candidates_token_count`.

### Token spike detection

After each enrichment, check if `input_tokens > TOKEN_SPIKE_THRESHOLD` (configurable, default 8000). If so, write a `token_spike_detected` event with the job ID and token count. This surfaces jobs with unusually long descriptions before they become cost problems.

---

## 13. New API Endpoints

### Reprocessing
| Method | Path | Description |
|---|---|---|
| POST | `/reprocessing/jobs` | Trigger reprocessing with filters |
| GET | `/reprocessing/runs` | List reprocessing runs |

### Events (read-only, for future dashboard use)
| Method | Path | Description |
|---|---|---|
| GET | `/events` | Query events with filters (category, severity, company_id, date range) |
| GET | `/events/summary` | Aggregated event counts by type/category |

### Jobs (new read endpoints)
| Method | Path | Description |
|---|---|---|
| GET | `/jobs` | List normalized jobs with filtering (state, platform, company, active) |
| GET | `/jobs/{job_id}` | Full job detail including enrichment history |
| GET | `/jobs/{job_id}/raw` | Raw ingestion payload for a job |

---

## 14. Configuration Additions

New `.env` keys for V2.1:

```
# Concurrency
FETCH_CONCURRENCY=10

# Token spike detection
TOKEN_SPIKE_THRESHOLD=8000

# Reprocessing
DEFAULT_EXTRACTION_VERSION=v2
```

---

## 15. Build Sequence

Do these in order. Each step is independently testable before moving to the next.

**Step 1 — Prerequisite**
- raw_html backfill script
- Ingestion guard in pipeline
- NOT NULL migration

**Step 2 — Constants + Schema**
- `app/ingestion/constants.py`
- `processing_state` + `failure_reason` on `normalized_jobs` migration
- `job_enrichments` table migration
- `ingestion_events` table migration

**Step 3 — Connector Architecture**
- `connectors/base.py` abstract interface
- Move Greenhouse logic to `connectors/greenhouse.py`
- `connectors/lever.py`
- `connectors/ashby.py`
- Fetcher dispatcher

**Step 4 — Deterministic Extractor Platform Mapping**
- Platform-aware field maps
- Validate against Lever and Ashby sample responses

**Step 5 — Decoupled Enrichment Pipeline**
- Separate enrichment from core ingestion
- `job_enrichments` write path
- Processing state transitions
- Enrichment failure handling (no longer propagates)

**Step 6 — Event System**
- `ingestion/events.py` writer
- Wire events into pipeline at all trigger points
- Verify events table populates correctly

**Step 7 — Token Usage + LLM Changes**
- `LLMResult` dataclass
- Token capture from Gemini response
- Token spike detection

**Step 8 — Concurrent Fetching**
- Semaphore-limited `asyncio.gather`
- `FETCH_CONCURRENCY` config

**Step 9 — Reprocessing**
- `reprocessor.py`
- `/reprocessing` endpoints

**Step 10 — Scale + Validation**
- Expand `companies.json` to 100+
- Full pipeline run at scale
- Validate event stream, token usage, processing states, concurrency behavior

---

## 16. Key Design Rules for V2.1

- **Constants file is the single source of truth.** Never hardcode state strings, event types, or failure reasons inline.
- **Enrichment failure never propagates to ingestion.** A job with `partial_success` is visible. A job blocked by enrichment is a bug.
- **`job_enrichments` is append-only.** Reprocessing writes a new row, never updates an old one.
- **Events are written in the same DB session as the pipeline.** No separate event queue in V2.1.
- **Connectors return platform-native dicts.** They do not normalize. Normalization is the extractor's job.
- **Token usage is captured on every enrichment attempt**, including failed ones (capture what's available before the failure).
- **Concurrent fetching uses a semaphore**, not unbounded `gather`. Default 10, configurable.
- **`/events` endpoints are read-only.** Events are written only by the pipeline, never via API.