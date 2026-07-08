from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company_watch import CompanyWatchSubscription
from app.models.notification_preferences import NotificationPreferences
from app.models.shared import NormalizedJob


def _ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


async def get_company_watch_watermark(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    company_id: uuid.UUID,
    prefs: NotificationPreferences,
) -> datetime | None:
    """Last batch send time, or per-company subscription created_at when no mail sent yet."""
    if prefs.last_company_watch_batch_at is not None:
        return prefs.last_company_watch_batch_at
    return await db.scalar(
        select(CompanyWatchSubscription.created_at).where(
            CompanyWatchSubscription.candidate_id == candidate_id,
            CompanyWatchSubscription.company_id == company_id,
            CompanyWatchSubscription.is_active.is_(True),
        )
    )


def job_reference_at_after_watermark(job: NormalizedJob, watermark: datetime | None) -> bool:
    if watermark is None or job.reference_at is None:
        return False
    return _ensure_utc(job.reference_at) > _ensure_utc(watermark)
