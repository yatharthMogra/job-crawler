from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enrichment_queue import EnrichmentQueue
from app.models.job_archive import JobArchive
from app.models.job_enrichment import JobEnrichment
from app.models.normalized_job import NormalizedJob
from app.models.raw_job import RawJob


@dataclass(frozen=True)
class PurgeTarget:
    id: UUID
    raw_job_id: UUID | None
    job_archive_id: UUID | None


async def purge_normalized_jobs(db: AsyncSession, rows: list[PurgeTarget]) -> int:
    if not rows:
        return 0

    normalized_ids = [row.id for row in rows]
    raw_job_ids = [row.raw_job_id for row in rows if row.raw_job_id]
    archive_ids = [row.job_archive_id for row in rows if row.job_archive_id]

    await db.execute(delete(EnrichmentQueue).where(EnrichmentQueue.normalized_job_id.in_(normalized_ids)))
    await db.execute(delete(JobEnrichment).where(JobEnrichment.normalized_job_id.in_(normalized_ids)))
    await db.execute(delete(NormalizedJob).where(NormalizedJob.id.in_(normalized_ids)))
    if raw_job_ids:
        await db.execute(delete(RawJob).where(RawJob.id.in_(raw_job_ids)))
    if archive_ids:
        await db.execute(
            update(JobArchive)
            .where(JobArchive.id.in_(archive_ids))
            .values(archived_at=datetime.now(timezone.utc))
        )
    return len(normalized_ids)
