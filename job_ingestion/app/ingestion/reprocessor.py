from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.ingestion.constants import EventCategory, EventSeverity, EventType, FailureReason, ProcessingState
from app.ingestion.events import write_event
from app.ingestion.extractor.deterministic import extract_deterministic_fields
from app.ingestion.extractor.llm import DEFAULT_ENRICHMENT, enrich_job_text
from app.ingestion.extractor.text_cleaner import clean_job_description
from app.ingestion.job_freshness import FreshnessVerdict, classify_posted_at
from app.ingestion.job_purge import PurgeTarget, purge_normalized_jobs
from app.ingestion.recommendation_fields import (
    assign_validated_retrieval_pools,
    compute_opportunity_score,
    fields_for_job_enrichment_record,
)
from app.llm.factory import get_llm_provider
from app.models.company import Company
from app.models.job_enrichment import JobEnrichment
from app.models.normalized_job import NormalizedJob
from app.models.raw_job import RawJob
from app.schemas.reprocessing import ReprocessingFilters


@dataclass
class ReprocessingResult:
    matched_jobs: int
    processed_jobs: int
    success_count: int
    failed_count: int
    dry_run: bool


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


async def reprocess_jobs(
    db: AsyncSession,
    settings: Settings,
    filters: ReprocessingFilters,
    target_version: str,
    dry_run: bool,
) -> ReprocessingResult:
    query: Select[tuple[NormalizedJob, Company]] = (
        select(NormalizedJob, Company).join(Company, Company.id == NormalizedJob.company_id)
    )
    if filters.processing_state:
        query = query.where(NormalizedJob.processing_state.in_(filters.processing_state))
    if filters.extraction_version:
        query = query.where(NormalizedJob.extraction_version == filters.extraction_version)
    if filters.company_id:
        query = query.where(NormalizedJob.company_id == UUID(filters.company_id))
    if filters.platform:
        query = query.where(Company.platform == filters.platform)

    rows = (await db.execute(query)).all()
    matched = len(rows)
    if dry_run:
        return ReprocessingResult(
            matched_jobs=matched,
            processed_jobs=0,
            success_count=0,
            failed_count=0,
            dry_run=True,
        )

    llm_provider = None
    try:
        llm_provider = get_llm_provider(settings)
    except Exception:  # noqa: BLE001
        llm_provider = None

    processed = 0
    success_count = 0
    failed_count = 0

    for normalized, company in rows:
        raw_job = await db.get(RawJob, normalized.raw_job_id)
        if raw_job is None:
            failed_count += 1
            continue
        processed += 1
        html = raw_job.raw_html or (raw_job.raw_api_response or {}).get("content", "")
        try:
            extracted = extract_deterministic_fields(raw_job.raw_api_response, platform=company.platform)
            normalized.title = extracted.get("title") or normalized.title
            normalized.location = extracted.get("location")
            normalized.department = extracted.get("department")
            normalized.posting_url = extracted.get("posting_url")
            normalized.posted_at = extracted.get("posted_at")
            normalized.employment_type = extracted.get("employment_type")
        except Exception:  # noqa: BLE001
            normalized.processing_state = ProcessingState.EXTRACTION_FAILED
            normalized.failure_reason = FailureReason.EXTRACTION_EXCEPTION
            normalized.last_failure_at = _utcnow()
            failed_count += 1
            await write_event(
                db,
                event_type=EventType.MALFORMED_SOURCE_RESPONSE,
                category=EventCategory.SOURCE,
                severity=EventSeverity.WARNING,
                platform=company.platform,
                company_id=company.id,
                normalized_job_id=normalized.id,
            )
            continue

        if classify_posted_at(normalized.posted_at, settings=settings) == FreshnessVerdict.STALE:
            await write_event(
                db,
                event_type=EventType.JOB_REJECTED_STALE,
                category=EventCategory.ENRICHMENT,
                severity=EventSeverity.INFO,
                platform=company.platform,
                company_id=company.id,
                normalized_job_id=normalized.id,
                metadata={
                    "stage": "reprocessing",
                    "external_job_id": normalized.external_job_id,
                    "posted_at": normalized.posted_at.isoformat() if normalized.posted_at else None,
                },
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
            failed_count += 1
            continue

        clean_text = clean_job_description(html)
        if llm_provider is None:
            enrichment = DEFAULT_ENRICHMENT
            failure_reason = FailureReason.LLM_EMPTY_RESPONSE
            status = "failed"
            input_tokens = 0
            output_tokens = 0
            latency_ms = 0
        else:
            try:
                llm_result = await enrich_job_text(
                    llm_provider,
                    clean_text,
                    title=normalized.title,
                    employment_type=normalized.employment_type,
                )
                enrichment = llm_result.output
                failure_reason = None
                status = "success"
                input_tokens = llm_result.input_tokens
                output_tokens = llm_result.output_tokens
                latency_ms = llm_result.latency_ms
            except Exception:  # noqa: BLE001
                enrichment = DEFAULT_ENRICHMENT
                failure_reason = FailureReason.LLM_SCHEMA_MISMATCH
                status = "failed"
                input_tokens = 0
                output_tokens = 0
                latency_ms = 0

        recommendation_fields: dict = {}
        if status == "success":
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
            recommendation_fields = {
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

        db.add(
            JobEnrichment(
                normalized_job_id=normalized.id,
                raw_job_id=raw_job.id,
                llm_provider=settings.llm_provider,
                llm_model=settings.gemini_model if settings.llm_provider == "gemini" else None,
                extraction_version=target_version,
                seniority=enrichment.seniority,
                is_internship=enrichment.is_internship,
                is_new_grad=enrichment.is_new_grad,
                sponsorship_status=enrichment.sponsorship_status,
                sponsorship_confidence=enrichment.sponsorship_confidence,
                remote_type=enrichment.remote_type,
                tech_stack=enrichment.tech_stack,
                skills=enrichment.skills,
                **fields_for_job_enrichment_record(recommendation_fields),
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                latency_ms=latency_ms,
                status=status,
                failure_reason=failure_reason,
            )
        )

        normalized.extraction_version = target_version
        if status == "success":
            normalized.processing_state = ProcessingState.SUCCESS
            normalized.failure_reason = None
            normalized.last_failure_at = None
            normalized.seniority = enrichment.seniority
            normalized.is_internship = enrichment.is_internship
            normalized.is_new_grad = enrichment.is_new_grad
            normalized.sponsorship_status = enrichment.sponsorship_status
            normalized.sponsorship_confidence = enrichment.sponsorship_confidence
            normalized.remote_type = enrichment.remote_type
            normalized.tech_stack = enrichment.tech_stack
            normalized.skills = enrichment.skills
            normalized.normalized_roles = recommendation_fields.get("normalized_roles", [])
            normalized.job_capabilities = recommendation_fields.get("job_capabilities", [])
            normalized.application_effort = recommendation_fields.get("application_effort")
            normalized.retrieval_pools = recommendation_fields.get("retrieval_pools", [])
            normalized.job_domain = recommendation_fields.get("job_domain")
            normalized.job_secondary_domain = recommendation_fields.get("job_secondary_domain")
            normalized.requires_clearance = recommendation_fields.get("requires_clearance", False)
            normalized.role_intent = recommendation_fields.get("role_intent")
            normalized.salary_min = recommendation_fields.get("salary_min")
            normalized.salary_max = recommendation_fields.get("salary_max")
            normalized.opportunity_score = recommendation_fields.get("opportunity_score")
            normalized.opportunity_score_computed_at = recommendation_fields.get("opportunity_score_computed_at")
            success_count += 1
        else:
            normalized.processing_state = ProcessingState.PARTIAL_SUCCESS
            normalized.failure_reason = failure_reason
            normalized.last_failure_at = _utcnow()
            failed_count += 1
            await write_event(
                db,
                event_type=EventType.LLM_EXTRACTION_FAILED,
                category=EventCategory.ENRICHMENT,
                severity=EventSeverity.WARNING,
                platform=company.platform,
                company_id=company.id,
                normalized_job_id=normalized.id,
                metadata={"source": "reprocessing", "reason": failure_reason},
            )

    await write_event(
        db,
        event_type="reprocessing_completed",
        category=EventCategory.PIPELINE,
        severity=EventSeverity.INFO,
        metadata={
            "matched_jobs": matched,
            "processed_jobs": processed,
            "success_count": success_count,
            "failed_count": failed_count,
            "target_version": target_version,
        },
    )
    await db.commit()
    return ReprocessingResult(
        matched_jobs=matched,
        processed_jobs=processed,
        success_count=success_count,
        failed_count=failed_count,
        dry_run=False,
    )
