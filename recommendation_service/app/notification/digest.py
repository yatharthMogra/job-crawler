from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.database import AsyncSessionLocal
from app.models.notification_preferences import NotificationPreferences
from app.models.shared import Candidate
from app.notification.ranker import deduplicate_ranked_jobs, rank_jobs_with_h1b, select_top_jobs
from app.notification.renderer import render_personalized_digest
from app.notification.retrieval import build_constraint_filters, fetch_new_jobs_in_pools
from app.notification.filters import build_digest_filters
from app.notification.sender import send_email
from app.notification.spam_limiter import can_send_email
from app.models.notification import NotificationBatch, NotificationJobHistory
from app.scoring.explainability import generate_explanations
from app.services.profile_loader import load_user_profile
from app.services.entitlements import (
    default_company_watch_cadence_minutes,
    default_max_emails_per_day,
    get_plan_tier,
)
from app.services.subscriptions import get_active_pools

log = structlog.get_logger(__name__)

CHANNEL_DIGEST = "digest"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def clamp_cadence_hours(hours: int, *, minimum: int = 3, maximum: int = 168) -> int:
    return max(minimum, min(maximum, hours))


def clamp_top_k(top_k: int, *, minimum: int = 1, maximum: int = 20) -> int:
    return max(minimum, min(maximum, top_k))


def compute_next_digest_due_at(
    *,
    last_sent_at: datetime | None,
    cadence_hours: int,
    now: datetime | None = None,
) -> datetime:
    now = now or _utcnow()
    if last_sent_at is None:
        return now
    return last_sent_at + timedelta(hours=cadence_hours)


async def get_or_create_preferences(
    db: AsyncSession,
    candidate_id: uuid.UUID,
    settings: Settings | None = None,
) -> NotificationPreferences:
    settings = settings or get_settings()
    prefs = await db.get(NotificationPreferences, candidate_id)
    if prefs is not None:
        return prefs

    plan_tier = await get_plan_tier(db, candidate_id)
    prefs = NotificationPreferences(
        candidate_id=candidate_id,
        digest_enabled=True,
        company_watch_enabled=False,
        cadence_hours=settings.default_digest_cadence_hours,
        top_k=settings.default_digest_top_k,
        company_watch_cadence_minutes=default_company_watch_cadence_minutes(plan_tier),
        max_emails_per_day=default_max_emails_per_day(plan_tier),
        next_digest_due_at=_utcnow(),
    )
    db.add(prefs)
    await db.flush()
    return prefs


def should_send_digest(ranked_job_count: int, settings: Settings) -> bool:
    minimum = settings.notification_min_jobs_to_send
    if minimum <= 0:
        return ranked_job_count > 0
    return ranked_job_count >= minimum


def should_send_notification(ranked_job_count: int, settings: Settings) -> bool:
    """Backwards-compatible alias."""
    return should_send_digest(ranked_job_count, settings)


def digest_window_start(
    prefs: NotificationPreferences,
    now: datetime | None = None,
) -> datetime:
    now = now or _utcnow()
    if prefs.last_digest_sent_at is not None:
        return prefs.last_digest_sent_at
    return now - timedelta(hours=prefs.cadence_hours)


async def run_digest_for_user(
    db: AsyncSession,
    candidate_id: uuid.UUID,
    settings: Settings | None = None,
) -> None:
    settings = settings or get_settings()
    prefs = await get_or_create_preferences(db, candidate_id, settings)

    batch = NotificationBatch(
        candidate_id=candidate_id,
        triggered_at=_utcnow(),
        status="pending",
        channel=CHANNEL_DIGEST,
    )
    db.add(batch)
    await db.flush()

    if not prefs.digest_enabled:
        await _skip_batch(batch, "digest_disabled", db)
        return

    pools = await get_active_pools(db, candidate_id)
    if not pools:
        await _skip_batch(batch, "no_pool_subscriptions", db)
        return

    user_profile = await load_user_profile(db, candidate_id)
    if user_profile is None:
        await _skip_batch(batch, "missing_profile", db)
        return

    since = digest_window_start(prefs)
    constraint_filters = build_constraint_filters(user_profile, settings)
    digest_filters = build_digest_filters(prefs.digest_filters, user_profile)
    extra_filters = constraint_filters + digest_filters

    candidate_jobs = await fetch_new_jobs_in_pools(
        db,
        candidate_id=candidate_id,
        pools=pools,
        since=since,
        limit=settings.notification_retrieval_limit,
        extra_filters=extra_filters,
        settings=settings,
        channel=CHANNEL_DIGEST,
    )
    batch.jobs_in_pools = len(candidate_jobs)
    batch.jobs_new_since_last = len(candidate_jobs)
    await db.flush()

    if not candidate_jobs:
        await _skip_batch(batch, "no_new_jobs", db)
        return

    batch.jobs_after_filter = len(candidate_jobs)
    ranked_jobs = deduplicate_ranked_jobs(
        await rank_jobs_with_h1b(db, candidate_jobs, user_profile, settings)
    )
    batch.jobs_ranked = len(ranked_jobs)

    if not should_send_digest(len(ranked_jobs), settings):
        await _skip_batch(batch, "insufficient_eligible_jobs", db)
        return

    top_jobs = select_top_jobs(
        ranked_jobs,
        prefs.top_k,
        max_per_company=settings.notification_max_jobs_per_company,
    )

    jobs_with_explanations: list[tuple] = []
    for job, score in top_jobs:
        explanations = generate_explanations(job, user_profile)
        jobs_with_explanations.append((job, explanations, score))

    if not await can_send_email(db, candidate_id, prefs.max_emails_per_day):
        await _skip_batch(batch, "daily_cap_reached", db)
        return

    html = render_personalized_digest(
        jobs_with_explanations=jobs_with_explanations,
        user_profile=user_profile,
        total_scanned=len(candidate_jobs),
        app_base_url=settings.app_base_url,
    )
    delivered = await send_email(
        to=user_profile.email,
        subject="Career Match AI - Personalized Digest",
        html=html,
        settings=settings,
    )

    for rank, (job, explanations, score) in enumerate(jobs_with_explanations, start=1):
        db.add(
            NotificationJobHistory(
                candidate_id=candidate_id,
                batch_id=batch.id,
                job_id=job.id,
                rank_in_batch=rank,
                recommendation_score=score,
                explanation=explanations,
                channel=CHANNEL_DIGEST,
            )
        )

    now = _utcnow()
    batch.sent_at = now
    batch.status = "sent" if delivered else "failed"
    batch.jobs_sent = len(top_jobs)
    batch.email_delivered = delivered
    if not delivered:
        batch.skip_reason = "email_failed"
    else:
        prefs.last_digest_sent_at = now
        prefs.next_digest_due_at = compute_next_digest_due_at(
            last_sent_at=now,
            cadence_hours=prefs.cadence_hours,
            now=now,
        )
    await db.commit()


async def _skip_batch(batch: NotificationBatch, reason: str, db: AsyncSession) -> None:
    batch.status = "skipped"
    batch.skip_reason = reason
    await db.commit()


async def run_digest_scheduler(settings: Settings | None = None) -> None:
    settings = settings or get_settings()
    now = _utcnow()
    async with AsyncSessionLocal() as db:
        candidate_ids = (
            await db.scalars(
                select(NotificationPreferences.candidate_id).where(
                    NotificationPreferences.digest_enabled.is_(True),
                    NotificationPreferences.next_digest_due_at.is_not(None),
                    NotificationPreferences.next_digest_due_at <= now,
                )
            )
        ).all()

    for candidate_id in candidate_ids:
        try:
            async with AsyncSessionLocal() as db:
                candidate = await db.get(Candidate, candidate_id)
                if candidate is None:
                    continue
                await run_digest_for_user(db, candidate_id, settings)
        except Exception as exc:
            log.error(
                "digest_scheduler_user_failed",
                candidate_id=str(candidate_id),
                error=str(exc),
            )
