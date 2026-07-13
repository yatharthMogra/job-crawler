from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
import logging
from typing import Any, Literal, Optional
from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

try:
    import structlog
except ImportError:  # pragma: no cover - dependency fallback path
    structlog = None

from app.config import Settings, get_settings, PLATFORM_FAILURE_ALERT_THRESHOLDS
from app.database import AsyncSessionLocal
from app.ingestion.fetch_backpressure import apply_fetch_backpressure, backpressure_metadata
from app.ingestion.fetch_schedule import select_due_companies
from app.ingestion.fetch_schedule_config import FetchScheduleConfig
from app.exceptions import IngestionError
from app.ingestion.alerts import write_failure_alert
from app.ingestion.change_detector import classify_jobs
from app.ingestion.dedup import build_dedup_fingerprint, fingerprint_exists
from app.ingestion.constants import (
    EventCategory,
    EventSeverity,
    EventType,
    FailureReason,
    ProcessingState,
)
from app.ingestion.enrichment_worker import queue_job_for_enrichment
from app.ingestion.events import write_event
from app.ingestion.extractor.deterministic import extract_deterministic_fields
from app.ingestion.extractor.llm import DEFAULT_ENRICHMENT
from app.ingestion.extractor.text_cleaner import build_description_preview, clean_job_description
from app.ingestion.fetcher import fetch_company_jobs
from app.ingestion.job_freshness import FreshnessVerdict, classify_posted_at
from app.ingestion.job_field_limits import clamp_deterministic_fields
from app.ingestion.job_timestamp import resolve_reference_at
from app.ingestion.job_archive_sync import (
    upsert_job_archive_from_deterministic,
    upsert_job_archive_from_normalized,
)
from app.ingestion.job_content_hash import compute_job_content_hash
from app.ingestion.job_identity_ledger import (
    load_ledger_first_seen_map,
    load_ledger_hashes,
    upsert_ledger_entry,
)
from app.models.company import Company
from app.models.normalized_job import NormalizedJob
from app.models.pipeline_run import CompanyRunResult, PipelineRun
from app.models.raw_job import RawJob

logger = structlog.get_logger(__name__) if structlog else logging.getLogger(__name__)
TerminalRunStatus = Literal["completed", "partial_success", "failed"]


@dataclass
class CompanyStats:
    jobs_fetched: int = 0
    jobs_new: int = 0
    jobs_updated: int = 0
    jobs_unchanged: int = 0
    jobs_removed: int = 0
    jobs_rejected_stale_fetch: int = 0
    jobs_rejected_stale_pipeline: int = 0


@dataclass
class PipelineSnapshot:
    run_id: str
    status: TerminalRunStatus
    total_companies: int
    successful_companies: int
    failed_companies: int
    jobs_fetched: int
    jobs_new: int
    jobs_updated: int
    jobs_unchanged: int
    jobs_removed: int


@dataclass
class CompanyRunOutcome:
    company_id: UUID
    status: Literal["success", "failed"]
    jobs_fetched: int = 0
    jobs_new: int = 0
    jobs_updated: int = 0
    jobs_unchanged: int = 0
    jobs_removed: int = 0
    jobs_deduped: int = 0
    jobs_ledger_skipped: int = 0
    jobs_ledger_baselined: int = 0
    jobs_rejected_stale_fetch: int = 0
    jobs_rejected_stale_pipeline: int = 0
    error_message: Optional[str] = None


async def _latest_hashes_for_company(db: AsyncSession, company_id: Any) -> dict[str, str]:
    stmt: Select[tuple[RawJob]] = (
        select(RawJob)
        .where(RawJob.company_id == company_id)
        .order_by(RawJob.external_job_id.asc(), RawJob.fetch_timestamp.desc())
    )
    rows = (await db.scalars(stmt)).all()
    latest: dict[str, str] = {}
    for row in rows:
        latest.setdefault(row.external_job_id, row.content_hash)
    return latest


async def _latest_raw_by_external_id(
    db: AsyncSession, company_id: Any
) -> dict[str, dict[str, Any]]:
    stmt: Select[tuple[RawJob]] = (
        select(RawJob)
        .where(RawJob.company_id == company_id)
        .order_by(RawJob.external_job_id.asc(), RawJob.fetch_timestamp.desc())
    )
    rows = (await db.scalars(stmt)).all()
    latest: dict[str, dict[str, Any]] = {}
    for row in rows:
        if row.external_job_id not in latest and isinstance(row.raw_api_response, dict):
            latest[row.external_job_id] = row.raw_api_response
    return latest


async def _latest_raw_fetch_times(
    db: AsyncSession, company_id: Any
) -> dict[str, datetime]:
    stmt: Select[tuple[RawJob]] = (
        select(RawJob)
        .where(RawJob.company_id == company_id)
        .order_by(RawJob.external_job_id.asc(), RawJob.fetch_timestamp.desc())
    )
    rows = (await db.scalars(stmt)).all()
    latest: dict[str, datetime] = {}
    for row in rows:
        latest.setdefault(row.external_job_id, row.fetch_timestamp)
    return latest


async def _normalized_map_for_company(db: AsyncSession, company_id: Any) -> dict[str, NormalizedJob]:
    stmt = select(NormalizedJob).where(NormalizedJob.company_id == company_id)
    jobs = (await db.scalars(stmt)).all()
    return {row.external_job_id: row for row in jobs}


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _is_baseline_run(
    ledger_hashes: dict[str, str],
    raw_hashes: dict[str, str],
    normalized_by_external_id: dict[str, NormalizedJob],
) -> bool:
    return not ledger_hashes and not raw_hashes and not normalized_by_external_id


def _resolve_terminal_status(successful_companies: int, failed_companies: int) -> TerminalRunStatus:
    if failed_companies == 0:
        return "completed"
    if successful_companies > 0:
        return "partial_success"
    return "failed"


async def _apply_removals(
    normalized_by_external_id: dict[str, NormalizedJob],
    removed_ids: list[str],
    threshold: int,
) -> int:
    removed_count = 0
    for external_id in removed_ids:
        normalized = normalized_by_external_id.get(external_id)
        if not normalized:
            continue
        normalized.consecutive_misses += 1
        if normalized.consecutive_misses >= threshold and normalized.is_active:
            normalized.is_active = False
            removed_count += 1
    return removed_count


async def _upsert_normalized_job(
    db: AsyncSession,
    company: Company,
    raw_row: RawJob,
    deterministic_fields: dict[str, Any],
    enrichment: Any,
    settings: Settings,
    existing_row: Optional[NormalizedJob],
    job_archive_id: Optional[UUID] = None,
    *,
    ledger_first_seen_at: Optional[datetime] = None,
) -> None:
    now = _utcnow()
    company_name = deterministic_fields.get("company_name") or company.name
    posted_at = deterministic_fields.get("posted_at")
    if existing_row is None:
        if posted_at is not None:
            reference_at = resolve_reference_at(posted_at, raw_row.fetch_timestamp)
        elif ledger_first_seen_at is not None:
            reference_at = ledger_first_seen_at
        else:
            reference_at = resolve_reference_at(None, raw_row.fetch_timestamp)
    elif posted_at is not None:
        reference_at = resolve_reference_at(posted_at, raw_row.fetch_timestamp)
    else:
        reference_at = existing_row.reference_at

    payload = dict(
        raw_job_id=raw_row.id,
        company_id=company.id,
        job_archive_id=job_archive_id,
        external_job_id=deterministic_fields["external_job_id"],
        title=deterministic_fields["title"] or "Untitled",
        company_name=company_name,
        location=deterministic_fields["location"],
        job_country=deterministic_fields.get("job_country"),
        department=deterministic_fields["department"],
        employment_type=deterministic_fields["employment_type"],
        posting_url=deterministic_fields["posting_url"],
        description_text=deterministic_fields.get("description_text"),
        description_preview=deterministic_fields.get("description_preview"),
        posted_at=posted_at,
        reference_at=reference_at,
        is_active=True,
        consecutive_misses=0,
        last_seen_at=now,
        seniority=enrichment.seniority,
        is_internship=enrichment.is_internship,
        is_new_grad=enrichment.is_new_grad,
        sponsorship_status=enrichment.sponsorship_status,
        sponsorship_confidence=enrichment.sponsorship_confidence,
        remote_type=enrichment.remote_type,
        tech_stack=enrichment.tech_stack,
        skills=enrichment.skills,
        llm_provider=settings.llm_provider,
        llm_model=settings.gemini_model if settings.llm_provider == "gemini" else None,
        extraction_version=settings.extraction_version,
        extracted_at=now,
        dedup_fingerprint=deterministic_fields.get("dedup_fingerprint"),
    )

    if existing_row is None:
        db.add(NormalizedJob(**payload))
        return

    for key, value in payload.items():
        setattr(existing_row, key, value)


def _resolve_description_text(job: dict[str, Any], raw_html: str) -> Optional[str]:
    description_candidates = [
        raw_html,
        job.get("content"),
        job.get("descriptionHtml"),
        job.get("description"),
        job.get("descriptionPlain"),
    ]
    for candidate in description_candidates:
        cleaned = clean_job_description(candidate)
        if cleaned:
            return cleaned
    return None


async def _upsert_normalized_core(
    db: AsyncSession,
    company: Company,
    raw_row: RawJob,
    deterministic_fields: dict[str, Any],
    settings: Settings,
    existing_row: Optional[NormalizedJob],
    job_archive_id: UUID,
    *,
    ledger_first_seen_at: Optional[datetime] = None,
) -> NormalizedJob:
    await _upsert_normalized_job(
        db=db,
        company=company,
        raw_row=raw_row,
        deterministic_fields=deterministic_fields,
        enrichment=DEFAULT_ENRICHMENT,
        settings=settings,
        existing_row=existing_row,
        job_archive_id=job_archive_id,
        ledger_first_seen_at=ledger_first_seen_at,
    )
    normalized = existing_row
    if normalized is None:
        normalized = await db.scalar(
            select(NormalizedJob).where(
                NormalizedJob.company_id == company.id,
                NormalizedJob.external_job_id == deterministic_fields["external_job_id"],
            )
        )
    if normalized is None:
        raise RuntimeError("Normalized job upsert failed unexpectedly.")
    normalized.processing_state = ProcessingState.PENDING
    normalized.failure_reason = None
    normalized.last_failure_at = None
    return normalized


async def process_company_raw_jobs(
    db: AsyncSession,
    company: Company,
    raw_jobs: list[dict[str, Any]],
    *,
    pipeline_run_id: UUID,
    settings: Settings,
    enrichment_source: str = "pipeline",
) -> CompanyRunOutcome:
    outcome = CompanyRunOutcome(company_id=company.id, status="success")
    outcome.jobs_fetched = len(raw_jobs)
    ledger_hashes = await load_ledger_hashes(db, company.id)
    ledger_first_seen = await load_ledger_first_seen_map(db, company.id)
    raw_hashes = await _latest_hashes_for_company(db, company.id)
    previous_hashes = {**raw_hashes, **ledger_hashes}
    normalized_by_external_id = await _normalized_map_for_company(db, company.id)
    is_baseline = _is_baseline_run(ledger_hashes, raw_hashes, normalized_by_external_id)
    active_ids = {job_id for job_id, row in normalized_by_external_id.items() if row.is_active}
    classified = classify_jobs(
        raw_jobs,
        previous_hashes,
        active_ids,
        platform=company.platform,
    )
    outcome.jobs_new = len(classified.new)
    outcome.jobs_updated = len(classified.updated)
    outcome.jobs_unchanged = len(classified.unchanged)

    new_external_ids = {str(job.get("id")) for job in classified.new}
    updated_external_ids = {str(job.get("id")) for job in classified.updated}
    changed_jobs = classified.new + classified.updated
    now = _utcnow()
    for job in changed_jobs:
        content_hash = compute_job_content_hash(job, company.platform)
        deterministic_fields = extract_deterministic_fields(job, platform=company.platform)
        external_id = deterministic_fields["external_job_id"]
        freshness = classify_posted_at(deterministic_fields.get("posted_at"), settings=settings)
        if is_baseline and freshness != FreshnessVerdict.FRESH:
            await upsert_ledger_entry(
                db,
                company.id,
                external_id,
                content_hash,
                seen_at=now,
            )
            ledger_hashes[external_id] = content_hash
            outcome.jobs_ledger_baselined += 1
            if external_id in new_external_ids:
                outcome.jobs_new -= 1
            else:
                outcome.jobs_updated -= 1
            if structlog:
                logger.info(
                    "job_ledger_baselined",
                    company_id=str(company.id),
                    external_job_id=external_id,
                    freshness=freshness.value,
                )
            continue
        if freshness == FreshnessVerdict.STALE:
            outcome.jobs_rejected_stale_pipeline += 1
            continue
        company_name = deterministic_fields.get("company_name") or company.name
        deterministic_fields["company_name"] = company_name
        deterministic_fields["dedup_fingerprint"] = build_dedup_fingerprint(
            company_name,
            deterministic_fields.get("title") or "",
            deterministic_fields.get("location"),
        )
        external_id = deterministic_fields["external_job_id"]
        if await fingerprint_exists(
            db,
            deterministic_fields["dedup_fingerprint"],
            company_id=company.id,
            external_job_id=external_id,
        ):
            outcome.jobs_deduped += 1
            if external_id in new_external_ids:
                outcome.jobs_new -= 1
            elif external_id in updated_external_ids:
                outcome.jobs_updated -= 1
            if structlog:
                logger.info(
                    "job_dedup_skipped",
                    company_id=str(company.id),
                    external_job_id=external_id,
                    fingerprint=deterministic_fields["dedup_fingerprint"],
                )
            continue
        deterministic_fields = clamp_deterministic_fields(deterministic_fields)
        external_id = deterministic_fields["external_job_id"]
        ledger_hash = ledger_hashes.get(external_id)
        if (
            ledger_hash is not None
            and ledger_hash == content_hash
            and external_id in normalized_by_external_id
        ):
            outcome.jobs_ledger_skipped += 1
            if external_id in new_external_ids:
                outcome.jobs_new -= 1
            else:
                outcome.jobs_updated -= 1
            await upsert_ledger_entry(
                db,
                company.id,
                external_id,
                content_hash,
                seen_at=now,
            )
            if structlog:
                logger.info(
                    "job_ledger_skipped",
                    company_id=str(company.id),
                    external_job_id=external_id,
                )
            continue
        raw_html = deterministic_fields.get("raw_html") or job.get("content") or ""
        description_text = _resolve_description_text(job, raw_html) or ""
        deterministic_fields["description_text"] = description_text or None
        deterministic_fields["description_preview"] = build_description_preview(description_text)
        raw_row = RawJob(
            company_id=company.id,
            external_job_id=external_id,
            platform=company.platform,
            raw_api_response=job,
            raw_html=raw_html,
            content_hash=content_hash,
            fetch_timestamp=now,
        )
        db.add(raw_row)
        await db.flush()

        job_archive_id = await upsert_job_archive_from_deterministic(
            db,
            deterministic_fields,
            company,
            description_text=deterministic_fields.get("description_text"),
        )

        normalized = await _upsert_normalized_core(
            db=db,
            company=company,
            raw_row=raw_row,
            deterministic_fields=deterministic_fields,
            settings=settings,
            existing_row=normalized_by_external_id.get(external_id),
            job_archive_id=job_archive_id,
            ledger_first_seen_at=ledger_first_seen.get(external_id),
        )
        normalized_by_external_id[external_id] = normalized

        await queue_job_for_enrichment(
            db=db,
            normalized_job_id=normalized.id,
            pipeline_run_id=pipeline_run_id,
            source=enrichment_source,
            priority=0,
        )
        await upsert_ledger_entry(
            db,
            company.id,
            external_id,
            content_hash,
            seen_at=now,
        )
        ledger_hashes[external_id] = content_hash

    for unchanged in classified.unchanged:
        external_id = str(unchanged.get("id"))
        await upsert_ledger_entry(
            db,
            company.id,
            external_id,
            compute_job_content_hash(unchanged, company.platform),
            seen_at=now,
        )
        existing = normalized_by_external_id.get(external_id)
        if existing:
            existing.last_seen_at = now
            existing.consecutive_misses = 0
            existing.is_active = True
            if existing.job_archive_id is None:
                existing.job_archive_id = await upsert_job_archive_from_normalized(
                    db, existing, company
                )

    outcome.jobs_removed = await _apply_removals(
        normalized_by_external_id,
        classified.removed_ids,
        settings.consecutive_misses_before_inactive,
    )

    recovered = company.consecutive_fetch_failures > 0
    company.consecutive_fetch_failures = 0
    company.last_successful_fetch_at = _utcnow()
    if recovered:
        await write_event(
            db,
            event_type=EventType.SOURCE_RECOVERED,
            category=EventCategory.SOURCE,
            severity=EventSeverity.INFO,
            platform=company.platform,
            company_id=company.id,
            pipeline_run_id=pipeline_run_id,
        )
    return outcome


async def _process_single_company(
    company_id: UUID,
    pipeline_run_id: UUID,
    settings: Settings,
) -> CompanyRunOutcome:
    async with AsyncSessionLocal() as db:
        company = await db.get(Company, company_id)
        if company is None:
            return CompanyRunOutcome(
                company_id=company_id,
                status="failed",
                error_message="Company not found during processing",
            )

        company_started = _utcnow()
        outcome = CompanyRunOutcome(company_id=company.id, status="success")
        try:
            await write_event(
                db,
                event_type=EventType.PIPELINE_STARTED,
                category=EventCategory.PIPELINE,
                severity=EventSeverity.INFO,
                platform=company.platform,
                company_id=company.id,
                pipeline_run_id=pipeline_run_id,
            )

            ledger_hashes = await load_ledger_hashes(db, company.id)
            raw_hashes = await _latest_hashes_for_company(db, company.id)
            normalized_map = await _normalized_map_for_company(db, company.id)
            baseline_run = _is_baseline_run(ledger_hashes, raw_hashes, normalized_map)
            raw_jobs, rejected_stale_fetch = await fetch_company_jobs(
                company,
                known_raw_by_id=await _latest_raw_by_external_id(db, company.id),
                known_raw_fetched_at=await _latest_raw_fetch_times(db, company.id),
                baseline_run=baseline_run,
            )
            outcome.jobs_rejected_stale_fetch = rejected_stale_fetch
            processed = await process_company_raw_jobs(
                db,
                company,
                raw_jobs,
                pipeline_run_id=pipeline_run_id,
                settings=settings,
            )
            outcome.jobs_fetched = processed.jobs_fetched
            outcome.jobs_new = processed.jobs_new
            outcome.jobs_updated = processed.jobs_updated
            outcome.jobs_unchanged = processed.jobs_unchanged
            outcome.jobs_removed = processed.jobs_removed
            outcome.jobs_deduped = processed.jobs_deduped
            outcome.jobs_ledger_skipped = processed.jobs_ledger_skipped
            outcome.jobs_ledger_baselined = processed.jobs_ledger_baselined
            outcome.jobs_rejected_stale_pipeline = processed.jobs_rejected_stale_pipeline
        except Exception as exc:  # noqa: BLE001
            outcome.status = "failed"
            outcome.error_message = str(exc)
            await db.rollback()
            company = await db.get(Company, company_id)
            if company is None:
                db.add(
                    CompanyRunResult(
                        pipeline_run_id=pipeline_run_id,
                        company_id=company_id,
                        status=outcome.status,
                        jobs_fetched=outcome.jobs_fetched,
                        jobs_new=outcome.jobs_new,
                        jobs_updated=outcome.jobs_updated,
                        jobs_unchanged=outcome.jobs_unchanged,
                        jobs_removed=outcome.jobs_removed,
                        error_message=outcome.error_message,
                        started_at=company_started,
                        completed_at=_utcnow(),
                    )
                )
                await db.commit()
                return outcome
            company.consecutive_fetch_failures += 1
            await write_event(
                db,
                event_type=EventType.SOURCE_FETCH_FAILED,
                category=EventCategory.SOURCE,
                severity=EventSeverity.ERROR,
                platform=company.platform,
                company_id=company.id,
                pipeline_run_id=pipeline_run_id,
                metadata={"error": outcome.error_message},
            )
            threshold = PLATFORM_FAILURE_ALERT_THRESHOLDS.get(
                company.platform,
                settings.max_consecutive_failures_before_alert,
            )
            if company.consecutive_fetch_failures >= threshold:
                write_failure_alert(
                    alerts_path=settings.alerts_path,
                    company=company,
                    consecutive_failures=company.consecutive_fetch_failures,
                    last_error=outcome.error_message,
                )
                await write_event(
                    db,
                    event_type=EventType.SOURCE_FAILURE_THRESHOLD_REACHED,
                    category=EventCategory.SOURCE,
                    severity=EventSeverity.CRITICAL,
                    platform=company.platform,
                    company_id=company.id,
                    pipeline_run_id=pipeline_run_id,
                    metadata={"consecutive_failures": company.consecutive_fetch_failures},
                )
            if structlog:
                logger.exception("company pipeline failed", company_id=str(company.id), board_token=company.board_token)
            else:
                logger.exception(
                    "company pipeline failed company_id=%s board_token=%s", str(company.id), company.board_token
                )

        db.add(
            CompanyRunResult(
                pipeline_run_id=pipeline_run_id,
                company_id=company.id,
                status=outcome.status,
                jobs_fetched=outcome.jobs_fetched,
                jobs_new=outcome.jobs_new,
                jobs_updated=outcome.jobs_updated,
                jobs_unchanged=outcome.jobs_unchanged,
                jobs_removed=outcome.jobs_removed,
                error_message=outcome.error_message,
                started_at=company_started,
                completed_at=_utcnow(),
            )
        )
        await db.commit()
        return outcome


class _PlatformFetchLimiter:
    def __init__(self, schedule: FetchScheduleConfig) -> None:
        self._schedule = schedule
        self._semaphores: dict[str, asyncio.Semaphore] = {}

    def _semaphore_for(self, platform: str) -> asyncio.Semaphore:
        if platform not in self._semaphores:
            throttle = self._schedule.throttles.for_platform(platform)
            self._semaphores[platform] = asyncio.Semaphore(throttle.concurrency)
        return self._semaphores[platform]

    async def run_company(
        self,
        platform: str,
        runner: Any,
    ) -> Any:
        throttle = self._schedule.throttles.for_platform(platform)
        async with self._semaphore_for(platform):
            result = await runner()
            if throttle.inter_company_seconds > 0:
                await asyncio.sleep(throttle.inter_company_seconds)
            return result


async def run_pipeline(
    db: AsyncSession,
    run_type: str = "manual",
    settings: Optional[Settings] = None,
    company_ids: Optional[list[UUID]] = None,
    schedule_metadata: Optional[dict[str, Any]] = None,
    force: bool = False,
) -> PipelineSnapshot:
    settings = settings or get_settings()
    schedule = settings.fetch_schedule()

    if company_ids is None and schedule_metadata is None:
        selection = await select_due_companies(db=db, settings=settings)
        company_ids = selection.company_ids
        schedule_metadata = selection.schedule_metadata
    elif company_ids is not None and not force and company_ids:
        companies_pre = (
            await db.scalars(
                select(Company).where(Company.id.in_(company_ids), Company.is_active.is_(True))
            )
        ).all()
        companies_by_id = {company.id: company for company in companies_pre}
        ordered = [companies_by_id[company_id] for company_id in company_ids if company_id in companies_by_id]
        filtered, decision = await apply_fetch_backpressure(db, ordered, settings=settings)
        schedule_metadata = {
            **(schedule_metadata or {}),
            "backpressure": backpressure_metadata(decision),
            "companies_selected": len(filtered),
        }
        company_ids = [company.id for company in filtered]

    run = PipelineRun(
        run_type=run_type,
        status="running",
        started_at=_utcnow(),
        schedule_metadata=schedule_metadata,
    )
    db.add(run)
    await db.flush()

    await write_event(
        db,
        event_type=EventType.PIPELINE_STARTED,
        category=EventCategory.PIPELINE,
        severity=EventSeverity.INFO,
        pipeline_run_id=run.id,
        metadata=schedule_metadata,
    )
    # Make the parent run visible to worker sessions before they emit events.
    await db.commit()

    if company_ids is not None:
        if not company_ids:
            companies = []
        else:
            companies = (
                await db.scalars(
                    select(Company)
                    .where(Company.id.in_(company_ids), Company.is_active.is_(True))
                    .order_by(Company.name.asc())
                )
            ).all()
    else:
        companies = (
            await db.scalars(select(Company).where(Company.is_active.is_(True)).order_by(Company.name.asc()))
        ).all()

    run.total_companies = len(companies)
    successful_companies = 0
    failed_companies = 0
    aggregate = CompanyStats()
    errors: list[dict[str, str]] = []

    if not companies:
        persisted_run = await db.get(PipelineRun, run.id)
        if persisted_run is None:
            raise RuntimeError(f"Pipeline run {run.id} missing before finalization.")
        persisted_run.status = "completed"
        persisted_run.completed_at = _utcnow()
        await write_event(
            db,
            event_type=EventType.PIPELINE_COMPLETED,
            category=EventCategory.PIPELINE,
            severity=EventSeverity.INFO,
            pipeline_run_id=run.id,
            metadata={
                "companies_selected": 0,
                **(
                    {"backpressure": schedule_metadata["backpressure"]}
                    if schedule_metadata and schedule_metadata.get("backpressure")
                    else {}
                ),
            },
        )
        await db.commit()
        return PipelineSnapshot(
            run_id=str(persisted_run.id),
            status=persisted_run.status,
            total_companies=0,
            successful_companies=0,
            failed_companies=0,
            jobs_fetched=0,
            jobs_new=0,
            jobs_updated=0,
            jobs_unchanged=0,
            jobs_removed=0,
        )

    limiter = _PlatformFetchLimiter(schedule)

    async def _run_company(company: Company) -> CompanyRunOutcome:
        async def _runner() -> CompanyRunOutcome:
            return await _process_single_company(
                company_id=company.id,
                pipeline_run_id=run.id,
                settings=settings,
            )

        return await limiter.run_company(company.platform, _runner)

    outcomes = await asyncio.gather(*[_run_company(company) for company in companies], return_exceptions=True)
    for company, raw_outcome in zip(companies, outcomes):
        if isinstance(raw_outcome, Exception):
            failed_companies += 1
            errors.append({"company_id": str(company.id), "error": str(raw_outcome)})
            continue
        outcome = raw_outcome
        if outcome.status == "success":
            successful_companies += 1
        else:
            failed_companies += 1
            errors.append({"company_id": str(company.id), "error": outcome.error_message or "unknown"})
        aggregate.jobs_fetched += outcome.jobs_fetched
        aggregate.jobs_new += outcome.jobs_new
        aggregate.jobs_updated += outcome.jobs_updated
        aggregate.jobs_unchanged += outcome.jobs_unchanged
        aggregate.jobs_removed += outcome.jobs_removed
        aggregate.jobs_rejected_stale_fetch += outcome.jobs_rejected_stale_fetch
        aggregate.jobs_rejected_stale_pipeline += outcome.jobs_rejected_stale_pipeline

    persisted_run = await db.get(PipelineRun, run.id)
    if persisted_run is None:
        raise RuntimeError(f"Pipeline run {run.id} missing before finalization.")

    persisted_run.status = _resolve_terminal_status(
        successful_companies=successful_companies,
        failed_companies=failed_companies,
    )
    persisted_run.completed_at = _utcnow()
    persisted_run.successful_companies = successful_companies
    persisted_run.failed_companies = failed_companies
    persisted_run.jobs_fetched = aggregate.jobs_fetched
    persisted_run.jobs_new = aggregate.jobs_new
    persisted_run.jobs_updated = aggregate.jobs_updated
    persisted_run.jobs_unchanged = aggregate.jobs_unchanged
    persisted_run.jobs_removed = aggregate.jobs_removed
    persisted_run.error_summary = errors or None
    freshness_metadata = {
        "rejected_fetch": aggregate.jobs_rejected_stale_fetch,
        "rejected_pipeline": aggregate.jobs_rejected_stale_pipeline,
    }
    if persisted_run.schedule_metadata:
        persisted_run.schedule_metadata = {
            **persisted_run.schedule_metadata,
            "freshness": freshness_metadata,
        }
    else:
        persisted_run.schedule_metadata = {"freshness": freshness_metadata}

    terminal_event = EventType.PIPELINE_COMPLETED
    terminal_severity = EventSeverity.INFO
    if persisted_run.status == "partial_success":
        terminal_event = EventType.PIPELINE_PARTIAL_SUCCESS
        terminal_severity = EventSeverity.WARNING
    elif persisted_run.status == "failed":
        terminal_event = EventType.PIPELINE_FAILED
        terminal_severity = EventSeverity.ERROR
    await write_event(
        db,
        event_type=terminal_event,
        category=EventCategory.PIPELINE,
        severity=terminal_severity,
        pipeline_run_id=run.id,
        metadata={"failed_companies": failed_companies, "successful_companies": successful_companies},
    )

    await db.commit()

    from app.ingestion.stats_publisher import publish_ops_stats

    await publish_ops_stats(db, settings=settings, trigger=f"pipeline_{run_type}")

    return PipelineSnapshot(
        run_id=str(persisted_run.id),
        status=persisted_run.status,
        total_companies=persisted_run.total_companies,
        successful_companies=persisted_run.successful_companies,
        failed_companies=persisted_run.failed_companies,
        jobs_fetched=persisted_run.jobs_fetched,
        jobs_new=persisted_run.jobs_new,
        jobs_updated=persisted_run.jobs_updated,
        jobs_unchanged=persisted_run.jobs_unchanged,
        jobs_removed=persisted_run.jobs_removed,
    )
