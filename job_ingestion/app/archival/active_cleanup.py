from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

try:
    import structlog
except ImportError:  # pragma: no cover
    import logging

    structlog = None  # type: ignore[assignment]

from app.config import get_settings
from app.models.job_archive import JobArchive
from app.models.job_enrichment import JobEnrichment
from app.models.normalized_job import NormalizedJob
from app.models.raw_job import RawJob

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
            .where(NormalizedJob.posted_at < cutoff)
            .where(NormalizedJob.is_active.is_(True))
            .limit(batch_size)
        )
        rows = result.all()
        if not rows:
            break

        normalized_ids = [r.id for r in rows]
        raw_job_ids = [r.raw_job_id for r in rows if r.raw_job_id]
        archive_ids = [r.job_archive_id for r in rows if r.job_archive_id]

        await db.execute(
            delete(JobEnrichment).where(JobEnrichment.normalized_job_id.in_(normalized_ids))
        )
        await db.execute(delete(NormalizedJob).where(NormalizedJob.id.in_(normalized_ids)))
        if raw_job_ids:
            await db.execute(delete(RawJob).where(RawJob.id.in_(raw_job_ids)))
        if archive_ids:
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
