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
from app.notification.company_watch_eligibility import job_passes_company_watch_eligibility
from app.notification.company_watch_watermark import (
    get_company_watch_watermark,
    job_reference_at_after_watermark,
)
from app.notification.ranker import _rank_sort_key
from app.notification.renderer import render_company_watch_batch
from app.notification.sender import send_email
from app.notification.spam_limiter import can_send_email
from app.scoring.explainability import generate_explanations
from app.scoring.recommendation import score_job
from app.services.profile_loader import load_user_profile
from app.services.subscriptions import get_active_pools

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


def select_company_watch_jobs(
    scored: list[tuple[NormalizedJob, float]],
    *,
    min_score: float,
    max_jobs: int,
) -> list[tuple[NormalizedJob, float]]:
    qualifying = [(job, score) for job, score in scored if score >= min_score]
    qualifying.sort(key=_rank_sort_key, reverse=True)
    return qualifying[:max_jobs]


async def schedule_company_watch_batch(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    job_id: uuid.UUID,
    company_id: uuid.UUID,
    prefs: NotificationPreferences,
) -> None:
    if await _already_notified(db, candidate_id, job_id):
        return

    job = await db.get(NormalizedJob, job_id)
    if job is None or not job.is_active or job.processing_state != "success":
        return

    watermark = await get_company_watch_watermark(
        db,
        candidate_id=candidate_id,
        company_id=company_id,
        prefs=prefs,
    )
    if not job_reference_at_after_watermark(job, watermark):
        return

    pending = await db.scalar(
        select(CompanyWatchPendingAlert.id).where(
            CompanyWatchPendingAlert.candidate_id == candidate_id,
            CompanyWatchPendingAlert.job_id == job_id,
            CompanyWatchPendingAlert.included_in_batch_id.is_(None),
        )
    )
    if pending is not None:
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


async def _advance_schedule_without_send(
    prefs: NotificationPreferences,
    *,
    now: datetime,
) -> None:
    prefs.next_company_watch_due_at = compute_next_company_watch_due_at(
        last_batch_at=prefs.last_company_watch_batch_at,
        cadence_minutes=prefs.company_watch_cadence_minutes,
        now=now,
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

    pools = await get_active_pools(db, candidate_id)
    dropped_row_ids: list[uuid.UUID] = []
    eligible_for_scoring: list[tuple[CompanyWatchPendingAlert, NormalizedJob, str]] = []

    for row in pending_rows:
        job = await db.get(NormalizedJob, row.job_id)
        if job is None or not job.is_active or job.processing_state != "success":
            dropped_row_ids.append(row.id)
            continue

        watermark = await get_company_watch_watermark(
            db,
            candidate_id=candidate_id,
            company_id=row.company_id,
            prefs=prefs,
        )
        if not job_reference_at_after_watermark(job, watermark):
            dropped_row_ids.append(row.id)
            continue

        if not pools or not await job_passes_company_watch_eligibility(
            db, job, user_profile, settings, pools=pools
        ):
            dropped_row_ids.append(row.id)
            continue

        company = await db.get(Company, row.company_id)
        company_name = company.name if company else job.company_name
        eligible_for_scoring.append((row, job, company_name))

    scored: list[tuple[CompanyWatchPendingAlert, NormalizedJob, str, float]] = []
    for row, job, company_name in eligible_for_scoring:
        personal_score = score_job(job, user_profile, settings)
        if personal_score < settings.company_watch_min_score:
            dropped_row_ids.append(row.id)
            continue
        scored.append((row, job, company_name, personal_score))

    for row_id in dropped_row_ids:
        row = await db.get(CompanyWatchPendingAlert, row_id)
        if row is not None:
            await db.delete(row)

    if not scored:
        now = _utcnow()
        log.info(
            "company_watch_batch_skipped_below_threshold",
            candidate_id=str(candidate_id),
            min_score=settings.company_watch_min_score,
        )
        await _advance_schedule_without_send(prefs, now=now)
        return

    scored.sort(key=lambda item: _rank_sort_key((item[1], item[3])), reverse=True)
    max_jobs = settings.company_watch_max_jobs_per_email
    selected = scored[:max_jobs]
    overflow = scored[max_jobs:]

    for row, _, _, _ in overflow:
        await db.delete(row)

    if overflow:
        log.info(
            "company_watch_batch_dropped_overflow",
            candidate_id=str(candidate_id),
            dropped=len(overflow),
            cap=max_jobs,
        )

    jobs_with_meta: list[tuple[NormalizedJob, list[str], str, float]] = []
    included_row_ids: list[uuid.UUID] = []

    for row, job, company_name, personal_score in selected:
        explanations = generate_explanations(job, user_profile)
        jobs_with_meta.append((job, explanations, company_name, personal_score))
        included_row_ids.append(row.id)

    now = _utcnow()
    html = render_company_watch_batch(
        jobs_with_explanations=[(job, explanations, company_name) for job, explanations, company_name, _ in jobs_with_meta],
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

    for rank, (job, explanations, _company_name, personal_score) in enumerate(jobs_with_meta, start=1):
        db.add(
            NotificationJobHistory(
                candidate_id=candidate_id,
                batch_id=batch.id,
                job_id=job.id,
                rank_in_batch=rank,
                recommendation_score=personal_score,
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
