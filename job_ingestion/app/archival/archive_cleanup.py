from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

try:
    import structlog
except ImportError:  # pragma: no cover
    import logging

    structlog = None  # type: ignore[assignment]

from app.archival.writer import get_archive_filepath, write_archive_batch
from app.config import get_settings
from app.models.job_archive import JobArchive

log = structlog.get_logger() if structlog else logging.getLogger(__name__)


def _job_archive_to_dict(row: JobArchive) -> dict:
    return {
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
        "dumped_at": datetime.now(timezone.utc).isoformat(),
    }


async def run_archive_cleanup(db: AsyncSession) -> dict:
    from datetime import timedelta

    settings = get_settings()
    cutoff = datetime.now(timezone.utc) - timedelta(days=settings.archive_retention_days)
    batch_size = settings.cleanup_batch_size
    filepath = get_archive_filepath()
    total_archived = 0
    total_deleted = 0

    log.info("archive_cleanup_started", cutoff=cutoff.isoformat(), file=str(filepath))

    while True:
        result = await db.execute(
            select(JobArchive)
            .where(JobArchive.original_posted_at < cutoff)
            .limit(batch_size)
        )
        rows = result.scalars().all()
        if not rows:
            break

        archive_rows = [_job_archive_to_dict(row) for row in rows]
        written = write_archive_batch(archive_rows, filepath)
        total_archived += written

        ids_to_delete = [row.id for row in rows]
        await db.execute(delete(JobArchive).where(JobArchive.id.in_(ids_to_delete)))
        await db.commit()
        total_deleted += len(ids_to_delete)

        log.info("archive_cleanup_batch", dumped=written, deleted=len(ids_to_delete))

        if len(rows) < batch_size:
            break

    log.info(
        "archive_cleanup_completed",
        total_archived=total_archived,
        total_deleted=total_deleted,
        file=str(filepath),
    )
    return {
        "archived_to_file": total_archived,
        "deleted": total_deleted,
        "file": str(filepath),
        "cutoff": cutoff.isoformat(),
    }
