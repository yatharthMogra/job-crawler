"""Fat-fetch full job rows by ID for a recommendation page."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shared import NormalizedJob


async def fat_fetch_jobs_by_ids(
    db: AsyncSession,
    job_ids: list[UUID],
) -> list[NormalizedJob]:
    """Load full NormalizedJob rows (including description_text), preserving input order."""
    if not job_ids:
        return []
    rows = list(
        (
            await db.scalars(
                select(NormalizedJob).where(NormalizedJob.id.in_(job_ids))
            )
        ).all()
    )
    by_id = {job.id: job for job in rows}
    return [by_id[job_id] for job_id in job_ids if job_id in by_id]
