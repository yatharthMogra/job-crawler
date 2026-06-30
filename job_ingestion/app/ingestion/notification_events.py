from __future__ import annotations

import uuid

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def enqueue_notification_job_events(
    db: AsyncSession,
    jobs: list[tuple[uuid.UUID, uuid.UUID]],
) -> None:
    """Insert rows into notification_job_events for successfully enriched jobs."""
    if not jobs:
        return

    for job_id, company_id in jobs:
        await db.execute(
            text(
                """
                INSERT INTO notification_job_events (id, job_id, company_id, enqueued_at)
                VALUES (gen_random_uuid(), :job_id, :company_id, NOW())
                """
            ),
            {"job_id": job_id, "company_id": company_id},
        )
