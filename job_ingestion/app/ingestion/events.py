from __future__ import annotations

from typing import Any, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ingestion_event import IngestionEvent


async def write_event(
    db: AsyncSession,
    event_type: str,
    category: str,
    severity: str,
    platform: Optional[str] = None,
    company_id: Optional[UUID] = None,
    pipeline_run_id: Optional[UUID] = None,
    normalized_job_id: Optional[UUID] = None,
    metadata: Optional[dict[str, Any]] = None,
) -> None:
    db.add(
        IngestionEvent(
            event_type=event_type,
            event_category=category,
            severity=severity,
            platform=platform,
            company_id=company_id,
            pipeline_run_id=pipeline_run_id,
            normalized_job_id=normalized_job_id,
            event_metadata=metadata or {},
        )
    )
    await db.flush()
