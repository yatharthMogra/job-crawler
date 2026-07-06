from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.database import AsyncSessionLocal
from app.models.company_watch_pending import CompanyWatchPendingAlert
from app.models.notification import NotificationBatch, NotificationJobHistory
from app.models.notification_preferences import NotificationPreferences
from app.models.shared import Company, NormalizedJob
from app.notification.renderer import render_company_watch_batch
from app.notification.sender import send_email
from app.notification.spam_limiter import can_send_email
from app.scoring.explainability import generate_explanations
from app.services.entitlements import get_plan_tier, get_tier_limits
from app.services.profile_loader import load_user_profile

log = structlog.get_logger(__name__)

CHANNEL_COMPANY_WATCH = "company_watch"


async def _already_notified(
    db: AsyncSession,
    candidate_id: uuid.UUID,
    job_id: uuid.UUID,
) -> bool:
    from sqlalchemy import func

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


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def compute_next_company_watch_due_at(
    *,
    last_batch_at: datetime | None,
    cadence_minutes: int,
    now: datetime | None = None,
) -> datetime:
    now = now or _utcnow()
    if last_batch_at is None:
        return now + timedelta(minutes=cadence_minutes)
    return last_batch_at + timedelta(minutes=cadence_minutes)


async def schedule_company_watch_batch(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    job_id: uuid.UUID,
    company_id: uuid.UUID,
    prefs: NotificationPreferences,
) -> None:
    pending = await db.scalar(
        select(CompanyWatchPendingAlert.id).where(
            CompanyWatchPendingAlert.candidate_id == candidate_id,
            CompanyWatchPendingAlert.job_id == job_id,
            CompanyWatchPendingAlert.included_in_batch_id.is_(None),
        )
    )
    if pending is not None:
        return

    if await _already_notified(db, candidate_id, job_id):
        return

    db.add(
        CompanyWatchPendingAlert(
            candidate_id=candidate_id,
            job_id=job_id,
            company_id=company_id,
        )
    )

    if prefs.next_company_watch_due_at is None:
        prefs.next_company_watch_due_at = compute_next_company_watch_due_at(
            last_batch_at=prefs.last_company_watch_batch_at,
            cadence_minutes=prefs.company_watch_cadence_minutes,
            now=_utcnow(),
        )


async def _send_batch_for_candidate(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    prefs: NotificationPreferences,
    settings: Settings,
) -> None:
    pending_rows = (
        await db.scalars(
            select(CompanyWatchPendingAlert)
            .where(
                CompanyWatchPendingAlert.candidate_id == candidate_id,
                CompanyWatchPendingAlert.included_in_batch_id.is_(None),
            )
            .order_by(CompanyWatchPendingAlert.enqueued_at.asc())
        )
    ).all()

    if not pending_rows:
        return

    if not await can_send_email(db, candidate_id, prefs.max_emails_per_day):
        log.info("company_watch_batch_deferred_daily_cap", candidate_id=str(candidate_id))
        return

    user_profile = await load_user_profile(db, candidate_id)
    if user_profile is None:
        return

    jobs_with_meta: list[tuple[NormalizedJob, list[str], str]] = []
    included_row_ids: list[uuid.UUID] = []
    stale_row_ids: list[uuid.UUID] = []

    for row in pending_rows:
        job = await db.get(NormalizedJob, row.job_id)
        if job is None or not job.is_active or job.processing_state != "success":
            stale_row_ids.append(row.id)
            continue
        company = await db.get(Company, row.company_id)
        company_name = company.name if company else job.company_name
        explanations = generate_explanations(job, user_profile)
        jobs_with_meta.append((job, explanations, company_name))
        included_row_ids.append(row.id)

    now = _utcnow()
    for row_id in stale_row_ids:
        row = await db.get(CompanyWatchPendingAlert, row_id)
        if row is not None:
            await db.delete(row)

    if not jobs_with_meta:
        prefs.last_company_watch_batch_at = now
        prefs.next_company_watch_due_at = compute_next_company_watch_due_at(
            last_batch_at=now,
            cadence_minutes=prefs.company_watch_cadence_minutes,
            now=now,
        )
        return

    html = render_company_watch_batch(
        jobs_with_explanations=jobs_with_meta,
        user_profile=user_profile,
        app_base_url=settings.app_base_url,
    )
    job_count = len(jobs_with_meta)
    subject = (
        f"Career Match AI - {job_count} new role{'s' if job_count != 1 else ''} "
        "from companies you're watching"
    )

    batch = NotificationBatch(
        candidate_id=candidate_id,
        triggered_at=now,
        status="pending",
        channel=CHANNEL_COMPANY_WATCH,
        jobs_sent=job_count,
    )
    db.add(batch)
    await db.flush()

    delivered = await send_email(
        to=user_profile.email,
        subject=subject,
        html=html,
        settings=settings,
    )

    for rank, (job, explanations, _company_name) in enumerate(jobs_with_meta, start=1):
        db.add(
            NotificationJobHistory(
                candidate_id=candidate_id,
                batch_id=batch.id,
                job_id=job.id,
                rank_in_batch=rank,
                recommendation_score=0.0,
                explanation=explanations,
                channel=CHANNEL_COMPANY_WATCH,
            )
        )

    for row_id in included_row_ids:
        row = await db.get(CompanyWatchPendingAlert, row_id)
        if row is not None:
            row.included_in_batch_id = batch.id

    batch.sent_at = now
    batch.status = "sent" if delivered else "failed"
    batch.email_delivered = delivered
    if not delivered:
        batch.skip_reason = "email_failed"

    prefs.last_company_watch_batch_at = now
    prefs.next_company_watch_due_at = compute_next_company_watch_due_at(
        last_batch_at=now,
        cadence_minutes=prefs.company_watch_cadence_minutes,
        now=now,
    )


async def run_company_watch_batch_processor(settings: Settings | None = None) -> None:
    settings = settings or get_settings()
    now = _utcnow()

    async with AsyncSessionLocal() as db:
        due_prefs = (
            await db.scalars(
                select(NotificationPreferences).where(
                    NotificationPreferences.company_watch_enabled.is_(True),
                    NotificationPreferences.next_company_watch_due_at.is_not(None),
                    NotificationPreferences.next_company_watch_due_at <= now,
                )
            )
        ).all()

    for prefs in due_prefs:
        try:
            async with AsyncSessionLocal() as db:
                plan_tier = await get_plan_tier(db, prefs.candidate_id)
                limits = get_tier_limits(plan_tier)
                if limits.delivery != "batched":
                    continue

                fresh_prefs = await db.get(NotificationPreferences, prefs.candidate_id)
                if fresh_prefs is None or not fresh_prefs.company_watch_enabled:
                    continue
                if fresh_prefs.next_company_watch_due_at is None or fresh_prefs.next_company_watch_due_at > now:
                    continue

                has_pending = await db.scalar(
                    select(CompanyWatchPendingAlert.id)
                    .where(
                        CompanyWatchPendingAlert.candidate_id == prefs.candidate_id,
                        CompanyWatchPendingAlert.included_in_batch_id.is_(None),
                    )
                    .limit(1)
                )
                if has_pending is None:
                    fresh_prefs.next_company_watch_due_at = compute_next_company_watch_due_at(
                        last_batch_at=fresh_prefs.last_company_watch_batch_at,
                        cadence_minutes=fresh_prefs.company_watch_cadence_minutes,
                        now=now,
                    )
                    await db.commit()
                    continue

                await _send_batch_for_candidate(
                    db,
                    candidate_id=prefs.candidate_id,
                    prefs=fresh_prefs,
                    settings=settings,
                )
                await db.commit()
        except Exception as exc:
            log.error(
                "company_watch_batch_failed",
                candidate_id=str(prefs.candidate_id),
                error=str(exc),
            )
