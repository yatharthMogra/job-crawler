from __future__ import annotations

import uuid
from datetime import datetime, timezone

import structlog
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.database import AsyncSessionLocal
from app.models.company_watch import CompanyWatchSubscription, NotificationJobEvent
from app.models.notification import NotificationBatch, NotificationJobHistory
from app.models.notification_preferences import NotificationPreferences
from app.models.shared import Company, NormalizedJob
from app.notification.filters import job_matches_location_constraints
from app.notification.renderer import render_company_watch
from app.notification.retrieval import build_constraint_filters
from app.notification.sender import send_email
from app.scoring.explainability import generate_explanations
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


async def _already_notified(
    db: AsyncSession,
    candidate_id: uuid.UUID,
    job_id: uuid.UUID,
) -> bool:
    existing = await db.scalar(
        select(func.count())
        .select_from(NotificationJobHistory)
        .where(
            NotificationJobHistory.candidate_id == candidate_id,
            NotificationJobHistory.job_id == job_id,
            NotificationJobHistory.channel == CHANNEL_COMPANY_WATCH,
        )
    )
    return bool(existing)


async def _notify_watcher(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    job: NormalizedJob,
    company_name: str,
    settings: Settings,
) -> None:
    if await _already_notified(db, candidate_id, job.id):
        return

    user_profile = await load_user_profile(db, candidate_id)
    if user_profile is None:
        return

    if not await job_passes_preference_filters(db, job, user_profile, settings):
        return

    explanations = generate_explanations(job, user_profile)
    html = render_company_watch(
        job=job,
        explanations=explanations,
        user_profile=user_profile,
        company_name=company_name,
        app_base_url=settings.app_base_url,
    )

    batch = NotificationBatch(
        candidate_id=candidate_id,
        triggered_at=_utcnow(),
        status="pending",
        channel=CHANNEL_COMPANY_WATCH,
        jobs_sent=1,
    )
    db.add(batch)
    await db.flush()

    delivered = await send_email(
        to=user_profile.email,
        subject=f"Career Match AI - New role at {company_name}",
        html=html,
        settings=settings,
    )

    db.add(
        NotificationJobHistory(
            candidate_id=candidate_id,
            batch_id=batch.id,
            job_id=job.id,
            rank_in_batch=1,
            recommendation_score=0.0,
            explanation=explanations,
            channel=CHANNEL_COMPANY_WATCH,
        )
    )
    batch.sent_at = _utcnow()
    batch.status = "sent" if delivered else "failed"
    batch.email_delivered = delivered
    if not delivered:
        batch.skip_reason = "email_failed"


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

    company = await db.get(Company, event.company_id)
    company_name = company.name if company else job.company_name

    watcher_ids = (
        await db.scalars(
            select(CompanyWatchSubscription.candidate_id)
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

    for candidate_id in watcher_ids:
        try:
            await _notify_watcher(
                db,
                candidate_id=candidate_id,
                job=job,
                company_name=company_name,
                settings=settings,
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
