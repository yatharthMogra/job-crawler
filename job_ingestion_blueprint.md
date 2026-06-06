# Job Ingestion System — Implementation Blueprint

---

## 1. What We Are Building

A **backend-only, locally-running job ingestion pipeline** that:

- Periodically fetches job postings from Greenhouse-hosted company career pages
- Detects new, updated, unchanged, and removed postings
- Preserves raw source data before any transformation
- Extracts structured fields deterministically and enriches semantic fields via an LLM
- Stores normalized job records suitable for search and downstream use
- Tracks every pipeline run for debuggability
- Alerts (via `alerts.json`) when a company's fetch breaks repeatedly

The system is scoped to Greenhouse only. It does not crawl the internet. Input is a curated list of companies seeded from a JSON file into the database.

---

## 2. Tech Stack

| Concern | Choice | Reason |
|---|---|---|
| Language | Python 3.11+ | Ecosystem fit, team familiarity |
| Web framework | FastAPI | Async-native, clean routing, auto docs |
| Scheduling | APScheduler (AsyncIOScheduler) | Embedded, no external broker needed for V1 |
| HTTP client | httpx (async) | Async-native, cleaner than requests for concurrent fetches |
| Database | PostgreSQL 15 | JSONB for raw storage, relational for normalized |
| ORM | SQLAlchemy 2.x (async) + asyncpg | Async session support, type-safe queries |
| Migrations | Alembic | Schema versioning from day one |
| HTML parsing | BeautifulSoup4 | Strip HTML before LLM input |
| LLM provider | Gemini (google-generativeai) | Free tier for prototyping |
| LLM structuring | Instructor | Enforces Pydantic schema on LLM output |
| Config management | pydantic-settings | Typed .env parsing, no manual os.getenv |
| Structured logging | structlog | JSON logs, easy to grep and filter |
| Local infra | Docker Compose | Isolated Postgres, portable setup |
| Package manager | pip + pyproject.toml | Standard, simple |

---

## 3. Greenhouse API

Greenhouse exposes a public Job Board API. No authentication is required.

**Fetch all jobs for a company (with descriptions):**
```
GET https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true
```

Response is a JSON object with a `jobs` array. Each job includes:
- `id` — external job ID
- `title`
- `location.name`
- `departments[]`
- `offices[]`
- `updated_at`
- `absolute_url` — posting URL
- `content` — raw HTML job description (when `?content=true`)
- `metadata[]` — optional custom fields

**Fetch a single job:**
```
GET https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs/{job_id}
```

Used only if granular re-fetching is needed. For V1, the list endpoint with `?content=true` is sufficient — it returns everything in one call.

---

## 4. Database Schema

Six tables. All primary keys are UUIDs. All timestamps are UTC.

---

### `companies`

Stores the curated company list. This is the system's single source of truth for which companies to fetch.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| name | VARCHAR | e.g. "OpenAI" |
| platform | VARCHAR | "greenhouse" for V1 |
| board_token | VARCHAR UNIQUE | e.g. "openai" |
| is_active | BOOLEAN | Soft disable without deleting |
| consecutive_fetch_failures | INTEGER | Increments on failure, resets on success |
| last_successful_fetch_at | TIMESTAMP | Nullable until first success |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

---

### `raw_jobs`

Append-only ingestion archive. One row per fetch of a job. Never updated, only inserted.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| company_id | UUID FK → companies | |
| external_job_id | VARCHAR | Job ID from Greenhouse |
| platform | VARCHAR | "greenhouse" |
| raw_api_response | JSONB | Full Greenhouse API job object |
| raw_html | TEXT | Job description HTML (nullable) |
| content_hash | VARCHAR | SHA-256 of raw_api_response |
| fetch_timestamp | TIMESTAMP | When this row was written |
| created_at | TIMESTAMP | |

Index on `(company_id, external_job_id)` for change detection lookups.

---

### `normalized_jobs`

One row per unique job posting. Updated in place when a job changes.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| raw_job_id | UUID FK → raw_jobs | Points to the raw row that produced this extraction |
| company_id | UUID FK → companies | |
| external_job_id | VARCHAR | |
| title | VARCHAR | Deterministic |
| company_name | VARCHAR | Deterministic |
| location | VARCHAR | Deterministic |
| department | VARCHAR | Deterministic |
| employment_type | VARCHAR | Deterministic (if available) |
| posting_url | TEXT | Deterministic |
| posted_at | TIMESTAMP | Deterministic |
| is_active | BOOLEAN | Managed by inactive detection |
| consecutive_misses | INTEGER | Increments when job absent from fetch |
| last_seen_at | TIMESTAMP | Last fetch where job appeared |
| seniority | VARCHAR | LLM: "senior / mid / junior / new_grad / internship / unclear" |
| is_internship | BOOLEAN | LLM |
| is_new_grad | BOOLEAN | LLM |
| sponsorship_status | VARCHAR | LLM: "yes / no / unclear" |
| sponsorship_confidence | VARCHAR | LLM: "high / low" |
| remote_type | VARCHAR | LLM: "remote / hybrid / onsite / unclear" |
| tech_stack | VARCHAR[] | LLM |
| skills | VARCHAR[] | LLM |
| llm_provider | VARCHAR | e.g. "gemini" |
| llm_model | VARCHAR | e.g. "gemini-1.5-flash" |
| extraction_version | VARCHAR | e.g. "v1" — for future reprocessing |
| extracted_at | TIMESTAMP | |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

Unique constraint on `(company_id, external_job_id)`.

---

### `pipeline_runs`

One row per scheduled or manual pipeline execution.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| run_type | VARCHAR | "scheduled" or "manual" |
| status | VARCHAR | "running / completed / failed" |
| started_at | TIMESTAMP | |
| completed_at | TIMESTAMP | Nullable until done |
| total_companies | INTEGER | |
| successful_companies | INTEGER | |
| failed_companies | INTEGER | |
| jobs_fetched | INTEGER | Total jobs seen across all companies |
| jobs_new | INTEGER | |
| jobs_updated | INTEGER | |
| jobs_unchanged | INTEGER | |
| jobs_removed | INTEGER | Marked inactive this run |
| error_summary | JSONB | Nullable; list of per-company errors |

---

### `company_run_results`

One row per company per pipeline run. Granular per-company audit trail.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| pipeline_run_id | UUID FK → pipeline_runs | |
| company_id | UUID FK → companies | |
| status | VARCHAR | "success / failed" |
| jobs_fetched | INTEGER | |
| jobs_new | INTEGER | |
| jobs_updated | INTEGER | |
| jobs_unchanged | INTEGER | |
| jobs_removed | INTEGER | |
| error_message | TEXT | Nullable |
| started_at | TIMESTAMP | |
| completed_at | TIMESTAMP | |

---

## 5. Configuration

All config lives in a `.env` file and is loaded via `pydantic-settings`. Every tunable has a default.

```
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/jobingestion

# Scheduling
FETCH_CADENCE_HOURS=6

# Failure alerting
MAX_CONSECUTIVE_FAILURES_BEFORE_ALERT=3

# Inactive job detection
CONSECUTIVE_MISSES_BEFORE_INACTIVE=3

# LLM
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-flash
EXTRACTION_VERSION=v1

# Alerts
ALERTS_FILE_PATH=./alerts.json

# Logging
LOG_LEVEL=INFO
```

---

## 6. Project Structure

```
job_ingestion/
│
├── docker-compose.yml           # Postgres service
├── .env                         # Local secrets (gitignored)
├── .env.example                 # Committed template
├── pyproject.toml               # Dependencies + project metadata
│
├── alembic/
│   ├── env.py
│   └── versions/                # Migration files (auto-generated)
│
├── data/
│   └── companies.json           # Seed input — curated company list
│
├── alerts.json                  # Runtime alert log (auto-created)
│
└── app/
    ├── main.py                  # FastAPI app init, lifespan, router registration
    ├── config.py                # pydantic-settings Settings class
    ├── database.py              # Async engine, session factory, Base
    ├── scheduler.py             # APScheduler setup, job registration
    │
    ├── models/                  # SQLAlchemy ORM models
    │   ├── company.py
    │   ├── raw_job.py
    │   ├── normalized_job.py
    │   └── pipeline_run.py      # pipeline_runs + company_run_results
    │
    ├── schemas/                 # Pydantic schemas for API I/O
    │   ├── company.py
    │   ├── pipeline.py
    │   └── job.py
    │
    ├── api/                     # FastAPI routers
    │   ├── companies.py
    │   └── pipeline.py
    │
    ├── ingestion/               # Core pipeline logic
    │   ├── pipeline.py          # Top-level orchestrator
    │   ├── fetcher.py           # Greenhouse API fetching
    │   ├── change_detector.py   # new / updated / unchanged / removed
    │   ├── alerts.py            # alerts.json writer
    │   │
    │   └── extractor/
    │       ├── deterministic.py # Code-based field extraction
    │       ├── llm.py           # LLM enrichment call + schema
    │       └── text_cleaner.py  # HTML → clean text for LLM input
    │
    ├── llm/                     # LLM provider abstraction
    │   ├── base.py              # Abstract LLMProvider interface
    │   ├── gemini.py            # Gemini implementation
    │   └── factory.py           # Returns correct provider from config
    │
    └── utils/
        ├── hashing.py           # SHA-256 content hash helper
        ├── logging.py           # structlog configuration
        └── seed.py              # companies.json → DB upsert helper
```

---

## 7. Component Responsibilities

### `main.py`
- Initializes the FastAPI app
- Registers routers (`/companies`, `/pipeline`)
- Uses FastAPI `lifespan` to start APScheduler on startup and shut it down on teardown
- Sets up structlog

### `config.py`
- Single `Settings` class via `pydantic-settings`
- Reads all values from `.env`
- Imported as a singleton wherever config is needed

### `database.py`
- Creates the async SQLAlchemy engine from `DATABASE_URL`
- Defines `AsyncSessionLocal` session factory
- Defines `Base` for ORM models
- Provides `get_db()` dependency for FastAPI route injection

### `scheduler.py`
- Initializes `AsyncIOScheduler`
- Registers the pipeline trigger as a cron job with `FETCH_CADENCE_HOURS`
- Scheduler is started/stopped via FastAPI lifespan

---

### `ingestion/pipeline.py` — Orchestrator

This is the core entry point called by both the scheduler and the manual trigger endpoint.

Flow:
1. Create a `pipeline_runs` row with status `running`
2. Load all active companies from DB
3. For each company, run the per-company pipeline (catch exceptions, never let one company crash the run)
4. Aggregate stats across companies
5. Update `pipeline_runs` row with final status and counts

### `ingestion/fetcher.py` — Greenhouse Fetcher

Responsibilities:
- Accept a `company` record
- Call Greenhouse list endpoint: `GET /v1/boards/{board_token}/jobs?content=true`
- Return raw job list (list of dicts as returned by the API)
- Raise a typed exception on failure (HTTP error, timeout, malformed response)
- Does not write to DB — returns data only

### `ingestion/change_detector.py` — Change Detection

Responsibilities:
- Accept list of freshly fetched jobs for a company
- Load last known raw jobs for this company from DB (keyed by `external_job_id`)
- For each fetched job: compute content hash, compare against stored hash
  - Not in DB → **new**
  - In DB, hash differs → **updated**
  - In DB, hash same → **unchanged**
- For each stored job not present in fresh fetch → **candidate for removal**
  - Increment `consecutive_misses` on the `normalized_jobs` record
  - If `consecutive_misses >= N` → mark `is_active = False` → counts as **removed**
  - If `consecutive_misses < N` → do not change active status yet
- Returns a classified result object: `{new: [], updated: [], unchanged: [], removed: []}`

### `ingestion/extractor/text_cleaner.py`

- Accept raw HTML string from Greenhouse `content` field
- Strip all HTML tags via BeautifulSoup4
- Normalize whitespace
- Return clean plain text string

### `ingestion/extractor/deterministic.py`

- Accept a raw Greenhouse job dict
- Extract all directly available fields:
  - `title` → `job["title"]`
  - `location` → `job["location"]["name"]`
  - `department` → `job["departments"][0]["name"]` (first, if present)
  - `posting_url` → `job["absolute_url"]`
  - `posted_at` → `job["updated_at"]` (best available proxy)
  - `employment_type` → from `job["metadata"]` if present, else null
- Returns a dict of deterministic fields

### `ingestion/extractor/llm.py`

- Accept clean text (from `text_cleaner`)
- Build a structured prompt asking for semantic field extraction
- Call LLM via provider abstraction using Instructor
- Instructor enforces the following Pydantic output schema:

```python
class JobEnrichment(BaseModel):
    seniority: Literal["senior", "mid", "junior", "new_grad", "internship", "unclear"]
    is_internship: bool
    is_new_grad: bool
    sponsorship_status: Literal["yes", "no", "unclear"]
    sponsorship_confidence: Literal["high", "low"]
    remote_type: Literal["remote", "hybrid", "onsite", "unclear"]
    tech_stack: list[str]
    skills: list[str]
```

- Returns a `JobEnrichment` instance
- Logs LLM provider and model used (stored on the normalized job row)

### `ingestion/alerts.py` — Alert Writer

- Called when `consecutive_fetch_failures >= K` for a company
- Appends a JSON entry to `alerts.json`:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "company_id": "uuid",
  "company_name": "OpenAI",
  "board_token": "openai",
  "consecutive_failures": 3,
  "last_error": "HTTPError: 503 Service Unavailable"
}
```

- File is created on first write if it doesn't exist
- Append-only, one JSON object per line (newline-delimited JSON / NDJSON format — easy to tail and parse)

---

### `llm/base.py` — Abstract Interface

Defines an abstract `LLMProvider` class with a single method:
```
async def complete(system_prompt: str, user_prompt: str, response_model: type[BaseModel]) -> BaseModel
```

### `llm/gemini.py` — Gemini Implementation

- Wraps `google-generativeai` SDK
- Uses Instructor to patch the client for structured outputs
- Reads model name from config

### `llm/factory.py` — Provider Factory

- Reads `LLM_PROVIDER` from config
- Returns the correct `LLMProvider` implementation
- Adding a new provider (OpenAI, Anthropic) requires: implement `base.py`, register in `factory.py`, add config keys — nothing else changes

---

### `utils/seed.py` — Company Seeder

- Reads `data/companies.json`
- For each entry, upserts into `companies` table keyed on `board_token`
  - If `board_token` exists → update name, mark active
  - If not → insert new row
- Called via `POST /companies/seed` endpoint or directly as a script

`data/companies.json` format:
```json
[
  { "company": "OpenAI", "platform": "greenhouse", "board_token": "openai" },
  { "company": "Anthropic", "platform": "greenhouse", "board_token": "anthropic" }
]
```

---

## 8. API Endpoints

### Pipeline

| Method | Path | Description |
|---|---|---|
| POST | `/pipeline/trigger` | Manually trigger a full pipeline run |
| GET | `/pipeline/runs` | List recent pipeline runs (paginated) |
| GET | `/pipeline/runs/{run_id}` | Get a specific run with per-company breakdown |

### Companies

| Method | Path | Description |
|---|---|---|
| GET | `/companies` | List all companies |
| GET | `/companies/{company_id}` | Get company + failure count + last fetch time |
| POST | `/companies/seed` | Re-run seed from `data/companies.json` |
| PATCH | `/companies/{company_id}` | Toggle `is_active`, update metadata |

---

## 9. Full Pipeline Data Flow

```
APScheduler / POST /pipeline/trigger
            │
            ▼
    pipeline_runs INSERT (status: running)
            │
            ▼
    Load active companies from DB
            │
     ┌──────┴────────────────────────┐
     │  Per-company loop             │
     │                               │
     │  1. Fetcher                   │
     │     └─ GET Greenhouse API     │
     │        (raises on failure)    │
     │                               │
     │  2. Change Detector           │
     │     └─ Hash + compare vs DB   │
     │     └─ Classify each job      │
     │                               │
     │  3. For NEW + UPDATED jobs:   │
     │     a. Insert into raw_jobs   │
     │     b. Deterministic extract  │
     │     c. Clean HTML → text      │
     │     d. LLM enrich             │
     │     e. Upsert normalized_jobs │
     │                               │
     │  4. For REMOVED candidates:   │
     │     └─ Increment miss counter │
     │     └─ Deactivate if >= N     │
     │                               │
     │  5. company_run_results INSERT│
     │                               │
     │  6. On failure:               │
     │     └─ Increment company      │
     │        consecutive_failures   │
     │     └─ If >= K: write alert   │
     │        to alerts.json         │
     │     └─ On success: reset to 0 │
     └──────────────────────────────-┘
            │
            ▼
    pipeline_runs UPDATE (status: completed, stats)
```

---

## 10. Docker Compose Setup

One service for V1: Postgres.

```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: jobingestion
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

FastAPI runs locally with `uvicorn`, not containerized in V1.

---

## 11. Local Development Startup Sequence

```bash
# 1. Start Postgres
docker compose up -d

# 2. Install dependencies
pip install -e .

# 3. Copy and fill env
cp .env.example .env

# 4. Run migrations
alembic upgrade head

# 5. Seed companies
python -m app.utils.seed
# or: POST /companies/seed via API

# 6. Start the app
uvicorn app.main:app --reload --port 8000

# Scheduler fires automatically on startup
# Manual trigger: POST http://localhost:8000/pipeline/trigger
# API docs: http://localhost:8000/docs
```

---

## 12. Key Design Rules to Enforce During Implementation

- **Fetcher returns data only.** It never writes to DB. The orchestrator writes.
- **raw_jobs is append-only.** Never update a raw row. Always insert.
- **Change detection is the gatekeeper.** Extraction only runs for new/updated. Unchanged jobs are fully skipped.
- **LLM receives clean text, never raw HTML.** The text cleaner is always called before the LLM.
- **All config is read from `Settings`.** No hardcoded values anywhere in business logic.
- **One company failure never stops the run.** Exceptions per company are caught, logged, and recorded. The loop continues.
- **`consecutive_fetch_failures` lives on the company record.** Don't derive it from pipeline_runs at runtime.
- **`consecutive_misses` lives on the normalized_job record.** Same principle.
- **`extraction_version` is stamped on every normalized_job row.** Required for future reprocessing without full re-fetch.
- **structlog is configured once in `utils/logging.py` and imported everywhere.** Never use `print()` or bare `logging.getLogger()`.
