from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.database import AsyncSessionLocal
from app.ingestion.constants import FailureReason, ProcessingState
from app.ingestion.extractor.llm import (
    BatchJobEnrichment,
    DEFAULT_ENRICHMENT,
    enrich_job_batch_text,
    enrichment_missing_skill_fields,
)
from app.ingestion.extractor.text_cleaner import clean_job_description
from app.ingestion.recommendation_fields import assign_retrieval_pools, compute_opportunity_score
from app.llm.factory import get_llm_provider
from app.models.company import Company
from app.models.enrichment_batch import EnrichmentBatch
from app.models.enrichment_batch_item import EnrichmentBatchItem
from app.models.enrichment_queue import EnrichmentQueue
from app.models.job_enrichment import JobEnrichment
from app.models.normalized_job import NormalizedJob
from app.models.raw_job import RawJob


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _is_retryable_error(message: str) -> bool:
    lowered = message.lower()
    return any(
        term in lowered
        for term in [
            "429",
            "resource_exhausted",
            "quota",
            "rate",
            "503",
            "unavailable",
            "timeout",
        ]
    )


def _estimate_tokens_fallback(clean_text: str) -> int:
    return max(32, len(clean_text) // 4)


@dataclass
class WorkItem:
    queue_row: EnrichmentQueue
    normalized: NormalizedJob
    raw_job: RawJob
    company: Company
    clean_text: str
    estimated_tokens: int
    priority_bucket: str


class EnrichmentWorker:
    def __init__(self, settings: Optional[Settings] = None) -> None:
        self._settings = settings or get_settings()
        self._stop = asyncio.Event()
        self._wake = asyncio.Event()

    def stop(self) -> None:
        self._stop.set()
        self._wake.set()

    def wake(self) -> None:
        self._wake.set()

    async def run_forever(self) -> None:
        while not self._stop.is_set():
            batches_processed = 0
            try:
                async with AsyncSessionLocal() as db:
                    processed, batches_processed = await process_enrichment_window(
                        db=db, settings=self._settings
                    )
            except Exception:
                processed = 0

            if batches_processed > 0:
                await asyncio.sleep(self._settings.enrichment_window_seconds)
                continue

            self._wake.clear()
            try:
                await asyncio.wait_for(self._wake.wait(), timeout=2.0)
            except asyncio.TimeoutError:
                continue


async def queue_job_for_enrichment(
    db: AsyncSession,
    normalized_job_id: UUID,
    pipeline_run_id: Optional[UUID],
    source: str = "pipeline",
    priority: int = 0,
) -> None:
    existing = await db.scalar(
        select(EnrichmentQueue).where(EnrichmentQueue.normalized_job_id == normalized_job_id)
    )
    if existing:
        existing.pipeline_run_id = pipeline_run_id
        existing.source = source
        existing.status = "queued"
        existing.priority = priority
        existing.attempt_count = 0
        existing.next_retry_at = None
        existing.last_error = None
        existing.last_failure_reason = None
        existing.estimated_input_tokens = None
        get_enrichment_worker().wake()
        return

    db.add(
        EnrichmentQueue(
            normalized_job_id=normalized_job_id,
            pipeline_run_id=pipeline_run_id,
            source=source,
            status="queued",
            attempt_count=0,
            priority=priority,
        )
    )
    get_enrichment_worker().wake()


async def _estimate_tokens(settings: Settings, clean_text: str) -> int:
    if settings.enrichment_token_estimation_strategy != "count_tokens":
        return _estimate_tokens_fallback(clean_text)
    try:
        provider = get_llm_provider(settings)
        prompt = (
            "You extract structured hiring attributes from job descriptions.\n\n"
            f"Job description text:\n{clean_text}\n\nReturn JSON only."
        )
        estimated = await provider.count_tokens(prompt)
        if estimated > 0:
            return estimated
    except Exception:
        pass
    return _estimate_tokens_fallback(clean_text)


async def _build_work_items(
    db: AsyncSession,
    settings: Settings,
    queue_rows: list[EnrichmentQueue],
    priority_bucket: str,
) -> list[WorkItem]:
    items: list[WorkItem] = []
    for queue_row in queue_rows:
        normalized = await db.get(NormalizedJob, queue_row.normalized_job_id)
        if normalized is None:
            queue_row.status = "failed"
            queue_row.last_failure_reason = FailureReason.MISSING_REQUIRED_FIELDS
            queue_row.last_error = "Normalized job not found."
            continue
        raw_job = await db.get(RawJob, normalized.raw_job_id)
        if raw_job is None:
            queue_row.status = "failed"
            queue_row.last_failure_reason = FailureReason.MISSING_REQUIRED_FIELDS
            queue_row.last_error = "Raw job not found."
            continue
        company = await db.get(Company, normalized.company_id)
        if company is None:
            queue_row.status = "failed"
            queue_row.last_failure_reason = FailureReason.MISSING_REQUIRED_FIELDS
            queue_row.last_error = "Company not found."
            continue
        clean_text = clean_job_description(raw_job.raw_html or "")
        estimated_tokens = await _estimate_tokens(settings, clean_text)
        queue_row.estimated_input_tokens = estimated_tokens
        items.append(
            WorkItem(
                queue_row=queue_row,
                normalized=normalized,
                raw_job=raw_job,
                company=company,
                clean_text=clean_text,
                estimated_tokens=estimated_tokens,
                priority_bucket=priority_bucket,
            )
        )
    return items


def _pack_batches(settings: Settings, items: list[WorkItem]) -> tuple[list[list[WorkItem]], list[WorkItem]]:
    ordered = sorted(items, key=lambda row: row.estimated_tokens, reverse=True)
    batches: list[list[WorkItem]] = []
    deferred: list[WorkItem] = []
    total_budget = 0

    for item in ordered:
        if total_budget + item.estimated_tokens > settings.enrichment_window_token_budget:
            deferred.append(item)
            continue
        placed = False
        for batch in batches:
            batch_tokens = sum(row.estimated_tokens for row in batch)
            if len(batch) >= settings.enrichment_micro_batch_size:
                continue
            if batch_tokens + item.estimated_tokens > settings.enrichment_max_input_tokens_per_batch:
                continue
            batch.append(item)
            total_budget += item.estimated_tokens
            placed = True
            break
        if placed:
            continue
        batches.append([item])
        total_budget += item.estimated_tokens
    return batches, deferred


def _allocate_tokens(total_tokens: int, estimates: list[int]) -> list[int]:
    if not estimates:
        return []
    total_estimate = sum(estimates)
    if total_estimate <= 0:
        even = total_tokens // len(estimates) if estimates else 0
        allocations = [even for _ in estimates]
        if allocations:
            allocations[0] += total_tokens - sum(allocations)
        return allocations
    allocations = [int(total_tokens * est / total_estimate) for est in estimates]
    if allocations:
        allocations[0] += total_tokens - sum(allocations)
    return allocations


def _apply_enrichment_to_job(
    normalized: NormalizedJob,
    enrichment: BatchJobEnrichment,
    settings: Settings,
) -> None:
    normalized.seniority = enrichment.seniority
    normalized.is_internship = enrichment.is_internship
    normalized.is_new_grad = enrichment.is_new_grad
    normalized.sponsorship_status = enrichment.sponsorship_status
    normalized.sponsorship_confidence = enrichment.sponsorship_confidence
    normalized.remote_type = enrichment.remote_type
    normalized.tech_stack = enrichment.tech_stack
    normalized.skills = enrichment.skills
    normalized.normalized_roles = list(enrichment.normalized_roles)
    normalized.job_capabilities = list(enrichment.job_capabilities)
    normalized.application_effort = enrichment.application_effort
    normalized.salary_min = enrichment.salary_min
    normalized.salary_max = enrichment.salary_max
    normalized.retrieval_pools = assign_retrieval_pools(
        normalized.normalized_roles,
        normalized.is_internship,
        normalized.is_new_grad,
    )
    now = _utcnow()
    normalized.opportunity_score = compute_opportunity_score(
        normalized.posted_at,
        normalized.salary_min,
        normalized.salary_max,
        normalized.application_effort,
        settings=settings,
    )
    normalized.opportunity_score_computed_at = now
    normalized.processing_state = ProcessingState.SUCCESS
    normalized.failure_reason = None
    normalized.last_failure_at = None


def _recommendation_fields_from_enrichment(
    normalized: NormalizedJob,
    enrichment: BatchJobEnrichment,
    settings: Settings,
) -> dict:
    normalized_roles = list(enrichment.normalized_roles)
    retrieval_pools = assign_retrieval_pools(
        normalized_roles,
        enrichment.is_internship,
        enrichment.is_new_grad,
    )
    computed_at = _utcnow()
    opportunity_score = compute_opportunity_score(
        normalized.posted_at,
        enrichment.salary_min,
        enrichment.salary_max,
        enrichment.application_effort,
        settings=settings,
    )
    return {
        "normalized_roles": normalized_roles,
        "job_capabilities": list(enrichment.job_capabilities),
        "application_effort": enrichment.application_effort,
        "retrieval_pools": retrieval_pools,
        "salary_min": enrichment.salary_min,
        "salary_max": enrichment.salary_max,
        "opportunity_score": opportunity_score,
        "opportunity_score_computed_at": computed_at,
    }


def _mark_for_retry(
    queue_row: EnrichmentQueue,
    settings: Settings,
    failure_reason: str,
    error_message: str,
) -> None:
    queue_row.attempt_count += 1
    queue_row.last_failure_reason = failure_reason
    queue_row.last_error = error_message
    if queue_row.attempt_count > settings.enrichment_max_retries:
        queue_row.status = "failed"
        queue_row.last_failure_reason = "retry_limit_exceeded"
        return
    queue_row.status = "cooldown"
    queue_row.next_retry_at = _utcnow() + timedelta(seconds=settings.enrichment_cooldown_seconds)


async def _process_batch(
    db: AsyncSession,
    settings: Settings,
    batch_items: list[WorkItem],
    source: str,
) -> None:
    started = _utcnow()
    batch = EnrichmentBatch(
        pipeline_run_id=batch_items[0].queue_row.pipeline_run_id if batch_items else None,
        source=source,
        status="running",
        jobs_total=len(batch_items),
        jobs_first_attempt=sum(1 for row in batch_items if row.priority_bucket == "first_attempt"),
        jobs_retry=sum(1 for row in batch_items if row.priority_bucket == "retry"),
        estimated_input_tokens=sum(row.estimated_tokens for row in batch_items),
    )
    db.add(batch)
    await db.flush()

    for row in batch_items:
        row.queue_row.status = "in_progress"
        db.add(
            EnrichmentBatchItem(
                batch_id=batch.id,
                queue_id=row.queue_row.id,
                normalized_job_id=row.normalized.id,
                status="pending",
                priority_bucket=row.priority_bucket,
                attempt_number=row.queue_row.attempt_count + 1,
                estimated_input_tokens=row.estimated_tokens,
            )
        )
    await db.flush()

    payload_jobs = [{"job_id": str(row.normalized.id), "text": row.clean_text} for row in batch_items]
    provider = get_llm_provider(settings)
    try:
        result = await enrich_job_batch_text(provider, payload_jobs)
        by_job_id = {entry.job_id: entry for entry in result.output.items}
        input_allocations = _allocate_tokens(result.input_tokens, [row.estimated_tokens for row in batch_items])
        output_allocations = _allocate_tokens(result.output_tokens, [row.estimated_tokens for row in batch_items])
        batch.actual_input_tokens = result.input_tokens
        batch.actual_output_tokens = result.output_tokens
        batch.latency_ms = result.latency_ms

        items = (
            await db.scalars(select(EnrichmentBatchItem).where(EnrichmentBatchItem.batch_id == batch.id))
        ).all()
        items_by_job = {str(item.normalized_job_id): item for item in items}

        for idx, row in enumerate(batch_items):
            enrichment = by_job_id.get(str(row.normalized.id))
            item = items_by_job.get(str(row.normalized.id))
            input_tokens = input_allocations[idx] if idx < len(input_allocations) else 0
            output_tokens = output_allocations[idx] if idx < len(output_allocations) else 0
            row.queue_row.last_actual_input_tokens = input_tokens
            row.queue_row.last_actual_output_tokens = output_tokens

            if enrichment is None:
                row.normalized.processing_state = ProcessingState.PARTIAL_SUCCESS
                row.normalized.failure_reason = FailureReason.LLM_SCHEMA_MISMATCH
                row.normalized.last_failure_at = _utcnow()
                _mark_for_retry(
                    queue_row=row.queue_row,
                    settings=settings,
                    failure_reason=FailureReason.LLM_SCHEMA_MISMATCH,
                    error_message="Missing job result in batch response.",
                )
                if item is not None:
                    item.status = "failed"
                    item.failure_reason = FailureReason.LLM_SCHEMA_MISMATCH
                    item.actual_input_tokens = input_tokens
                    item.actual_output_tokens = output_tokens
                db.add(
                    JobEnrichment(
                        normalized_job_id=row.normalized.id,
                        raw_job_id=row.raw_job.id,
                        enrichment_batch_id=batch.id,
                        llm_provider=settings.llm_provider,
                        llm_model=settings.gemini_model if settings.llm_provider == "gemini" else None,
                        extraction_version=settings.extraction_version,
                        seniority=DEFAULT_ENRICHMENT.seniority,
                        is_internship=DEFAULT_ENRICHMENT.is_internship,
                        is_new_grad=DEFAULT_ENRICHMENT.is_new_grad,
                        sponsorship_status=DEFAULT_ENRICHMENT.sponsorship_status,
                        sponsorship_confidence=DEFAULT_ENRICHMENT.sponsorship_confidence,
                        remote_type=DEFAULT_ENRICHMENT.remote_type,
                        tech_stack=DEFAULT_ENRICHMENT.tech_stack,
                        skills=DEFAULT_ENRICHMENT.skills,
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                        latency_ms=result.latency_ms,
                        status="failed",
                        failure_reason=FailureReason.LLM_SCHEMA_MISMATCH,
                    )
                )
                continue

            if enrichment_missing_skill_fields(
                enrichment.tech_stack,
                enrichment.skills,
                description_chars=len(row.clean_text),
                normalized_roles=list(enrichment.normalized_roles),
            ):
                row.normalized.processing_state = ProcessingState.PARTIAL_SUCCESS
                row.normalized.failure_reason = FailureReason.EMPTY_SKILL_EXTRACTION
                row.normalized.last_failure_at = _utcnow()
                _mark_for_retry(
                    queue_row=row.queue_row,
                    settings=settings,
                    failure_reason=FailureReason.EMPTY_SKILL_EXTRACTION,
                    error_message="LLM returned empty tech_stack and skills for substantive description.",
                )
                if item is not None:
                    item.status = "failed"
                    item.failure_reason = FailureReason.EMPTY_SKILL_EXTRACTION
                    item.actual_input_tokens = input_tokens
                    item.actual_output_tokens = output_tokens
                db.add(
                    JobEnrichment(
                        normalized_job_id=row.normalized.id,
                        raw_job_id=row.raw_job.id,
                        enrichment_batch_id=batch.id,
                        llm_provider=settings.llm_provider,
                        llm_model=settings.gemini_model if settings.llm_provider == "gemini" else None,
                        extraction_version=settings.extraction_version,
                        seniority=enrichment.seniority,
                        is_internship=enrichment.is_internship,
                        is_new_grad=enrichment.is_new_grad,
                        sponsorship_status=enrichment.sponsorship_status,
                        sponsorship_confidence=enrichment.sponsorship_confidence,
                        remote_type=enrichment.remote_type,
                        tech_stack=enrichment.tech_stack,
                        skills=enrichment.skills,
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                        latency_ms=result.latency_ms,
                        status="failed",
                        failure_reason=FailureReason.EMPTY_SKILL_EXTRACTION,
                    )
                )
                continue

            _apply_enrichment_to_job(row.normalized, enrichment, settings)
            recommendation_fields = _recommendation_fields_from_enrichment(row.normalized, enrichment, settings)
            row.queue_row.status = "completed"
            row.queue_row.next_retry_at = None
            row.queue_row.last_failure_reason = None
            row.queue_row.last_error = None
            if item is not None:
                item.status = "success"
                item.actual_input_tokens = input_tokens
                item.actual_output_tokens = output_tokens
            db.add(
                JobEnrichment(
                    normalized_job_id=row.normalized.id,
                    raw_job_id=row.raw_job.id,
                    enrichment_batch_id=batch.id,
                    llm_provider=settings.llm_provider,
                    llm_model=settings.gemini_model if settings.llm_provider == "gemini" else None,
                    extraction_version=settings.extraction_version,
                    seniority=enrichment.seniority,
                    is_internship=enrichment.is_internship,
                    is_new_grad=enrichment.is_new_grad,
                    sponsorship_status=enrichment.sponsorship_status,
                    sponsorship_confidence=enrichment.sponsorship_confidence,
                    remote_type=enrichment.remote_type,
                    tech_stack=enrichment.tech_stack,
                    skills=enrichment.skills,
                    **recommendation_fields,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    latency_ms=result.latency_ms,
                    status="success",
                    failure_reason=None,
                )
            )

        batch.status = "completed"
    except Exception as exc:
        message = str(exc)
        retryable = _is_retryable_error(message)
        items = (
            await db.scalars(select(EnrichmentBatchItem).where(EnrichmentBatchItem.batch_id == batch.id))
        ).all()
        items_by_job = {item.queue_id: item for item in items}
        for row in batch_items:
            if retryable:
                _mark_for_retry(
                    queue_row=row.queue_row,
                    settings=settings,
                    failure_reason=FailureReason.TOKEN_LIMIT_EXCEEDED,
                    error_message=message,
                )
            else:
                row.queue_row.status = "failed"
                row.queue_row.last_failure_reason = FailureReason.LLM_SCHEMA_MISMATCH
                row.queue_row.last_error = message
            row.normalized.processing_state = ProcessingState.PARTIAL_SUCCESS
            row.normalized.failure_reason = row.queue_row.last_failure_reason
            row.normalized.last_failure_at = _utcnow()
            db.add(
                JobEnrichment(
                    normalized_job_id=row.normalized.id,
                    raw_job_id=row.raw_job.id,
                    enrichment_batch_id=batch.id,
                    llm_provider=settings.llm_provider,
                    llm_model=settings.gemini_model if settings.llm_provider == "gemini" else None,
                    extraction_version=settings.extraction_version,
                    seniority=DEFAULT_ENRICHMENT.seniority,
                    is_internship=DEFAULT_ENRICHMENT.is_internship,
                    is_new_grad=DEFAULT_ENRICHMENT.is_new_grad,
                    sponsorship_status=DEFAULT_ENRICHMENT.sponsorship_status,
                    sponsorship_confidence=DEFAULT_ENRICHMENT.sponsorship_confidence,
                    remote_type=DEFAULT_ENRICHMENT.remote_type,
                    tech_stack=DEFAULT_ENRICHMENT.tech_stack,
                    skills=DEFAULT_ENRICHMENT.skills,
                    input_tokens=0,
                    output_tokens=0,
                    latency_ms=0,
                    status="failed",
                    failure_reason=row.queue_row.last_failure_reason,
                )
            )
            item = items_by_job.get(row.queue_row.id)
            if item is not None:
                item.status = "failed"
                item.failure_reason = row.queue_row.last_failure_reason
                item.last_error = message
        batch.status = "failed"
        batch.failure_reason = FailureReason.TOKEN_LIMIT_EXCEEDED if retryable else FailureReason.LLM_SCHEMA_MISMATCH
        batch.last_error = message

    batch.completed_at = _utcnow()
    batch.latency_ms = int((batch.completed_at - started).total_seconds() * 1000)


async def process_enrichment_window(
    db: AsyncSession, settings: Optional[Settings] = None
) -> tuple[int, int]:
    settings = settings or get_settings()
    now = _utcnow()
    eligible = and_(
        EnrichmentQueue.status.in_(["queued", "cooldown"]),
        or_(EnrichmentQueue.next_retry_at.is_(None), EnrichmentQueue.next_retry_at <= now),
    )
    first_attempt_rows = (
        await db.scalars(
            select(EnrichmentQueue)
            .where(eligible, EnrichmentQueue.attempt_count == 0)
            .order_by(EnrichmentQueue.created_at.asc())
            .limit(settings.enrichment_max_jobs_per_window)
        )
    ).all()

    remaining_capacity = max(0, settings.enrichment_max_jobs_per_window - len(first_attempt_rows))
    retry_rows: list[EnrichmentQueue] = []
    if remaining_capacity > 0:
        retry_rows = (
            await db.scalars(
                select(EnrichmentQueue)
                .where(eligible, EnrichmentQueue.attempt_count > 0)
                .order_by(EnrichmentQueue.next_retry_at.asc(), EnrichmentQueue.updated_at.asc())
                .limit(remaining_capacity)
            )
        ).all()

    first_work = await _build_work_items(db=db, settings=settings, queue_rows=first_attempt_rows, priority_bucket="first_attempt")
    retry_work = await _build_work_items(db=db, settings=settings, queue_rows=retry_rows, priority_bucket="retry")
    candidates = first_work + retry_work
    if not candidates:
        await db.commit()
        return 0, 0

    batches, deferred = _pack_batches(settings=settings, items=candidates)
    for row in deferred:
        row.queue_row.status = "queued"
    if not batches:
        await db.commit()
        return 0, 0

    batches = batches[: settings.enrichment_max_batches_per_window]
    processed_jobs = 0
    for batch in batches:
        await _process_batch(db=db, settings=settings, batch_items=batch, source="worker")
        processed_jobs += len(batch)
        await db.commit()
    return processed_jobs, len(batches)


async def process_job_immediately(
    db: AsyncSession,
    normalized_job_id: UUID,
    settings: Optional[Settings] = None,
) -> dict[str, str]:
    settings = settings or get_settings()
    normalized = await db.get(NormalizedJob, normalized_job_id)
    if normalized is None:
        raise ValueError("Job not found")
    raw_job = await db.get(RawJob, normalized.raw_job_id)
    if raw_job is None:
        raise ValueError("Raw payload not found for job")
    company = await db.get(Company, normalized.company_id)
    if company is None:
        raise ValueError("Company not found for job")

    queue_row = await db.scalar(select(EnrichmentQueue).where(EnrichmentQueue.normalized_job_id == normalized.id))
    if queue_row is None:
        queue_row = EnrichmentQueue(
            normalized_job_id=normalized.id,
            pipeline_run_id=None,
            source="manual",
            status="queued",
            attempt_count=0,
            priority=1000,
        )
        db.add(queue_row)
        await db.flush()
    clean_text = clean_job_description(raw_job.raw_html or "")
    estimated_tokens = await _estimate_tokens(settings, clean_text)
    queue_row.estimated_input_tokens = estimated_tokens
    queue_row.source = "manual"

    item = WorkItem(
        queue_row=queue_row,
        normalized=normalized,
        raw_job=raw_job,
        company=company,
        clean_text=clean_text,
        estimated_tokens=estimated_tokens,
        priority_bucket="manual",
    )
    await _process_batch(db=db, settings=settings, batch_items=[item], source="manual")
    await db.commit()
    return {"job_id": str(normalized.id), "status": queue_row.status}


_ENRICHMENT_WORKER: Optional[EnrichmentWorker] = None


def get_enrichment_worker(settings: Optional[Settings] = None) -> EnrichmentWorker:
    global _ENRICHMENT_WORKER
    if _ENRICHMENT_WORKER is None:
        _ENRICHMENT_WORKER = EnrichmentWorker(settings=settings)
    return _ENRICHMENT_WORKER
