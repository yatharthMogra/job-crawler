from __future__ import annotations

import uuid
from datetime import datetime, timezone

import structlog
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.database import AsyncSessionLocal
from app.models.notification import NotificationBatch, NotificationJobHistory
from app.models.shared import Candidate
from app.models.subscription import UserPoolSubscription
from app.notification.ranker import deduplicate_ranked_jobs, rank_jobs
from app.notification.renderer import render_daily_briefing
from app.notification.retrieval import build_constraint_filters, fetch_new_jobs_in_pools
from app.notification.sender import send_email
from app.scoring.explainability import generate_explanations
from app.services.profile_loader import load_user_profile
from app.services.subscriptions import get_active_pools

log = structlog.get_logger(__name__)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


async def get_last_notification_time(db: AsyncSession, candidate_id: uuid.UUID) -> datetime | None:
    return await db.scalar(
        select(func.max(NotificationBatch.sent_at)).where(
            NotificationBatch.candidate_id == candidate_id,
            NotificationBatch.status == "sent",
        )
    )


async def run_notification_for_user(
    db: AsyncSession,
    candidate_id: uuid.UUID,
    settings: Settings | None = None,
) -> None:
    settings = settings or get_settings()
    batch = NotificationBatch(
        candidate_id=candidate_id,
        triggered_at=_utcnow(),
        status="pending",
    )
    db.add(batch)
    await db.flush()

    pools = await get_active_pools(db, candidate_id)
    if not pools:
        await _skip_batch(batch, "no_pool_subscriptions", db)
        return

    user_profile = await load_user_profile(db, candidate_id)
    if user_profile is None:
        await _skip_batch(batch, "missing_profile", db)
        return

    last_notified_at = await get_last_notification_time(db, candidate_id)
    constraint_filters = build_constraint_filters(user_profile)
    candidate_jobs = await fetch_new_jobs_in_pools(
        db,
        candidate_id=candidate_id,
        pools=pools,
        since=last_notified_at,
        limit=settings.notification_retrieval_limit,
        extra_filters=constraint_filters,
    )
    batch.jobs_in_pools = len(candidate_jobs)
    batch.jobs_new_since_last = len(candidate_jobs)
    await db.flush()

    if not candidate_jobs:
        await _skip_batch(batch, "no_new_jobs", db)
        return

    filtered_jobs = candidate_jobs
    batch.jobs_after_filter = len(filtered_jobs)
    await db.flush()

    if not filtered_jobs:
        await _skip_batch(batch, "no_jobs_after_filter", db)
        return

    ranked_jobs = deduplicate_ranked_jobs(rank_jobs(filtered_jobs, user_profile, settings))
    batch.jobs_ranked = len(ranked_jobs)
    top_jobs = ranked_jobs[: settings.notification_jobs_per_email]

    jobs_with_explanations: list[tuple] = []
    for job, score in top_jobs:
        explanations = generate_explanations(job, user_profile)
        jobs_with_explanations.append((job, explanations, score))

    html = render_daily_briefing(
        jobs_with_explanations=jobs_with_explanations,
        user_profile=user_profile,
        total_scanned=len(candidate_jobs),
        app_base_url=settings.app_base_url,
    )
    delivered = await send_email(
        to=user_profile.email,
        subject="Career Match AI - Daily Briefing",
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
            )
        )

    batch.sent_at = _utcnow()
    batch.status = "sent" if delivered else "failed"
    batch.jobs_sent = len(top_jobs)
    batch.email_delivered = delivered
    if not delivered:
        batch.skip_reason = "email_failed"
    await db.commit()


async def _skip_batch(batch: NotificationBatch, reason: str, db: AsyncSession) -> None:
    batch.status = "skipped"
    batch.skip_reason = reason
    await db.commit()


async def run_notification_pipeline(settings: Settings | None = None) -> None:
    settings = settings or get_settings()
    async with AsyncSessionLocal() as db:
        candidate_ids = (
            await db.scalars(
                select(UserPoolSubscription.candidate_id)
                .where(UserPoolSubscription.is_active.is_(True))
                .distinct()
            )
        ).all()

    for candidate_id in candidate_ids:
        try:
            async with AsyncSessionLocal() as db:
                candidate = await db.get(Candidate, candidate_id)
                if candidate is None:
                    continue
                await run_notification_for_user(db, candidate_id, settings)
        except Exception as exc:
            log.error("notification_pipeline_user_failed", candidate_id=str(candidate_id), error=str(exc))
