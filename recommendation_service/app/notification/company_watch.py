from __future__ import annotations

import uuid
from datetime import datetime, timezone

import structlog
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.database import AsyncSessionLocal
from app.models.company_watch import CompanyWatchSubscription, NotificationJobEvent
from app.models.notification_preferences import NotificationPreferences
from app.models.shared import Company, NormalizedJob
from app.notification.company_watch_batch import schedule_company_watch_batch
from app.notification.company_watch_watermark import (
    get_company_watch_watermark,
    job_reference_at_after_watermark,
)
from app.notification.filters import job_matches_location_constraints
from app.notification.retrieval import build_constraint_filters
from app.services.profile_loader import load_user_profile

log = structlog.get_logger(__name__)

CHANNEL_COMPANY_WATCH = "company_watch"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


async def job_passes_preference_filters(
    db: AsyncSession,
    job: NormalizedJob,
    user_profile,
    settings: Settings,
) -> bool:
    filters = build_constraint_filters(user_profile, settings)
    if not filters:
        return True

    stmt = select(func.count()).select_from(NormalizedJob).where(
        and_(NormalizedJob.id == job.id, *filters)
    )
    count = await db.scalar(stmt) or 0
    if count == 0:
        return False

    return job_matches_location_constraints(job, user_profile)


async def _handle_watcher(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    job: NormalizedJob,
    company_id: uuid.UUID,
    settings: Settings,
    prefs: NotificationPreferences,
) -> None:
    user_profile = await load_user_profile(db, candidate_id)
    if user_profile is None:
        return

    if not await job_passes_preference_filters(db, job, user_profile, settings):
        return

    watermark = await get_company_watch_watermark(
        db,
        candidate_id=candidate_id,
        company_id=company_id,
        prefs=prefs,
    )
    if not job_reference_at_after_watermark(job, watermark):
        return

    await schedule_company_watch_batch(
        db,
        candidate_id=candidate_id,
        job_id=job.id,
        company_id=company_id,
        prefs=prefs,
    )


async def process_company_watch_event(
    db: AsyncSession,
    event: NotificationJobEvent,
    settings: Settings | None = None,
) -> None:
    settings = settings or get_settings()
    job = await db.get(NormalizedJob, event.job_id)
    if job is None or not job.is_active or job.processing_state != "success":
        event.processed_at = _utcnow()
        return

    watcher_rows = (
        await db.execute(
            select(CompanyWatchSubscription.candidate_id, NotificationPreferences)
            .join(
                NotificationPreferences,
                NotificationPreferences.candidate_id == CompanyWatchSubscription.candidate_id,
            )
            .where(
                CompanyWatchSubscription.company_id == event.company_id,
                CompanyWatchSubscription.is_active.is_(True),
                NotificationPreferences.company_watch_enabled.is_(True),
            )
            .distinct()
        )
    ).all()

    for candidate_id, prefs in watcher_rows:
        try:
            await _handle_watcher(
                db,
                candidate_id=candidate_id,
                job=job,
                company_id=event.company_id,
                settings=settings,
                prefs=prefs,
            )
        except Exception as exc:
            log.error(
                "company_watch_notify_failed",
                candidate_id=str(candidate_id),
                job_id=str(job.id),
                error=str(exc),
            )

    event.processed_at = _utcnow()
    await db.commit()


async def run_company_watch_processor(settings: Settings | None = None) -> None:
    settings = settings or get_settings()
    async with AsyncSessionLocal() as db:
        events = (
            await db.scalars(
                select(NotificationJobEvent)
                .where(NotificationJobEvent.processed_at.is_(None))
                .order_by(NotificationJobEvent.enqueued_at.asc())
                .limit(settings.company_watch_batch_size)
            )
        ).all()

    for event in events:
        try:
            async with AsyncSessionLocal() as db:
                fresh = await db.get(NotificationJobEvent, event.id)
                if fresh is None or fresh.processed_at is not None:
                    continue
                await process_company_watch_event(db, fresh, settings)
        except Exception as exc:
            log.error("company_watch_event_failed", event_id=str(event.id), error=str(exc))
            async with AsyncSessionLocal() as db:
                fresh = await db.get(NotificationJobEvent, event.id)
                if fresh is not None:
                    fresh.processed_at = _utcnow()
                    fresh.error = str(exc)[:512]
                    await db.commit()
