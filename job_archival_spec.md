# Job Archival & Deletion — Implementation Spec

---

## 1. What This Builds

A two-table, two-job archival system that keeps the active DB lean while preserving job history for users who applied.

**Core model:**
- `job_archive` — created at ingestion alongside `normalized_jobs`. Lives for 100 days. Source of truth for applied job history.
- `normalized_jobs` — active recommendation/notification layer. Deleted at 7 days.

**Two nightly jobs:**
- `active_cleanup` (2am) — deletes `normalized_jobs`, `job_enrichments`, `raw_jobs` older than 7 days.
- `archive_cleanup` (2:30am) — dumps `job_archive` rows older than 100 days to JSONL, then deletes them.

---

## 2. Schema

### 2.1 New table: `job_archive`

```sql
CREATE TABLE job_archive (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Identity
    external_job_id     VARCHAR NOT NULL,
    company_id          UUID NOT NULL REFERENCES companies(id),
    company_name        VARCHAR NOT NULL,
    platform            VARCHAR NOT NULL,

    -- Deterministic fields (populated at ingestion)
    title               VARCHAR,
    location            VARCHAR,
    department          VARCHAR,
    posting_url         TEXT,
    employment_type     VARCHAR,
    salary_min          INTEGER,
    salary_max          INTEGER,
    original_posted_at  TIMESTAMP WITH TIME ZONE,

    -- Enriched fields (populated after LLM enrichment)
    seniority           VARCHAR,
    normalized_roles    VARCHAR[],
    job_capabilities    VARCHAR[],
    skills              VARCHAR[],
    tech_stack          VARCHAR[],
    remote_type         VARCHAR,
    description_text    TEXT,       -- plain text from raw_html

    -- Lifecycle
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    archived_at         TIMESTAMP WITH TIME ZONE,   -- set when normalized_jobs row is deleted

    UNIQUE (external_job_id, company_id)
);

CREATE INDEX idx_job_archive_company_id ON job_archive(company_id);
CREATE INDEX idx_job_archive_original_posted_at ON job_archive(original_posted_at);
```

---

### 2.2 Modified table: `normalized_jobs`

Add one column:

```sql
ALTER TABLE normalized_jobs
ADD COLUMN job_archive_id UUID REFERENCES job_archive(id);

CREATE INDEX idx_normalized_jobs_job_archive_id ON normalized_jobs(job_archive_id);
```

No cascade — `normalized_jobs` is deleted first; `job_archive` outlives it.

---

### 2.3 New table: `user_applications`

```sql
CREATE TABLE user_applications (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id        UUID NOT NULL REFERENCES candidates(id),

    -- FK to job_archive (ON DELETE SET NULL — job_archive deleted at 100 days)
    job_archive_id      UUID REFERENCES job_archive(id) ON DELETE SET NULL,

    -- Denormalized safety copies (always populated, survive job_archive deletion)
    company_name        VARCHAR NOT NULL,
    job_title           VARCHAR NOT NULL,
    location            VARCHAR,
    platform            VARCHAR,
    external_job_id     VARCHAR,    -- for reference only, not a FK

    -- User-managed fields
    applied_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    status              VARCHAR NOT NULL DEFAULT 'applied',
    -- valid values: applied / interviewing / offer / rejected / withdrawn
    notes               TEXT,

    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),

    UNIQUE (candidate_id, job_archive_id)  -- prevent duplicate applications
);

CREATE INDEX idx_user_applications_candidate_id ON user_applications(candidate_id);
CREATE INDEX idx_user_applications_applied_at ON user_applications(applied_at);
```

---

### 2.4 Alembic migration

One migration file:

```
alembic/versions/YYYYMMDD_XXXX_job_archival_tables.py
```

Order within the migration:
1. Create `job_archive`
2. Add `job_archive_id` column to `normalized_jobs`
3. Create `user_applications`

---

## 3. Config Additions

```env
# Archival
ACTIVE_JOB_RETENTION_DAYS=7
ARCHIVE_RETENTION_DAYS=100
CLEANUP_BATCH_SIZE=500
ARCHIVE_DIR=data/archives
```

Add to `app/config.py`:

```python
active_job_retention_days: int = 7
archive_retention_days: int = 100
cleanup_batch_size: int = 500
archive_dir: str = "data/archives"
```

---

## 4. Project Structure

```
app/
├── archival/
│   ├── __init__.py
│   ├── archiver.py         # orchestrates both cleanup jobs
│   ├── active_cleanup.py   # 7-day normalized_jobs deletion
│   ├── archive_cleanup.py  # 100-day job_archive JSONL dump + deletion
│   └── writer.py           # JSONL file writer
├── models/
│   ├── job_archive.py      # new SQLAlchemy model
│   └── user_application.py # new SQLAlchemy model
└── api/
    └── maintenance.py      # manual trigger endpoints
```

---

## 5. Ingestion Pipeline Changes

### 5.1 Write to `job_archive` at ingestion time

In `app/ingestion/pipeline.py`, the current flow writes to `normalized_jobs` after deterministic extraction. Add `job_archive` write immediately before `normalized_jobs`:

```python
# pipeline.py — inside per-job processing, after deterministic extraction

async def _upsert_job_archive(det_fields: dict, company: Company, db: AsyncSession) -> UUID:
    """
    Insert or update job_archive row. Returns the job_archive.id.
    Upsert on (external_job_id, company_id) — handles re-ingestion of updated jobs.
    """
    stmt = pg_insert(JobArchive).values(
        external_job_id=det_fields["external_job_id"],
        company_id=company.id,
        company_name=company.name,
        platform=company.platform,
        title=det_fields.get("title"),
        location=det_fields.get("location"),
        department=det_fields.get("department"),
        posting_url=det_fields.get("posting_url"),
        employment_type=det_fields.get("employment_type"),
        salary_min=det_fields.get("salary_min"),
        salary_max=det_fields.get("salary_max"),
        original_posted_at=det_fields.get("posted_at"),
        description_text=clean_job_description(det_fields.get("raw_html", "")),
    ).on_conflict_do_update(
        index_elements=["external_job_id", "company_id"],
        set_={
            "title": det_fields.get("title"),
            "location": det_fields.get("location"),
            "posting_url": det_fields.get("posting_url"),
            "description_text": clean_job_description(det_fields.get("raw_html", "")),
        }
    ).returning(JobArchive.id)

    result = await db.execute(stmt)
    return result.scalar_one()
```

Then when writing `normalized_jobs`:

```python
job_archive_id = await _upsert_job_archive(det_fields, company, db)

await upsert_normalized_job(
    det_fields=det_fields,
    company=company,
    job_archive_id=job_archive_id,   # new field
    db=db,
)
```

**Write order within per-job transaction:**
1. `job_archive` upsert → get `job_archive_id`
2. `normalized_jobs` upsert with `job_archive_id`
3. `raw_jobs` insert

If `job_archive` write fails → raise, skip job. If `normalized_jobs` write fails → `job_archive` row exists orphaned but that is harmless (it has no description_text gaps, will be cleaned at 100 days).

---

### 5.2 Enrichment worker update

After enrichment completes and `normalized_jobs` is updated, also update `job_archive`:

In `app/ingestion/enrichment_worker.py` (or wherever enrichment writes back):

```python
async def _update_job_archive_after_enrichment(
    job_archive_id: UUID,
    enrichment: JobEnrichment,
    db: AsyncSession,
) -> None:
    """
    Populate enriched fields in job_archive after LLM enrichment completes.
    These are the fields users see in their applied history.
    """
    await db.execute(
        update(JobArchive)
        .where(JobArchive.id == job_archive_id)
        .values(
            seniority=enrichment.seniority,
            normalized_roles=enrichment.normalized_roles,
            job_capabilities=enrichment.job_capabilities,
            skills=enrichment.skills,
            tech_stack=enrichment.tech_stack,
            remote_type=enrichment.remote_type,
            salary_min=enrichment.salary_min or None,  # enrichment may refine salary
            salary_max=enrichment.salary_max or None,
        )
    )
```

Retrieve `job_archive_id` from the `normalized_jobs` row being enriched — it's already stored there.

---

## 6. Archival Module

### 6.1 `app/archival/writer.py`

```python
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from app.config import settings


def get_archive_filepath(run_date: datetime | None = None) -> Path:
    date_str = (run_date or datetime.now(timezone.utc)).strftime("%Y-%m-%d")
    path = Path(settings.archive_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path / f"jobs_{date_str}.jsonl"


def serialize_for_archive(job_archive_row: dict) -> str:
    """
    Serialize a job_archive row dict to a JSON line.
    Handles UUID and datetime serialization.
    """
    def default(obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, list):
            return obj
        raise TypeError(f"Not serializable: {type(obj)}")

    return json.dumps(job_archive_row, default=default, ensure_ascii=False)


def write_archive_batch(rows: list[dict], filepath: Path) -> int:
    """
    Append rows to JSONL archive file. Returns number of rows written.
    Uses fsync to ensure data is flushed before deletion proceeds.
    """
    lines = [serialize_for_archive(row) for row in rows]
    with open(filepath, "a", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
        f.flush()
        os.fsync(f.fileno())
    return len(lines)
```

---

### 6.2 `app/archival/active_cleanup.py`

Deletes `normalized_jobs`, `job_enrichments`, and `raw_jobs` older than 7 days.

```python
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.normalized_job import NormalizedJob
from app.models.job_enrichment import JobEnrichment
from app.models.raw_job import RawJob
from app.models.job_archive import JobArchive
import structlog

log = structlog.get_logger()


async def run_active_cleanup(db: AsyncSession) -> dict:
    """
    Delete normalized_jobs, job_enrichments, and raw_jobs older than ACTIVE_JOB_RETENTION_DAYS.
    Processes in batches to avoid large transactions.
    Returns stats dict.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=settings.active_job_retention_days)
    batch_size = settings.cleanup_batch_size
    total_deleted = 0

    log.info("active_cleanup_started", cutoff=cutoff.isoformat())

    while True:
        # Step 1: Fetch a batch of expired normalized_jobs
        result = await db.execute(
            select(NormalizedJob.id, NormalizedJob.raw_job_id, NormalizedJob.job_archive_id)
            .where(NormalizedJob.posted_at < cutoff)
            .where(NormalizedJob.is_active == True)
            .limit(batch_size)
        )
        rows = result.all()
        if not rows:
            break

        normalized_ids = [r.id for r in rows]
        raw_job_ids = [r.raw_job_id for r in rows if r.raw_job_id]
        archive_ids = [r.job_archive_id for r in rows if r.job_archive_id]

        # Step 2: Delete job_enrichments (FK to normalized_jobs)
        await db.execute(
            delete(JobEnrichment).where(JobEnrichment.normalized_job_id.in_(normalized_ids))
        )

        # Step 3: Delete normalized_jobs
        await db.execute(
            delete(NormalizedJob).where(NormalizedJob.id.in_(normalized_ids))
        )

        # Step 4: Delete raw_jobs
        if raw_job_ids:
            await db.execute(
                delete(RawJob).where(RawJob.id.in_(raw_job_ids))
            )

        # Step 5: Stamp archived_at on job_archive rows
        if archive_ids:
            from sqlalchemy import update
            await db.execute(
                update(JobArchive)
                .where(JobArchive.id.in_(archive_ids))
                .values(archived_at=datetime.now(timezone.utc))
            )

        await db.commit()
        total_deleted += len(normalized_ids)

        log.info("active_cleanup_batch", deleted=len(normalized_ids), total_so_far=total_deleted)

        if len(rows) < batch_size:
            break

    log.info("active_cleanup_completed", total_deleted=total_deleted)
    return {"deleted": total_deleted, "cutoff": cutoff.isoformat()}
```

---

### 6.3 `app/archival/archive_cleanup.py`

Dumps `job_archive` rows older than 100 days to JSONL, then deletes them.

```python
from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.archival.writer import get_archive_filepath, write_archive_batch
from app.config import settings
from app.models.job_archive import JobArchive
import structlog

log = structlog.get_logger()


async def run_archive_cleanup(db: AsyncSession) -> dict:
    """
    JSONL dump + delete job_archive rows older than ARCHIVE_RETENTION_DAYS.
    ON DELETE SET NULL handles user_applications.job_archive_id automatically.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=settings.archive_retention_days)
    batch_size = settings.cleanup_batch_size
    filepath = get_archive_filepath()
    total_archived = 0
    total_deleted = 0

    log.info("archive_cleanup_started", cutoff=cutoff.isoformat(), file=str(filepath))

    while True:
        # Step 1: Fetch a batch of expired job_archive rows
        result = await db.execute(
            select(JobArchive)
            .where(JobArchive.original_posted_at < cutoff)
            .limit(batch_size)
        )
        rows = result.scalars().all()
        if not rows:
            break

        # Step 2: Serialize to JSONL — must succeed before deletion
        archive_rows = [_job_archive_to_dict(row) for row in rows]
        written = write_archive_batch(archive_rows, filepath)
        total_archived += written

        # Step 3: Delete from job_archive (ON DELETE SET NULL handles user_applications FK)
        ids_to_delete = [row.id for row in rows]
        await db.execute(
            delete(JobArchive).where(JobArchive.id.in_(ids_to_delete))
        )
        await db.commit()
        total_deleted += len(ids_to_delete)

        log.info("archive_cleanup_batch", dumped=written, deleted=len(ids_to_delete))

        if len(rows) < batch_size:
            break

    log.info("archive_cleanup_completed",
             total_archived=total_archived,
             total_deleted=total_deleted,
             file=str(filepath))

    return {
        "archived_to_file": total_archived,
        "deleted": total_deleted,
        "file": str(filepath),
        "cutoff": cutoff.isoformat(),
    }


def _job_archive_to_dict(row: JobArchive) -> dict:
    return {
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "archive_reason": "age_100_days",
        "id": str(row.id),
        "external_job_id": row.external_job_id,
        "company_id": str(row.company_id),
        "company_name": row.company_name,
        "platform": row.platform,
        "title": row.title,
        "location": row.location,
        "department": row.department,
        "posting_url": row.posting_url,
        "employment_type": row.employment_type,
        "salary_min": row.salary_min,
        "salary_max": row.salary_max,
        "seniority": row.seniority,
        "normalized_roles": row.normalized_roles,
        "job_capabilities": row.job_capabilities,
        "skills": row.skills,
        "tech_stack": row.tech_stack,
        "remote_type": row.remote_type,
        "description_text": row.description_text,
        "original_posted_at": row.original_posted_at.isoformat() if row.original_posted_at else None,
        "created_at": row.created_at.isoformat(),
        "archived_at": row.archived_at.isoformat() if row.archived_at else None,
    }
```

---

### 6.4 `app/archival/archiver.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession

from app.archival.active_cleanup import run_active_cleanup
from app.archival.archive_cleanup import run_archive_cleanup
import structlog

log = structlog.get_logger()


async def run_all_cleanup(db: AsyncSession) -> dict:
    """Entry point for manual trigger endpoint."""
    active_stats = await run_active_cleanup(db)
    archive_stats = await run_archive_cleanup(db)
    return {"active_cleanup": active_stats, "archive_cleanup": archive_stats}
```

---

## 7. Scheduler Registration

In `app/scheduler.py`:

```python
from app.archival.active_cleanup import run_active_cleanup
from app.archival.archive_cleanup import run_archive_cleanup

scheduler.add_job(
    run_active_cleanup_job,
    trigger="cron",
    hour=2,
    minute=0,
    id="active_cleanup",
    replace_existing=True,
)

scheduler.add_job(
    run_archive_cleanup_job,
    trigger="cron",
    hour=2,
    minute=30,
    id="archive_cleanup",
    replace_existing=True,
)


async def run_active_cleanup_job():
    async with AsyncSessionLocal() as db:
        await run_active_cleanup(db)


async def run_archive_cleanup_job():
    async with AsyncSessionLocal() as db:
        await run_archive_cleanup(db)
```

---

## 8. API Endpoints

In `app/api/maintenance.py`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.archival.archiver import run_all_cleanup
from app.archival.active_cleanup import run_active_cleanup
from app.archival.archive_cleanup import run_archive_cleanup
from app.database import get_db

router = APIRouter(prefix="/maintenance", tags=["maintenance"])


@router.post("/cleanup")
async def trigger_full_cleanup(db: AsyncSession = Depends(get_db)):
    """Manually trigger both active and archive cleanup."""
    return await run_all_cleanup(db)


@router.post("/cleanup/active")
async def trigger_active_cleanup(db: AsyncSession = Depends(get_db)):
    """Manually trigger 7-day normalized_jobs cleanup only."""
    return await run_active_cleanup(db)


@router.post("/cleanup/archive")
async def trigger_archive_cleanup(db: AsyncSession = Depends(get_db)):
    """Manually trigger 100-day job_archive JSONL dump + deletion."""
    return await run_archive_cleanup(db)
```

Register in `app/main.py`:

```python
from app.api.maintenance import router as maintenance_router
app.include_router(maintenance_router)
```

---

## 9. Display Query for Applied History

The front-end or dashboard API calls this for a user's applied jobs:

```python
async def get_user_applications(candidate_id: UUID, db: AsyncSession) -> list[dict]:
    result = await db.execute(
        select(
            UserApplication,
            JobArchive.title.label("archive_title"),
            JobArchive.company_name.label("archive_company"),
            JobArchive.location.label("archive_location"),
            JobArchive.salary_min,
            JobArchive.salary_max,
            JobArchive.description_text,
            JobArchive.skills,
            JobArchive.seniority,
            JobArchive.posting_url,
        )
        .outerjoin(JobArchive, UserApplication.job_archive_id == JobArchive.id)
        .where(UserApplication.candidate_id == candidate_id)
        .order_by(UserApplication.applied_at.desc())
    )

    rows = result.all()
    return [_format_application(row) for row in rows]


def _format_application(row) -> dict:
    ua = row.UserApplication
    return {
        "applied_at": ua.applied_at,
        "status": ua.status,
        "notes": ua.notes,
        # Use archive data when available, fall back to denormalized copy
        "title": row.archive_title or ua.job_title,
        "company_name": row.archive_company or ua.company_name,
        "location": row.archive_location or ua.location,
        "salary_min": row.salary_min,
        "salary_max": row.salary_max,
        "description_text": row.description_text,    # None after day 100
        "skills": row.skills,
        "seniority": row.seniority,
        "posting_url": row.posting_url,
    }
```

---

## 10. Tests

| Test | What it verifies |
|---|---|
| `test_ingestion_creates_job_archive` | job_archive row created at ingest time; normalized_jobs.job_archive_id is populated |
| `test_enrichment_updates_job_archive` | enrichment worker populates seniority/skills/tech_stack on job_archive row |
| `test_active_cleanup_deletes_expired` | jobs with `posted_at` > 7 days are deleted from normalized_jobs, raw_jobs, job_enrichments |
| `test_active_cleanup_skips_recent` | jobs within 7 days are untouched |
| `test_active_cleanup_stamps_archived_at` | job_archive.archived_at is set after normalized_jobs deletion |
| `test_active_cleanup_batch_limit` | with 1200 expired jobs, cleanup processes in batches of 500 |
| `test_archive_cleanup_writes_jsonl` | JSONL file exists and has correct number of lines before deletion |
| `test_archive_cleanup_deletes_expired` | job_archive rows > 100 days are deleted from DB |
| `test_archive_cleanup_set_null` | user_applications.job_archive_id becomes NULL after job_archive deletion |
| `test_archive_cleanup_preserves_recent` | job_archive rows < 100 days untouched |
| `test_jsonl_writer_fsync` | JSONL file is flushed before deletion runs (mocked fsync) |
| `test_user_application_display_query` | returns archive data when job_archive exists, falls back to denormalized copy when NULL |
| `test_first_run_large_batch` | simulate 5000 expired jobs, confirm all deleted across multiple batches without timeout |

---

## 11. Build Sequence

Do these in order. Each step is testable before the next.

**Step 1 — Schema**
Alembic migration: `job_archive`, `job_archive_id` on `normalized_jobs`, `user_applications`.

**Step 2 — Models**
SQLAlchemy models for `JobArchive` and `UserApplication`.

**Step 3 — Ingestion pipeline**
`_upsert_job_archive()` in `pipeline.py`. Wire before `normalized_jobs` write.
Test: run ingestion for one company, confirm `job_archive` rows created with correct fields.

**Step 4 — Enrichment worker**
`_update_job_archive_after_enrichment()`. Wire after enrichment write-back.
Test: confirm `seniority`, `skills`, `description_text` populated on `job_archive` after enrichment.

**Step 5 — JSONL writer**
`app/archival/writer.py`. Unit test serialization and fsync behavior.

**Step 6 — Active cleanup**
`active_cleanup.py` + scheduler registration.
Manual test via `POST /maintenance/cleanup/active` with `ACTIVE_JOB_RETENTION_DAYS=0` to force deletion of all jobs. Verify counts match expected.

**Step 7 — Archive cleanup**
`archive_cleanup.py` + scheduler registration.
Manual test via `POST /maintenance/cleanup/archive` with `ARCHIVE_RETENTION_DAYS=0`. Verify JSONL file created and DB rows deleted.

**Step 8 — Applied history API**
`user_applications` write path (when user marks applied). Display query endpoint.

**Step 9 — Full integration test**
Seed jobs, run ingestion, run enrichment, delete via active_cleanup, confirm job_archive intact, apply as user, run archive_cleanup, confirm user_applications.job_archive_id is NULL but denormalized fields remain.

---

## 12. Key Rules to Enforce

- **JSONL write before delete — always.** The `archive_cleanup` must write to file and fsync before any DB delete. If the file write fails, the batch is skipped and retried on the next run.
- **Batch all deletes.** Never delete more than `CLEANUP_BATCH_SIZE` rows in a single transaction. First run could affect thousands of rows.
- **`job_archive` upsert, not insert.** A re-ingested updated job (content hash changed) must update the existing `job_archive` row, not create a duplicate. The unique constraint on `(external_job_id, company_id)` enforces this.
- **Enrichment always updates `job_archive`.** Any enrichment write-back that doesn't also update `job_archive` means applied history loses enriched metadata.
- **`archived_at` is diagnostic only.** Set it when active_cleanup runs, but don't depend on it for deletion logic — use `original_posted_at` as the single source of truth for all retention cutoffs.
