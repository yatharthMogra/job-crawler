from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

try:
    import structlog
except ImportError:  # pragma: no cover
    import logging

    structlog = None  # type: ignore[assignment]

from app.config import get_settings
from app.ingestion.job_purge import PurgeTarget, purge_normalized_jobs
from app.models.normalized_job import NormalizedJob

log = structlog.get_logger() if structlog else logging.getLogger(__name__)


async def run_active_cleanup(db: AsyncSession) -> dict:
    settings = get_settings()
    cutoff = datetime.now(timezone.utc) - timedelta(days=settings.job_max_age_days)
    batch_size = settings.cleanup_batch_size
    total_deleted = 0

    log.info("active_cleanup_started", cutoff=cutoff.isoformat())

    while True:
        result = await db.execute(
            select(NormalizedJob.id, NormalizedJob.raw_job_id, NormalizedJob.job_archive_id)
            .where(NormalizedJob.reference_at < cutoff)
            .limit(batch_size)
        )
        rows = result.all()
        if not rows:
            break

        purge_rows = [
            PurgeTarget(id=row.id, raw_job_id=row.raw_job_id, job_archive_id=row.job_archive_id)
            for row in rows
        ]
        deleted = await purge_normalized_jobs(db, purge_rows)
        await db.commit()
        total_deleted += deleted
        log.info("active_cleanup_batch", deleted=deleted, total_so_far=total_deleted)

        if len(rows) < batch_size:
            break

    log.info("active_cleanup_completed", total_deleted=total_deleted)
    return {"deleted": total_deleted, "cutoff": cutoff.isoformat()}
