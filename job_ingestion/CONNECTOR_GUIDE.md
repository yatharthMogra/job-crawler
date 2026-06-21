# Job Ingestion — Connector Guide

This document explains how our job ingestion pipeline works across Greenhouse, Ashby, and Lever, and what a new platform connector (e.g. Workday) must provide. It is written for external engineers who need to propose an implementation approach without reading the full codebase.

For broader system context (schema, enrichment worker, events), see [`job_ingestion_v2.md`](../job_ingestion_v2.md).

---

## 1. High-Level Pipeline

Each company in our database has a `platform` (e.g. `greenhouse`) and a `board_token` (the company's identifier on that platform). On a scheduled or manual run, the pipeline:

1. **Fetch** — calls the platform connector to get all current job postings for that company.
2. **Classify** — compares each fetched job against the last known version (by content hash) and labels it as new, updated, unchanged, or removed.
3. **Persist raw** — for new/updated jobs, stores the full platform-native JSON in `raw_jobs`, plus extracted HTML description in `raw_html`.
4. **Extract deterministic fields** — maps platform-specific JSON into a common schema (title, location, etc.). No LLM involved.
5. **Upsert normalized job** — writes/updates a `normalized_jobs` row with deterministic fields and `processing_state = pending`.
6. **Queue for enrichment** — adds the job to an async enrichment queue.
7. **LLM enrichment** (separate worker) — reads `raw_html`, extracts semantic fields (seniority, skills, sponsorship, etc.), and updates the normalized job.

```
Company (platform + board_token)
        │
        ▼
  Connector.fetch_jobs()  ──► list[platform-native dict]
        │
        ▼
  Change detector (hash by job["id"])
        │
        ▼ (new / updated only)
  RawJob (raw_api_response + raw_html + content_hash)
        │
        ▼
  Deterministic extractor  ──► common field dict
        │
        ▼
  NormalizedJob (processing_state = pending)
        │
        ▼
  Enrichment queue  ──► LLM worker (async, batched)
```

**Key design rule:** Connectors return platform-native dicts. They do **not** normalize. Normalization happens in `deterministic.py`.

**Key design rule:** Ingestion and enrichment are decoupled. A fetch/extraction failure blocks the job; an enrichment failure does not roll back ingestion — the job remains visible with `processing_state = partial_success` or `enrichment_failed`.

---

## 2. Connector Interface

Every connector implements one method:

```python
class BaseConnector:
    async def fetch_jobs(self, company: Company) -> list[dict]:
        """
        Returns a list of raw job dicts in platform-native format.
        Raises ConnectorFetchError on HTTP/network failure.
        Raises ParseError on malformed/unexpected response shape.
        """
```

Registration is in `app/ingestion/fetcher.py`:

```python
CONNECTORS = {
    "greenhouse": GreenhouseConnector,
    "lever": LeverConnector,
    "ashby": AshbyConnector,
    "workable": WorkableConnector,
}
```

The `Company` model fields relevant to connectors:

| Field | Purpose |
|---|---|
| `platform` | Which connector to use (`greenhouse`, `lever`, `ashby`) |
| `board_token` | Company slug/token on that platform (unique per company) |
| `platform_config` | Optional JSONB for future auth/config (currently unused for public boards) |

---

## 3. Change Detection Contract

The change detector (`classify_jobs`) expects every job dict to have:

| Requirement | Details |
|---|---|
| **`id` field** | Stable external job ID. Used as `external_job_id`. Jobs without `id` (or with `id = None`) are **silently skipped**. |
| **Full payload for hashing** | `compute_content_hash(job)` SHA-256s the entire dict (JSON, sorted keys). Any field change triggers re-ingestion. |
| **Complete descriptions in fetch** | Descriptions must be present in the dict returned by `fetch_jobs`, not fetched later in the extractor. Ashby is the example of a two-step fetch inside the connector. |

Removal detection: jobs that were previously active but missing from the latest fetch get `consecutive_misses` incremented; after N consecutive misses (default 3), `is_active` is set to `false`.

---

## 4. Platform Connectors

### 4.1 Greenhouse

**List API + optional branded careers supplement — see [`greenhouse_connector_guide.md`](../greenhouse_connector_guide.md) for full details.**

| | |
|---|---|
| **Auth** | None (public Job Board API) |
| **List endpoint** | `GET https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true` |
| **Detail endpoint** | `GET https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs/{id}?content=true` |
| **`board_token`** | Greenhouse board slug (e.g. `stripe`, `anthropic`) |
| **Implementation** | `app/ingestion/connectors/greenhouse.py` |

**Default behavior:** single list call returns all publicly listed board jobs with full `content`.

**Branded careers supplement:** when `platform_config.careers_url` is set, the connector also scrapes the company careers page for `gh_jid` / Greenhouse job links, fetches any **additional** job IDs via the per-job API, and merges them with the list (deduped by `id`; list payload wins on conflict). Use `board_token_override` when the API slug differs from the careers hostname (e.g. C3.ai → `c3iot`).

**Response shape:** `{ "jobs": [ ... ] }` from list; single job object from detail — connector returns a unified array.

**Per-job fields we rely on:**

| Platform field | Used for |
|---|---|
| `id` | External job ID, change detection |
| `title` | Job title |
| `location.name` | Location |
| `departments[0].name` | Department (first department if multiple) |
| `absolute_url` | Posting URL |
| `updated_at` | Posted/updated timestamp (ISO 8601) |
| `content` | HTML job description → `raw_html` |
| `metadata[]` | Employment type (scans for name containing "employment" or "type") |

**Example minimal job dict:**

```json
{
  "id": 42,
  "title": "Backend Engineer",
  "location": { "name": "New York" },
  "departments": [{ "name": "Engineering" }],
  "absolute_url": "https://boards.greenhouse.io/company/jobs/42",
  "updated_at": "2026-05-20T10:00:00Z",
  "content": "<p>Build APIs with Python...</p>",
  "metadata": [{ "name": "Employment Type", "value": "Full-time" }]
}
```

---

### 4.2 Lever

**Simple connector — single REST call, descriptions included.**

| | |
|---|---|
| **Auth** | None (public postings API) |
| **Endpoint** | `GET https://api.lever.co/v0/postings/{board_token}?mode=json` |
| **`board_token`** | Lever company slug (e.g. `netflix`, `basis`) |
| **Implementation** | `app/ingestion/connectors/lever.py` |

**Response shape:** JSON array of posting objects — connector returns the array directly.

**Per-job fields we rely on:**

| Platform field | Used for |
|---|---|
| `id` | External job ID |
| `text` | Job title |
| `categories.location` | Location |
| `categories.department` or `categories.team` | Department |
| `categories.commitment` | Employment type |
| `hostedUrl` | Posting URL |
| `createdAt` | Posted timestamp (epoch milliseconds) |
| `description` or `descriptionPlain` | HTML or plain description → `raw_html` |

**Example minimal job dict:**

```json
{
  "id": "a1b2c3d4-...",
  "text": "Software Engineer",
  "hostedUrl": "https://jobs.lever.co/company/a1b2c3d4",
  "createdAt": 1700000000000,
  "categories": {
    "location": "Remote",
    "department": "Engineering",
    "commitment": "Full-time"
  },
  "description": "<div>Join our team...</div>"
}
```

---

### 4.3 Ashby

**Two-step connector — list endpoint lacks descriptions; per-job detail fetch required.**

| | |
|---|---|
| **Auth** | None (public GraphQL API) |
| **List endpoint** | `POST https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams` |
| **Detail endpoint** | `POST https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobPosting` |
| **`board_token`** | Organization hosted jobs page name (e.g. `openai`, `notion`) |
| **Implementation** | `app/ingestion/connectors/ashby.py` |

**Fetch pattern:**

1. GraphQL list query → `jobPostings[]` with `id`, `title`, `locationName`, `employmentType`, `secondaryLocations`.
2. For each posting, GraphQL detail query → `descriptionHtml`, `departmentName`, `publishedDate`, `secondaryLocationNames`.
3. Merge list + detail into one dict per job.
4. Synthesize `externalLink` as `https://jobs.ashbyhq.com/{board_token}/{job_id}`.

**Rate limiting:** All list and detail requests share a global `HostTokenBucket` for `jobs.ashbyhq.com` (see `app/ingestion/rate_limiter.py`, tuned via `ASHBY_HOST_RATE_PER_SECOND` / `ASHBY_HOST_BURST`). Per-company detail concurrency stays at 1. On 429, the connector honors `Retry-After` when present, otherwise exponential backoff. Incremental re-fetch skips unchanged jobs using cached `raw_jobs` (listing fingerprint + `ASHBY_FULL_REFRESH_DAYS`). Partial detail failures fall back to cache or listing-only data rather than failing the whole company.

**Per-job fields we rely on (after merge):**

| Platform field | Used for |
|---|---|
| `id` | External job ID |
| `title` | Job title |
| `locationName` + `secondaryLocationNames` | Location (joined with ` \| `) |
| `departmentName` | Department (from detail query only) |
| `employmentType` | Employment type |
| `externalLink` | Posting URL (synthesized by connector) |
| `publishedDate` or `publishedAt` | Posted timestamp (ISO 8601) |
| `descriptionHtml` | HTML description → `raw_html` (from detail query only) |

**Why two steps:** The list API does not return `descriptionHtml` or `departmentName`. We learned this the hard way — jobs ingested without the detail fetch had empty descriptions and failed enrichment.

---

### 4.4 Workable

**Simple connector — single REST call with descriptions via query param.**

| | |
|---|---|
| **Auth** | None (public widget API) |
| **Endpoint** | `GET https://apply.workable.com/api/v1/widget/accounts/{board_token}?details=true` |
| **`board_token`** | Account slug from the hosted careers URL (e.g. `quadric-dot-i-o-inc` from `https://apply.workable.com/quadric-dot-i-o-inc/`) |
| **Implementation** | `app/ingestion/connectors/workable.py` |

**Fetch pattern:**

1. Single GET with `details=true` → all active jobs with plain-text descriptions.
2. Dedupe by `shortcode` (multi-region roles may appear twice in the list).
3. Map `shortcode` → `id` for change detection.

**Per-job fields we rely on:**

| Platform field | Used for |
|---|---|
| `shortcode` → `id` | External job ID (connector maps shortcode to `id`) |
| `title` | Job title |
| `locations[]` + `telecommuting` | Location (joined with ` \| `; prefix `Remote` when telecommuting) |
| `department` | Department |
| `employment_type` | Employment type |
| `url` or `shortlink` | Posting URL |
| `published_on` | Posted date (`YYYY-MM-DD`) |
| `description` | Plain-text description → `raw_html` (requires `?details=true`) |

**Dedupe requirement:** Some companies list the same `shortcode` multiple times for multi-region variants (e.g. China + Taiwan). The connector merges `locations[]` and returns one dict per shortcode.

**Example minimal job dict (after connector normalization):**

```json
{
  "id": "48DBFB8E87",
  "shortcode": "48DBFB8E87",
  "title": "AI Applications Engineer",
  "department": "Software Engineering",
  "employment_type": "Full-time",
  "url": "https://apply.workable.com/j/48DBFB8E87",
  "published_on": "2025-08-25",
  "telecommuting": false,
  "locations": [{"country": "United States", "city": "Burlingame", "region": "California"}],
  "description": "Build AI applications..."
}
```

---

## 5. Deterministic Extraction (Pre-LLM)

After fetch, `extract_deterministic_fields(job, platform)` in `app/ingestion/extractor/deterministic.py` maps each platform's native dict into a **common schema**. This is the boundary between platform-specific and platform-agnostic data.

### 5.1 Common output schema

Every platform extractor returns:

| Field | Type | Required | Notes |
|---|---|---|---|
| `external_job_id` | `str` | **Yes** | From `str(job["id"])`. Primary key with `company_id`. |
| `title` | `str` | **Yes** | Falls back to `"Untitled"` at DB write time if empty. |
| `location` | `str \| None` | No | |
| `department` | `str \| None` | No | |
| `posting_url` | `str \| None` | No | |
| `posted_at` | `datetime \| None` | No | Timezone-aware UTC. |
| `employment_type` | `str \| None` | No | |
| `raw_html` | `str` | **Yes** (can be `""`) | HTML description; stored in `raw_jobs.raw_html`. |

The pipeline additionally computes (not in the extractor):

| Field | Source |
|---|---|
| `description_text` | `clean_job_description(raw_html)` — HTML stripped to plain text |
| `description_preview` | First ~400 chars of `description_text` |

### 5.2 Platform field mapping reference

| Common field | Greenhouse | Lever | Ashby | Workable |
|---|---|---|---|---|
| `external_job_id` | `id` | `id` | `id` | `shortcode` (mapped to `id`) |
| `title` | `title` | `text` | `title` | `title` |
| `location` | `location.name` | `categories.location` | `locationName` (+ secondary) | `locations[]` (+ `telecommuting`) |
| `department` | `departments[0].name` | `categories.department` or `.team` | `departmentName` | `department` |
| `posting_url` | `absolute_url` | `hostedUrl` | `externalLink` | `url` or `shortlink` |
| `posted_at` | `updated_at` (ISO) | `createdAt` (epoch ms) | `publishedDate` (ISO) | `published_on` (date) |
| `employment_type` | `metadata[]` scan | `categories.commitment` | `employmentType` | `employment_type` |
| `raw_html` | `content` | `description` or `descriptionPlain` | `descriptionHtml` | `description` (plain text) |

### 5.3 What gets stored before enrichment

For each new/updated job, **before** it enters the enrichment queue:

**`raw_jobs` table:**
- `external_job_id`, `platform`, `company_id`
- `raw_api_response` — full platform-native JSON (JSONB)
- `raw_html` — HTML description extracted by deterministic extractor
- `content_hash` — SHA-256 of full raw dict
- `fetch_timestamp`

**`normalized_jobs` table:**
- All deterministic fields above (title, location, department, posting_url, posted_at, employment_type, description_text, description_preview)
- `company_name`, `is_active = true`, `consecutive_misses = 0`
- `processing_state = pending`
- Enrichment fields set to **defaults** (`seniority = unclear`, empty skills/tech_stack, etc.) — overwritten after LLM runs

---

## 6. LLM Enrichment (Post-Ingestion)

The enrichment worker runs asynchronously. It does **not** re-fetch from the job board.

### 6.1 What the enrichment worker reads

| Source | Fields used |
|---|---|
| `raw_jobs.raw_html` | Primary input — cleaned to plain text via BeautifulSoup |
| `normalized_jobs.title` | Passed to LLM as context |
| `normalized_jobs.employment_type` | Passed to LLM as context |
| `normalized_jobs.external_job_id` | Batch correlation ID |

The LLM payload per job (`build_batch_job_payload`):

```json
{
  "job_id": "<external_job_id>",
  "text": "<cleaned plain text from raw_html>",
  "title": "<title>",
  "employment_type": "<employment_type>",
  "seniority_hint": "<optional, inferred from title/employment_type>"
}
```

### 6.2 What the LLM produces

| Field | Description |
|---|---|
| `seniority` | INTERN, NEW_GRAD, ENTRY, JUNIOR, MID, SENIOR, STAFF, PRINCIPAL, MANAGEMENT, UNKNOWN |
| `is_internship`, `is_new_grad` | Booleans |
| `sponsorship_status`, `sponsorship_confidence` | Visa sponsorship signals |
| `remote_type` | remote, hybrid, onsite, unclear |
| `tech_stack` | Tools/languages/frameworks (required for engineering roles) |
| `skills` | Domain competencies (required for engineering roles) |
| `normalized_roles` | Role taxonomy (SWE, ML_ENGINEER, etc.) |
| `job_capabilities` | Capability taxonomy |
| `application_effort` | LOW, MEDIUM, HIGH |
| `salary_min`, `salary_max` | Annual USD if stated |

### 6.3 Hard requirements for successful enrichment

| Requirement | Why |
|---|---|
| **`id` must be present and stable** | Change detection and deduplication depend on it. |
| **`raw_html` should contain the full job description** | This is the LLM's sole input for semantic extraction. Empty `raw_html` → enrichment runs on empty text → poor/no skill extraction. |
| **Description should be HTML (or plain text)** | `clean_job_description` handles HTML stripping. Plain text works but HTML is preferred when available. |
| **Title strongly recommended** | Used as LLM context and for seniority hint inference. |
| **Employment type helpful but optional** | Improves seniority inference. |

There is no hard validation that blocks enrichment if `raw_html` is empty — the job will queue and enrich with empty text, likely resulting in `enrichment_failed` or `partial_success` if the description was substantive but missing from the fetch.

For engineering roles with descriptions ≥300 chars, we flag enrichment as incomplete if both `tech_stack` and `skills` come back empty (suggests the description was not actually ingested).

---

## 7. Implementing a New Connector (Workday)

### 7.1 What you need to deliver

1. **`WorkdayConnector.fetch_jobs(company)`** — returns `list[dict]` in Workday-native format.
2. **`_extract_workday(job)`** in `deterministic.py` — maps Workday fields to the common schema (section 5.1).
3. **Registration** in `fetcher.py` `CONNECTORS` dict and `FIELD_EXTRACTORS` in `deterministic.py`.
4. **Tests** — success path, malformed response, fetch failure (see `tests/test_ashby_connector.py`, `tests/test_lever_connector.py`).

### 7.2 Questions to answer for Workday

These are the decisions we need your input on:

| Question | Context |
|---|---|
| **What is the `board_token` equivalent?** | For Greenhouse it's the board slug; for Ashby it's the hosted page name. What identifies a Workday tenant/career site? |
| **Public API vs scraping?** | Our three existing connectors use official public APIs with no auth. Does Workday offer an equivalent, or is scraping/interception required? |
| **Single call or multi-step fetch?** | Greenhouse/Lever return descriptions in the list call. Ashby requires a per-job detail call. Which pattern does Workday follow? |
| **Stable job ID** | What field is immutable across re-posts? Change detection keys on this. |
| **Description format** | HTML, plain text, or structured blocks? We store HTML in `raw_html` when possible. |
| **Rate limits / pagination** | How many jobs per company? Paginated? Throttled? |
| **Auth requirements** | If auth is needed, what goes in `company.platform_config`? |
| **Location representation** | Single string, multiple locations, remote flags? Ashby joins secondary locations with `\|`. |
| **Timestamp field** | Which field best represents "posted date"? |

### 7.3 Minimum viable job dict

At minimum, each dict returned by `fetch_jobs` must have:

```python
{
    "id": "<stable-external-id>",       # REQUIRED — used for change detection
    # ... plus enough fields that _extract_workday() can populate:
    # title, location, department, posting_url, posted_at, raw_html
}
```

The full platform response should remain in the dict (or as the dict itself) so `raw_api_response` preserves everything for debugging and reprocessing.

### 7.4 Anti-patterns we have learned

| Anti-pattern | What happened |
|---|---|
| Fetching descriptions outside the connector | Ashby initially missed `descriptionHtml` → 281 jobs with empty skills. |
| Normalizing inside the connector | Connectors should return native dicts; normalization is centralized in `deterministic.py`. |
| Using a non-`id` field for change detection | The change detector only looks at `job["id"]`. If Workday uses a different key, the connector must map it to `id`. |
| Skipping jobs with missing descriptions | Jobs are still ingested; they just fail enrichment silently. Better to fetch the description or exclude the job explicitly. |

---

## 8. File Reference

| File | Purpose |
|---|---|
| `app/ingestion/connectors/base.py` | Abstract connector interface |
| `app/ingestion/connectors/greenhouse.py` | Greenhouse connector |
| `app/ingestion/connectors/lever.py` | Lever connector |
| `app/ingestion/connectors/ashby.py` | Ashby connector (two-step GraphQL) |
| `app/ingestion/connectors/workable.py` | Workable connector (single-call widget API) |
| `app/ingestion/fetcher.py` | Connector registry and dispatcher |
| `app/ingestion/pipeline.py` | Main ingestion orchestration |
| `app/ingestion/change_detector.py` | New/updated/unchanged/removed classification |
| `app/ingestion/extractor/deterministic.py` | Platform → common field mapping |
| `app/ingestion/extractor/text_cleaner.py` | HTML → plain text |
| `app/ingestion/enrichment_worker.py` | Async LLM enrichment queue |
| `app/ingestion/extractor/llm.py` | LLM prompt and output schema |
| `app/models/company.py` | Company model (`platform`, `board_token`) |
| `app/models/raw_job.py` | Raw job storage |
| `app/models/normalized_job.py` | Normalized job storage |
| `data/companies.json` | Seed data for companies and their platform tokens |

---

## 9. Existing Documentation

| Document | Coverage |
|---|---|
| **`greenhouse_connector_guide.md`** | Greenhouse list API + branded careers supplement (`gh_jid` discovery). |
| **`job_ingestion_v2.md`** | Full V2 architecture blueprint — schema, events, enrichment worker, connector registry. Sections 3 and 7 overlap with this guide. |
| **`job_ingestion_blueprint.md`** | V1 Greenhouse-only blueprint (historical). |
| **`IMPLEMENTATION_STATUS_V2.md`** | What's built vs planned. |
| **This guide** | Focused reference for implementing a new platform connector. |
