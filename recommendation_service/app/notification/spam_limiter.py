from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import NotificationBatch


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


async def count_emails_sent_today(db: AsyncSession, candidate_id: uuid.UUID) -> int:
    cutoff = _utcnow() - timedelta(hours=24)
    count = await db.scalar(
        select(func.count())
        .select_from(NotificationBatch)
        .where(
            NotificationBatch.candidate_id == candidate_id,
            NotificationBatch.status == "sent",
            NotificationBatch.email_delivered.is_(True),
            NotificationBatch.sent_at.is_not(None),
            NotificationBatch.sent_at >= cutoff,
        )
    )
    return int(count or 0)


async def can_send_email(
    db: AsyncSession,
    candidate_id: uuid.UUID,
    max_emails_per_day: int,
) -> bool:
    sent = await count_emails_sent_today(db, candidate_id)
    return sent < max_emails_per_day


async def remaining_email_quota(
    db: AsyncSession,
    candidate_id: uuid.UUID,
    max_emails_per_day: int,
) -> int:
    sent = await count_emails_sent_today(db, candidate_id)
    return max(0, max_emails_per_day - sent)
