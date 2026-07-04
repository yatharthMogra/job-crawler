from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Callable, Optional
from uuid import UUID

from sqlalchemy import and_, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.database import AsyncSessionLocal
from app.ingestion.constants import EventCategory, EventSeverity, EventType, FailureReason, ProcessingState
from app.ingestion.events import write_event
from app.ingestion.notification_events import enqueue_notification_job_events
from app.ingestion.extractor.llm import (
    BatchJobEnrichment,
    DEFAULT_ENRICHMENT,
    enrich_job_batch_text,
    enrichment_missing_skill_fields,
)
from app.ingestion.extractor.seniority import build_batch_job_payload
from app.ingestion.extractor.text_cleaner import clean_job_description
from app.ingestion.job_archive_sync import update_job_archive_after_enrichment
from app.ingestion.job_freshness import FreshnessVerdict, refresh_posted_at_verdict
from app.ingestion.job_purge import PurgeTarget, purge_normalized_jobs
from app.ingestion.recommendation_fields import (
    assign_validated_retrieval_pools,
    compute_opportunity_score,
    fields_for_job_enrichment_record,
)
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


def _is_daily_quota_exhausted(message: str) -> bool:
    """True only for explicit daily quota exhaustion, not generic 429 RESOURCE_EXHAUSTED."""
    lowered = message.lower()
    daily_markers = (
        "per day",
        "perday",
        "/day",
        "daily",
        "generate_requests_per_day",
        "generaterequestsperday",
        "quota exceeded for metric",
    )
    if any(marker in lowered for marker in daily_markers):
        return True
    if "exceeded your current quota" in lowered:
        return True
    return False


def _is_transient_rate_limit(message: str) -> bool:
    if _is_daily_quota_exhausted(message):
        return False
    lowered = message.lower()
    if any(
        term in lowered
        for term in [
            "429",
            "503",
            "unavailable",
            "timeout",
            "rate limit",
            "rate_limit",
            "too many requests",
            "resource_exhausted",
        ]
    ):
        return True
    return False


def _is_provider_capacity_error(message: str) -> bool:
    return _is_daily_quota_exhausted(message) or _is_transient_rate_limit(message)


def _is_retryable_error(message: str) -> bool:
    return _is_transient_rate_limit(message)


def _is_schema_validation_error(message: str) -> bool:
    lowered = message.lower()
    return any(
        term in lowered
        for term in [
            "validation error",
            "input should be",
            "failed to parse batch enrichment",
            "jsondecodeerror",
            "invalid json",
            "model_validate",
        ]
    )


def _mark_quota_blocked(queue_row: EnrichmentQueue, error_message: str) -> None:
    queue_row.status = "quota_blocked"
    queue_row.last_failure_reason = FailureReason.TOKEN_LIMIT_EXCEEDED
    queue_row.last_error = error_message


def _partition_filter(worker_id: int, worker_count: int):
    return text(
        "mod(abs(hashtext(enrichment_queue.normalized_job_id::text)), :worker_count) = :worker_id"
    ).bindparams(worker_count=worker_count, worker_id=worker_id)


def _estimate_tokens_fallback(clean_text: str) -> int:
    return max(32, len(clean_text) // 4)


async def _emit_stale_rejection_event(
    db: AsyncSession,
    *,
    normalized: NormalizedJob,
    company: Company,
    queue_row: EnrichmentQueue,
    posted_at: datetime | None,
    stage: str,
) -> None:
    await write_event(
        db,
        event_type=EventType.JOB_REJECTED_STALE,
        category=EventCategory.ENRICHMENT,
        severity=EventSeverity.INFO,
        platform=company.platform,
        company_id=company.id,
        pipeline_run_id=queue_row.pipeline_run_id,
        normalized_job_id=normalized.id,
        metadata={
            "stage": stage,
            "external_job_id": normalized.external_job_id,
            "posted_at": posted_at.isoformat() if posted_at else None,
        },
    )


async def _purge_if_stale_before_enrichment(
    db: AsyncSession,
    *,
    normalized: NormalizedJob,
    raw_job: RawJob,
    company: Company,
    queue_row: EnrichmentQueue,
    settings: Settings,
) -> bool:
    posted_at, verdict = refresh_posted_at_verdict(
        normalized.posted_at,
        raw_job.raw_api_response,
        company.platform,
        settings=settings,
    )
    if posted_at is not None:
        normalized.posted_at = posted_at
    if verdict != FreshnessVerdict.STALE:
        return False

    await _emit_stale_rejection_event(
        db,
        normalized=normalized,
        company=company,
        queue_row=queue_row,
        posted_at=posted_at,
        stage="pre_enrichment",
    )
    await purge_normalized_jobs(
        db,
        [
            PurgeTarget(
                id=normalized.id,
                raw_job_id=normalized.raw_job_id,
                job_archive_id=normalized.job_archive_id,
            )
        ],
    )
    return True


async def _purge_if_stale_after_enrichment(
    db: AsyncSession,
    *,
    normalized: NormalizedJob,
    raw_job: RawJob,
    company: Company,
    queue_row: EnrichmentQueue,
    settings: Settings,
    batch_item: EnrichmentBatchItem | None,
) -> bool:
    posted_at, verdict = refresh_posted_at_verdict(
        normalized.posted_at,
        raw_job.raw_api_response,
        company.platform,
        settings=settings,
    )
    if posted_at is not None:
        normalized.posted_at = posted_at
    if verdict != FreshnessVerdict.STALE:
        return False

    await _emit_stale_rejection_event(
        db,
        normalized=normalized,
        company=company,
        queue_row=queue_row,
        posted_at=posted_at,
        stage="post_enrichment",
    )
    if batch_item is not None:
        batch_item.status = "failed"
        batch_item.failure_reason = FailureReason.STALE_POSTING
        batch_item.last_error = "Job posting date exceeds freshness window after enrichment."
    await purge_normalized_jobs(
        db,
        [
            PurgeTarget(
                id=normalized.id,
                raw_job_id=normalized.raw_job_id,
                job_archive_id=normalized.job_archive_id,
            )
        ],
    )
    return True


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
    def __init__(
        self,
        settings: Settings,
        *,
        worker_id: int,
        worker_count: int,
    ) -> None:
        self._settings = settings
        self._worker_id = worker_id
        self._worker_count = worker_count
        self._quota_paused = False
        self._stop = asyncio.Event()
        self._wake = asyncio.Event()

    def stop(self) -> None:
        self._stop.set()
        self._wake.set()

    def wake(self) -> None:
        self._wake.set()

    def pause_for_daily_quota(self, _message: str) -> None:
        self._quota_paused = True

    async def _sleep_until_stop(self, seconds: float) -> bool:
        """Sleep up to `seconds`. Returns True if stop was signaled."""
        if self._stop.is_set():
            return True
        try:
            await asyncio.wait_for(self._stop.wait(), timeout=seconds)
            return True
        except asyncio.TimeoutError:
            return False

    async def _wait_idle(self, timeout: float) -> bool:
        """Wait for wake, stop, or timeout. Returns True if stop was signaled."""
        if self._stop.is_set():
            return True
        wake_task = asyncio.create_task(self._wake.wait())
        stop_task = asyncio.create_task(self._stop.wait())
        try:
            done, pending = await asyncio.wait(
                [wake_task, stop_task],
                timeout=timeout,
                return_when=asyncio.FIRST_COMPLETED,
            )
            return stop_task in done
        finally:
            for task in pending:
                task.cancel()
            await asyncio.gather(wake_task, stop_task, return_exceptions=True)

    async def run_forever(self) -> None:
        while not self._stop.is_set():
            if self._quota_paused:
                if await self._sleep_until_stop(30.0):
                    break
                continue
            batches_processed = 0
            try:
                async with AsyncSessionLocal() as db:
                    processed, batches_processed = await process_enrichment_window(
                        db=db,
                        settings=self._settings,
                        worker_id=self._worker_id,
                        worker_count=self._worker_count,
                        on_daily_quota_exhausted=self.pause_for_daily_quota,
                        stop_event=self._stop,
                    )
            except asyncio.CancelledError:
                raise
            except Exception:
                processed = 0

            if self._stop.is_set():
                break

            if batches_processed > 0:
                if await self._sleep_until_stop(float(self._settings.enrichment_window_seconds)):
                    break
                continue

            self._wake.clear()
            if await self._wait_idle(2.0):
                break


class EnrichmentWorkerPool:
    def __init__(self, settings: Optional[Settings] = None) -> None:
        base = settings or get_settings()
        keys = base.gemini_api_keys_list()
        if not keys:
            self.worker_count = 0
            self.workers: list[EnrichmentWorker] = []
            return
        worker_count = base.resolved_enrichment_worker_count()
        self.worker_count = worker_count
        self.workers = [
            EnrichmentWorker(
                base.worker_settings(api_key),
                worker_id=worker_id,
                worker_count=worker_count,
            )
            for worker_id, api_key in enumerate(keys[:worker_count])
        ]

    def wake(self) -> None:
        for worker in self.workers:
            worker.wake()

    def stop(self) -> None:
        for worker in self.workers:
            worker.stop()


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
            normalized.is_active = False
            normalized.processing_state = ProcessingState.PARTIAL_SUCCESS
            normalized.failure_reason = FailureReason.MISSING_REQUIRED_FIELDS
            normalized.last_failure_at = _utcnow()
            db.add(normalized)
            continue
        company = await db.get(Company, normalized.company_id)
        if company is None:
            queue_row.status = "failed"
            queue_row.last_failure_reason = FailureReason.MISSING_REQUIRED_FIELDS
            queue_row.last_error = "Company not found."
            continue
        if await _purge_if_stale_before_enrichment(
            db,
            normalized=normalized,
            raw_job=raw_job,
            company=company,
            queue_row=queue_row,
            settings=settings,
        ):
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


def _queue_wait_started_at(queue_row: EnrichmentQueue) -> datetime:
    if queue_row.attempt_count == 0:
        return queue_row.created_at
    return queue_row.updated_at


def _batch_is_ready(batch: list[WorkItem], settings: Settings, now: datetime) -> bool:
    if not settings.enrichment_min_batch_enabled:
        return True
    min_size = settings.enrichment_min_batch_size
    if min_size <= 1:
        return True
    if len(batch) >= min_size:
        return True
    bypass = timedelta(seconds=settings.enrichment_min_batch_bypass_wait_seconds)
    return any(now - _queue_wait_started_at(row.queue_row) >= bypass for row in batch)


def _partition_ready_batches(
    batches: list[list[WorkItem]],
    settings: Settings,
    now: datetime,
) -> tuple[list[list[WorkItem]], list[WorkItem]]:
    ready: list[list[WorkItem]] = []
    held: list[WorkItem] = []
    for batch in batches:
        if _batch_is_ready(batch, settings, now):
            ready.append(batch)
        else:
            held.extend(batch)
    return ready, held


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


def _jd_section_fields(enrichment: BatchJobEnrichment) -> dict[str, list[str]]:
    return {
        "responsibilities": list(enrichment.responsibilities),
        "required_qualifications": list(enrichment.required_qualifications),
        "preferred_qualifications": list(enrichment.preferred_qualifications),
        "benefits": list(enrichment.benefits),
    }


def _apply_enrichment_to_job(
    normalized: NormalizedJob,
    enrichment: BatchJobEnrichment,
    settings: Settings,
) -> None:
    normalized.seniority = enrichment.seniority
    normalized.experience_tier = enrichment.experience_tier
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
    normalized.job_domain = enrichment.job_domain
    normalized.job_secondary_domain = enrichment.job_secondary_domain
    normalized.requires_clearance = enrichment.requires_clearance
    normalized.role_intent = enrichment.role_intent
    sections = _jd_section_fields(enrichment)
    normalized.responsibilities = sections["responsibilities"]
    normalized.required_qualifications = sections["required_qualifications"]
    normalized.preferred_qualifications = sections["preferred_qualifications"]
    normalized.benefits = sections["benefits"]
    normalized.retrieval_pools = assign_validated_retrieval_pools(
        normalized.normalized_roles,
        normalized.is_internship,
        normalized.is_new_grad,
        enrichment.job_domain,
        enrichment.job_secondary_domain,
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
    normalized.extraction_version = settings.extraction_version
    normalized.processing_state = ProcessingState.SUCCESS
    normalized.failure_reason = None
    normalized.last_failure_at = None


def _apply_waas_sponsorship_hint(normalized: NormalizedJob, raw_job: RawJob) -> None:
    if raw_job.platform != "workatastartup":
        return
    payload = raw_job.raw_api_response
    if not isinstance(payload, dict):
        return
    visa = payload.get("visa_sponsorship")
    if visa is True:
        normalized.sponsorship_status = "yes"
        normalized.sponsorship_confidence = "high"
    elif visa is False:
        normalized.sponsorship_status = "no"
        normalized.sponsorship_confidence = "high"


def _recommendation_fields_from_enrichment(
    normalized: NormalizedJob,
    enrichment: BatchJobEnrichment,
    settings: Settings,
) -> dict:
    normalized_roles = list(enrichment.normalized_roles)
    retrieval_pools = assign_validated_retrieval_pools(
        normalized_roles,
        enrichment.is_internship,
        enrichment.is_new_grad,
        enrichment.job_domain,
        enrichment.job_secondary_domain,
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
        "job_domain": enrichment.job_domain,
        "job_secondary_domain": enrichment.job_secondary_domain,
        "requires_clearance": enrichment.requires_clearance,
        "role_intent": enrichment.role_intent,
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


def _mark_for_provider_capacity_error(
    queue_row: EnrichmentQueue,
    settings: Settings,
    *,
    error_message: str,
    daily_quota: bool,
) -> None:
    """Re-queue after Gemini quota/rate-limit errors instead of permanent failure."""
    queue_row.last_failure_reason = FailureReason.TOKEN_LIMIT_EXCEEDED
    queue_row.last_error = error_message
    if daily_quota:
        queue_row.status = "queued"
        queue_row.next_retry_at = None
        return
    queue_row.attempt_count += 1
    if queue_row.attempt_count > settings.enrichment_max_retries:
        queue_row.status = "failed"
        queue_row.last_failure_reason = "retry_limit_exceeded"
        return
    queue_row.status = "cooldown"
    queue_row.next_retry_at = _utcnow() + timedelta(seconds=settings.enrichment_cooldown_seconds)


def _update_normalized_after_batch_error(
    normalized: NormalizedJob,
    queue_row: EnrichmentQueue,
    failure_reason: str,
) -> None:
    normalized.failure_reason = failure_reason
    normalized.last_failure_at = _utcnow()
    if queue_row.status == "failed":
        normalized.processing_state = ProcessingState.PARTIAL_SUCCESS
        return
    if normalized.processing_state == ProcessingState.SUCCESS:
        return
    if queue_row.status == "queued":
        normalized.processing_state = ProcessingState.PENDING
        return
    normalized.processing_state = ProcessingState.PARTIAL_SUCCESS


async def _process_batch(
    db: AsyncSession,
    settings: Settings,
    batch_items: list[WorkItem],
    source: str,
    *,
    on_daily_quota_exhausted: Callable[[str], None] | None = None,
) -> None:
    started = _utcnow()
    enriched_for_notifications: list[tuple[UUID, UUID]] = []
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

    payload_jobs = [
        build_batch_job_payload(
            job_id=str(row.normalized.id),
            text=row.clean_text,
            title=row.normalized.title,
            employment_type=row.normalized.employment_type,
        )
        for row in batch_items
    ]
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
                        experience_tier=DEFAULT_ENRICHMENT.experience_tier,
                        is_internship=DEFAULT_ENRICHMENT.is_internship,
                        is_new_grad=DEFAULT_ENRICHMENT.is_new_grad,
                        sponsorship_status=DEFAULT_ENRICHMENT.sponsorship_status,
                        sponsorship_confidence=DEFAULT_ENRICHMENT.sponsorship_confidence,
                        remote_type=DEFAULT_ENRICHMENT.remote_type,
                        tech_stack=DEFAULT_ENRICHMENT.tech_stack,
                        skills=DEFAULT_ENRICHMENT.skills,
                        responsibilities=DEFAULT_ENRICHMENT.responsibilities,
                        required_qualifications=DEFAULT_ENRICHMENT.required_qualifications,
                        preferred_qualifications=DEFAULT_ENRICHMENT.preferred_qualifications,
                        benefits=DEFAULT_ENRICHMENT.benefits,
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
                        experience_tier=enrichment.experience_tier,
                        is_internship=enrichment.is_internship,
                        is_new_grad=enrichment.is_new_grad,
                        sponsorship_status=enrichment.sponsorship_status,
                        sponsorship_confidence=enrichment.sponsorship_confidence,
                        remote_type=enrichment.remote_type,
                        tech_stack=enrichment.tech_stack,
                        skills=enrichment.skills,
                        **_jd_section_fields(enrichment),
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                        latency_ms=result.latency_ms,
                        status="failed",
                        failure_reason=FailureReason.EMPTY_SKILL_EXTRACTION,
                    )
                )
                continue

            _apply_enrichment_to_job(row.normalized, enrichment, settings)
            _apply_waas_sponsorship_hint(row.normalized, row.raw_job)
            if row.normalized.job_archive_id is not None:
                await update_job_archive_after_enrichment(
                    db,
                    row.normalized.job_archive_id,
                    seniority=enrichment.seniority,
                    experience_tier=enrichment.experience_tier,
                    normalized_roles=list(enrichment.normalized_roles),
                    job_capabilities=list(enrichment.job_capabilities),
                    skills=list(enrichment.skills),
                    tech_stack=list(enrichment.tech_stack),
                    remote_type=enrichment.remote_type,
                    salary_min=enrichment.salary_min,
                    salary_max=enrichment.salary_max,
                    job_domain=enrichment.job_domain,
                    job_secondary_domain=enrichment.job_secondary_domain,
                    requires_clearance=enrichment.requires_clearance,
                    role_intent=enrichment.role_intent,
                )
            recommendation_fields = _recommendation_fields_from_enrichment(row.normalized, enrichment, settings)
            db.add(
                JobEnrichment(
                    normalized_job_id=row.normalized.id,
                    raw_job_id=row.raw_job.id,
                    enrichment_batch_id=batch.id,
                    llm_provider=settings.llm_provider,
                    llm_model=settings.gemini_model if settings.llm_provider == "gemini" else None,
                    extraction_version=settings.extraction_version,
                    seniority=enrichment.seniority,
                    experience_tier=enrichment.experience_tier,
                    is_internship=enrichment.is_internship,
                    is_new_grad=enrichment.is_new_grad,
                    sponsorship_status=enrichment.sponsorship_status,
                    sponsorship_confidence=enrichment.sponsorship_confidence,
                    remote_type=enrichment.remote_type,
                    tech_stack=enrichment.tech_stack,
                    skills=enrichment.skills,
                    **_jd_section_fields(enrichment),
                    **fields_for_job_enrichment_record(recommendation_fields),
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    latency_ms=result.latency_ms,
                    status="success",
                    failure_reason=None,
                )
            )
            if await _purge_if_stale_after_enrichment(
                db,
                normalized=row.normalized,
                raw_job=row.raw_job,
                company=row.company,
                queue_row=row.queue_row,
                settings=settings,
                batch_item=item,
            ):
                continue

            row.queue_row.status = "completed"
            row.queue_row.next_retry_at = None
            row.queue_row.last_failure_reason = None
            row.queue_row.last_error = None
            if item is not None:
                item.status = "success"
                item.actual_input_tokens = input_tokens
                item.actual_output_tokens = output_tokens
            if row.normalized.processing_state == ProcessingState.SUCCESS:
                enriched_for_notifications.append((row.normalized.id, row.normalized.company_id))

        batch.status = "completed"
    except Exception as exc:
        message = str(exc)
        daily_quota = _is_daily_quota_exhausted(message)
        retryable = _is_transient_rate_limit(message)
        schema_error = _is_schema_validation_error(message)
        provider_capacity = _is_provider_capacity_error(message)
        if daily_quota and on_daily_quota_exhausted is not None:
            on_daily_quota_exhausted(message)
        if (
            len(batch_items) > 1
            and not provider_capacity
            and schema_error
        ):
            batch.status = "failed"
            batch.failure_reason = FailureReason.LLM_SCHEMA_MISMATCH
            batch.last_error = f"Batch split to singles after: {message}"
            batch.completed_at = _utcnow()
            batch.latency_ms = int((batch.completed_at - started).total_seconds() * 1000)
            for row in batch_items:
                row.queue_row.status = "queued"
            await db.flush()
            for row in batch_items:
                await _process_batch(
                    db=db,
                    settings=settings,
                    batch_items=[row],
                    source="worker_single_fallback",
                    on_daily_quota_exhausted=on_daily_quota_exhausted,
                )
            return
        items = (
            await db.scalars(select(EnrichmentBatchItem).where(EnrichmentBatchItem.batch_id == batch.id))
        ).all()
        items_by_job = {item.queue_id: item for item in items}
        for row in batch_items:
            if daily_quota and settings.enrichment_stop_on_daily_quota:
                _mark_quota_blocked(queue_row=row.queue_row, error_message=message)
            elif provider_capacity:
                _mark_for_provider_capacity_error(
                    queue_row=row.queue_row,
                    settings=settings,
                    error_message=message,
                    daily_quota=daily_quota,
                )
            elif schema_error:
                _mark_for_retry(
                    queue_row=row.queue_row,
                    settings=settings,
                    failure_reason=FailureReason.LLM_SCHEMA_MISMATCH,
                    error_message=message,
                )
            else:
                row.queue_row.status = "failed"
                row.queue_row.last_failure_reason = FailureReason.LLM_SCHEMA_MISMATCH
                row.queue_row.last_error = message
            failure_reason = row.queue_row.last_failure_reason or FailureReason.LLM_SCHEMA_MISMATCH
            _update_normalized_after_batch_error(row.normalized, row.queue_row, failure_reason)
            db.add(
                JobEnrichment(
                    normalized_job_id=row.normalized.id,
                    raw_job_id=row.raw_job.id,
                    enrichment_batch_id=batch.id,
                    llm_provider=settings.llm_provider,
                    llm_model=settings.gemini_model if settings.llm_provider == "gemini" else None,
                    extraction_version=settings.extraction_version,
                    seniority=DEFAULT_ENRICHMENT.seniority,
                    experience_tier=DEFAULT_ENRICHMENT.experience_tier,
                    is_internship=DEFAULT_ENRICHMENT.is_internship,
                    is_new_grad=DEFAULT_ENRICHMENT.is_new_grad,
                    sponsorship_status=DEFAULT_ENRICHMENT.sponsorship_status,
                    sponsorship_confidence=DEFAULT_ENRICHMENT.sponsorship_confidence,
                    remote_type=DEFAULT_ENRICHMENT.remote_type,
                    tech_stack=DEFAULT_ENRICHMENT.tech_stack,
                    skills=DEFAULT_ENRICHMENT.skills,
                    responsibilities=DEFAULT_ENRICHMENT.responsibilities,
                    required_qualifications=DEFAULT_ENRICHMENT.required_qualifications,
                    preferred_qualifications=DEFAULT_ENRICHMENT.preferred_qualifications,
                    benefits=DEFAULT_ENRICHMENT.benefits,
                    input_tokens=0,
                    output_tokens=0,
                    latency_ms=0,
                    status="failed",
                    failure_reason=failure_reason,
                )
            )
            item = items_by_job.get(row.queue_row.id)
            if item is not None:
                item.status = "failed"
                item.failure_reason = failure_reason
                item.last_error = message
        batch.status = "failed"
        if provider_capacity or (daily_quota and settings.enrichment_stop_on_daily_quota):
            batch.failure_reason = FailureReason.TOKEN_LIMIT_EXCEEDED
        elif schema_error:
            batch.failure_reason = FailureReason.LLM_SCHEMA_MISMATCH
        else:
            batch.failure_reason = FailureReason.LLM_SCHEMA_MISMATCH
        batch.last_error = message

    batch.completed_at = _utcnow()
    batch.latency_ms = int((batch.completed_at - started).total_seconds() * 1000)

    if batch.status == "completed" and settings.company_watch_events_enabled:
        await enqueue_notification_job_events(db, enriched_for_notifications)


async def cleanup_orphan_enrichment_queue(db: AsyncSession) -> dict[str, int]:
    """Remove queue rows for missing jobs and deactivate normalized jobs without raw payloads."""
    deactivated = (
        await db.execute(
            text(
                """
                UPDATE normalized_jobs nj
                SET is_active = false,
                    processing_state = 'partial_success',
                    failure_reason = 'missing_required_fields',
                    last_failure_at = NOW()
                WHERE nj.is_active
                  AND NOT EXISTS (
                    SELECT 1 FROM raw_jobs rj WHERE rj.id = nj.raw_job_id
                  )
                """
            )
        )
    ).rowcount
    deleted_queue = (
        await db.execute(
            text(
                """
                DELETE FROM enrichment_queue eq
                WHERE NOT EXISTS (
                    SELECT 1 FROM normalized_jobs nj WHERE nj.id = eq.normalized_job_id
                  )
                  OR NOT EXISTS (
                    SELECT 1
                    FROM normalized_jobs nj
                    JOIN raw_jobs rj ON rj.id = nj.raw_job_id
                    WHERE nj.id = eq.normalized_job_id
                  )
                """
            )
        )
    ).rowcount
    await db.commit()
    return {"deactivated_jobs": deactivated, "deleted_queue_rows": deleted_queue}


async def reset_stuck_queue_rows(db: AsyncSession) -> int:
    """Re-queue failed, quota_blocked, and cooldown rows for active jobs."""
    result = await db.execute(
        text(
            """
            UPDATE enrichment_queue eq
            SET status = 'queued',
                attempt_count = 0,
                next_retry_at = NULL,
                last_error = NULL,
                last_failure_reason = NULL
            FROM normalized_jobs nj
            JOIN raw_jobs rj ON rj.id = nj.raw_job_id
            WHERE eq.normalized_job_id = nj.id
              AND nj.is_active
              AND eq.status IN ('failed', 'quota_blocked', 'cooldown')
            """
        )
    )
    await db.commit()
    return int(result.rowcount or 0)


async def process_enrichment_window(
    db: AsyncSession,
    *,
    settings: Optional[Settings] = None,
    worker_id: int = 0,
    worker_count: int = 1,
    on_daily_quota_exhausted: Callable[[str], None] | None = None,
    stop_event: asyncio.Event | None = None,
) -> tuple[int, int]:
    settings = settings or get_settings()
    now = _utcnow()
    partition = _partition_filter(worker_id, worker_count)
    eligible = and_(
        EnrichmentQueue.status.in_(["queued", "cooldown"]),
        or_(EnrichmentQueue.next_retry_at.is_(None), EnrichmentQueue.next_retry_at <= now),
        partition,
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

    batches, held_for_min_size = _partition_ready_batches(batches, settings=settings, now=now)
    for row in held_for_min_size:
        row.queue_row.status = "queued"

    if not batches:
        await db.commit()
        return 0, 0

    rpm_cap = max(settings.enrichment_llm_max_rpm, 1)
    batches = batches[: min(settings.enrichment_max_batches_per_window, rpm_cap)]
    processed_jobs = 0
    for idx, batch in enumerate(batches):
        if stop_event is not None and stop_event.is_set():
            break
        if idx > 0:
            if stop_event is not None:
                try:
                    await asyncio.wait_for(stop_event.wait(), timeout=settings.enrichment_batch_interval_seconds)
                    break
                except asyncio.TimeoutError:
                    pass
            else:
                await asyncio.sleep(settings.enrichment_batch_interval_seconds)
        await _process_batch(
            db=db,
            settings=settings,
            batch_items=batch,
            source=f"worker_{worker_id}",
            on_daily_quota_exhausted=on_daily_quota_exhausted,
        )
        processed_jobs += len(batch)
        await db.commit()
    return processed_jobs, len(batches)


async def process_job_immediately(
    db: AsyncSession,
    normalized_job_id: UUID,
    settings: Optional[Settings] = None,
) -> dict[str, str]:
    settings = (settings or get_settings()).primary_enrichment_settings()
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

    if await _purge_if_stale_before_enrichment(
        db,
        normalized=normalized,
        raw_job=raw_job,
        company=company,
        queue_row=queue_row,
        settings=settings,
    ):
        await db.commit()
        return {"job_id": str(normalized_job_id), "status": "purged_stale"}

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


_ENRICHMENT_WORKER_POOL: Optional[EnrichmentWorkerPool] = None


def get_enrichment_worker_pool(settings: Optional[Settings] = None) -> EnrichmentWorkerPool:
    global _ENRICHMENT_WORKER_POOL
    if _ENRICHMENT_WORKER_POOL is None:
        _ENRICHMENT_WORKER_POOL = EnrichmentWorkerPool(settings=settings)
    return _ENRICHMENT_WORKER_POOL


def get_enrichment_worker(settings: Optional[Settings] = None) -> EnrichmentWorkerPool:
    return get_enrichment_worker_pool(settings=settings)
