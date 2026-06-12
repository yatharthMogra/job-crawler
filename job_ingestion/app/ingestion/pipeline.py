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

from app.config import Settings, get_settings
from app.database import AsyncSessionLocal
from app.exceptions import IngestionError
from app.ingestion.alerts import write_failure_alert
from app.ingestion.change_detector import classify_jobs
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
from app.ingestion.job_archive_sync import (
    upsert_job_archive_from_deterministic,
    upsert_job_archive_from_normalized,
)
from app.models.company import Company
from app.models.normalized_job import NormalizedJob
from app.models.pipeline_run import CompanyRunResult, PipelineRun
from app.models.raw_job import RawJob
from app.utils.hashing import compute_content_hash

logger = structlog.get_logger(__name__) if structlog else logging.getLogger(__name__)
TerminalRunStatus = Literal["completed", "partial_success", "failed"]


@dataclass
class CompanyStats:
    jobs_fetched: int = 0
    jobs_new: int = 0
    jobs_updated: int = 0
    jobs_unchanged: int = 0
    jobs_removed: int = 0


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


async def _normalized_map_for_company(db: AsyncSession, company_id: Any) -> dict[str, NormalizedJob]:
    stmt = select(NormalizedJob).where(NormalizedJob.company_id == company_id)
    jobs = (await db.scalars(stmt)).all()
    return {row.external_job_id: row for row in jobs}


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


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
) -> None:
    now = _utcnow()
    payload = dict(
        raw_job_id=raw_row.id,
        company_id=company.id,
        job_archive_id=job_archive_id,
        external_job_id=deterministic_fields["external_job_id"],
        title=deterministic_fields["title"] or "Untitled",
        company_name=company.name,
        location=deterministic_fields["location"],
        department=deterministic_fields["department"],
        employment_type=deterministic_fields["employment_type"],
        posting_url=deterministic_fields["posting_url"],
        description_text=deterministic_fields.get("description_text"),
        description_preview=deterministic_fields.get("description_preview"),
        posted_at=deterministic_fields["posted_at"],
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

            raw_jobs = await fetch_company_jobs(company)
            outcome.jobs_fetched = len(raw_jobs)
            previous_hashes = await _latest_hashes_for_company(db, company.id)
            normalized_by_external_id = await _normalized_map_for_company(db, company.id)
            active_ids = {job_id for job_id, row in normalized_by_external_id.items() if row.is_active}
            classified = classify_jobs(raw_jobs, previous_hashes, active_ids)
            outcome.jobs_new = len(classified.new)
            outcome.jobs_updated = len(classified.updated)
            outcome.jobs_unchanged = len(classified.unchanged)

            changed_jobs = classified.new + classified.updated
            for job in changed_jobs:
                deterministic_fields = extract_deterministic_fields(job, platform=company.platform)
                external_id = deterministic_fields["external_job_id"]
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
                    content_hash=compute_content_hash(job),
                    fetch_timestamp=_utcnow(),
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
                )
                normalized_by_external_id[external_id] = normalized

                await queue_job_for_enrichment(
                    db=db,
                    normalized_job_id=normalized.id,
                    pipeline_run_id=pipeline_run_id,
                    source="pipeline",
                    priority=0,
                )

            now = _utcnow()
            for unchanged in classified.unchanged:
                external_id = str(unchanged.get("id"))
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
        except Exception as exc:  # noqa: BLE001
            outcome.status = "failed"
            outcome.error_message = str(exc)
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
            if company.consecutive_fetch_failures >= settings.max_consecutive_failures_before_alert:
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


async def run_pipeline(
    db: AsyncSession,
    run_type: str = "manual",
    settings: Optional[Settings] = None,
) -> PipelineSnapshot:
    settings = settings or get_settings()

    run = PipelineRun(run_type=run_type, status="running", started_at=_utcnow())
    db.add(run)
    await db.flush()

    await write_event(
        db,
        event_type=EventType.PIPELINE_STARTED,
        category=EventCategory.PIPELINE,
        severity=EventSeverity.INFO,
        pipeline_run_id=run.id,
    )
    # Make the parent run visible to worker sessions before they emit events.
    await db.commit()

    companies = (
        await db.scalars(select(Company).where(Company.is_active.is_(True)).order_by(Company.name.asc()))
    ).all()

    run.total_companies = len(companies)
    successful_companies = 0
    failed_companies = 0
    aggregate = CompanyStats()
    errors: list[dict[str, str]] = []

    semaphore = asyncio.Semaphore(settings.fetch_concurrency)

    async def _run_company(company_id: UUID) -> CompanyRunOutcome:
        async with semaphore:
            return await _process_single_company(company_id=company_id, pipeline_run_id=run.id, settings=settings)

    outcomes = await asyncio.gather(*[_run_company(company.id) for company in companies], return_exceptions=True)
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
