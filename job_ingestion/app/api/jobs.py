from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.ingestion.constants import EventCategory, EventSeverity, EventType, ProcessingState
from app.ingestion.enrichment_worker import process_job_immediately
from app.ingestion.events import write_event
from app.ingestion.job_archive_sync import update_job_archive_from_normalized_fields
from app.models.company import Company
from app.models.job_enrichment import JobEnrichment
from app.models.normalized_job import NormalizedJob
from app.models.raw_job import RawJob
from app.schemas.enrichment import JobEnrichmentOut
from app.schemas.job import JobFlagIn, JobReviewPatchIn, NormalizedJobDetailOut, NormalizedJobOut

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=list[NormalizedJobOut])
async def list_jobs(
    processing_state: Optional[str] = Query(default=None),
    platform: Optional[str] = Query(default=None),
    company_id: Optional[str] = Query(default=None),
    company: Optional[str] = Query(default=None),
    title: Optional[str] = Query(default=None),
    is_active: Optional[bool] = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    sort_by: str = Query(default="updated_at"),
    sort_dir: str = Query(default="desc"),
    db: AsyncSession = Depends(get_db),
) -> list[NormalizedJobOut]:
    stmt = select(NormalizedJob)
    if platform:
        stmt = stmt.join(Company, Company.id == NormalizedJob.company_id).where(Company.platform == platform)
    if processing_state:
        states = [item.strip() for item in processing_state.split(",") if item.strip()]
        if len(states) == 1:
            stmt = stmt.where(NormalizedJob.processing_state == states[0])
        elif states:
            stmt = stmt.where(NormalizedJob.processing_state.in_(states))
    if company_id:
        try:
            stmt = stmt.where(NormalizedJob.company_id == uuid.UUID(company_id))
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid company_id") from exc
    if company:
        stmt = stmt.where(NormalizedJob.company_name.ilike(f"%{company}%"))
    if title:
        stmt = stmt.where(
            or_(
                NormalizedJob.title.ilike(f"%{title}%"),
                NormalizedJob.description_preview.ilike(f"%{title}%"),
            )
        )
    if is_active is not None:
        stmt = stmt.where(NormalizedJob.is_active == is_active)

    sort_field_map = {
        "updated_at": NormalizedJob.updated_at,
        "last_seen_at": NormalizedJob.last_seen_at,
        "extracted_at": NormalizedJob.extracted_at,
        "title": NormalizedJob.title,
        "company_name": NormalizedJob.company_name,
        "processing_state": NormalizedJob.processing_state,
    }
    sort_column = sort_field_map.get(sort_by, NormalizedJob.updated_at)
    if sort_dir.lower() == "asc":
        stmt = stmt.order_by(sort_column.asc())
    else:
        stmt = stmt.order_by(sort_column.desc())
    stmt = stmt.offset(offset).limit(limit)

    rows = (await db.scalars(stmt)).all()
    return [_serialize_job_out(row) for row in rows]


@router.get("/{job_id}", response_model=NormalizedJobDetailOut)
async def get_job(job_id: str, db: AsyncSession = Depends(get_db)) -> NormalizedJobDetailOut:
    row = await _get_job_or_404(job_id=job_id, db=db)
    enrichments = await _get_job_enrichments(row=row, db=db)
    return _serialize_job_detail(row=row, enrichment_out=enrichments)


@router.get("/{job_id}/raw")
async def get_job_raw(job_id: str, db: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    try:
        job_uuid = uuid.UUID(job_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid job id") from exc

    normalized = await db.get(NormalizedJob, job_uuid)
    if normalized is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    raw_row = await db.get(RawJob, normalized.raw_job_id)
    if raw_row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Raw payload not found")
    return {
        "normalized_job_id": str(normalized.id),
        "raw_job_id": str(raw_row.id),
        "platform": raw_row.platform,
        "external_job_id": raw_row.external_job_id,
        "fetch_timestamp": raw_row.fetch_timestamp.isoformat(),
        "raw_html": raw_row.raw_html,
        "raw_api_response": raw_row.raw_api_response,
    }


@router.post("/{job_id}/enrich-now")
async def enrich_job_now(job_id: str, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    try:
        job_uuid = uuid.UUID(job_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid job id") from exc

    settings = get_settings()
    try:
        result = await process_job_immediately(db=db, normalized_job_id=job_uuid, settings=settings)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{job_id}", response_model=NormalizedJobDetailOut)
async def patch_job_for_review(
    job_id: str,
    payload: JobReviewPatchIn,
    db: AsyncSession = Depends(get_db),
) -> NormalizedJobDetailOut:
    row = await _get_job_or_404(job_id=job_id, db=db)

    patch_data = payload.model_dump(exclude={"comment"}, exclude_none=True)
    for key, value in patch_data.items():
        setattr(row, key, value)
    row.processing_state = ProcessingState.MANUALLY_CORRECTED
    row.last_manual_review_at = datetime.now(timezone.utc)
    row.last_review_comment = payload.comment

    if row.job_archive_id is not None:
        await update_job_archive_from_normalized_fields(db, row.job_archive_id, row)

    await write_event(
        db=db,
        event_type=EventType.REVIEWER_EDITED_JOB,
        category=EventCategory.REVIEW,
        severity=EventSeverity.INFO,
        platform=(await _get_job_platform(row.company_id, db)),
        company_id=row.company_id,
        normalized_job_id=row.id,
        metadata={"comment": payload.comment},
    )
    await db.commit()
    await db.refresh(row)
    enrichments = await _get_job_enrichments(row=row, db=db)
    return _serialize_job_detail(row=row, enrichment_out=enrichments)


@router.post("/{job_id}/flag", response_model=NormalizedJobDetailOut)
async def flag_job_for_review(
    job_id: str,
    payload: JobFlagIn,
    db: AsyncSession = Depends(get_db),
) -> NormalizedJobDetailOut:
    row = await _get_job_or_404(job_id=job_id, db=db)
    row.processing_state = ProcessingState.REQUIRES_REVIEW
    row.last_manual_review_at = datetime.now(timezone.utc)
    row.last_review_comment = payload.comment

    await write_event(
        db=db,
        event_type=EventType.JOB_MARKED_REQUIRES_REVIEW,
        category=EventCategory.REVIEW,
        severity=EventSeverity.WARNING,
        platform=(await _get_job_platform(row.company_id, db)),
        company_id=row.company_id,
        normalized_job_id=row.id,
        metadata={"comment": payload.comment},
    )
    await db.commit()
    await db.refresh(row)
    enrichments = await _get_job_enrichments(row=row, db=db)
    return _serialize_job_detail(row=row, enrichment_out=enrichments)


async def _get_job_or_404(job_id: str, db: AsyncSession) -> NormalizedJob:
    try:
        job_uuid = uuid.UUID(job_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid job id") from exc
    row = await db.get(NormalizedJob, job_uuid)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return row


async def _get_job_enrichments(row: NormalizedJob, db: AsyncSession) -> list[JobEnrichmentOut]:
    enrichments = (
        await db.scalars(
            select(JobEnrichment)
            .where(JobEnrichment.normalized_job_id == row.id)
            .order_by(JobEnrichment.created_at.desc())
        )
    ).all()
    return [
        JobEnrichmentOut(
            id=str(e.id),
            status=e.status,
            failure_reason=e.failure_reason,
            llm_provider=e.llm_provider,
            llm_model=e.llm_model,
            extraction_version=e.extraction_version,
            seniority=e.seniority,
            experience_tier=e.experience_tier,
            is_internship=e.is_internship,
            is_new_grad=e.is_new_grad,
            sponsorship_status=e.sponsorship_status,
            sponsorship_confidence=e.sponsorship_confidence,
            remote_type=e.remote_type,
            tech_stack=e.tech_stack,
            skills=e.skills,
            required_skills=e.required_skills,
            preferred_skills=e.preferred_skills,
            responsibilities=e.responsibilities,
            required_qualifications=e.required_qualifications,
            preferred_qualifications=e.preferred_qualifications,
            benefits=e.benefits,
            normalized_roles=e.normalized_roles,
            job_capabilities=e.job_capabilities,
            application_effort=e.application_effort,
            retrieval_pools=e.retrieval_pools,
            salary_min=e.salary_min,
            salary_max=e.salary_max,
            opportunity_score=e.opportunity_score,
            opportunity_score_computed_at=e.opportunity_score_computed_at,
            input_tokens=e.input_tokens,
            output_tokens=e.output_tokens,
            latency_ms=e.latency_ms,
            created_at=e.created_at,
        )
        for e in enrichments
    ]


async def _get_job_platform(company_id: uuid.UUID, db: AsyncSession) -> Optional[str]:
    company = await db.get(Company, company_id)
    return company.platform if company else None


def _serialize_job_out(row: NormalizedJob) -> NormalizedJobOut:
    return NormalizedJobOut(
        id=str(row.id),
        external_job_id=row.external_job_id,
        title=row.title,
        company_name=row.company_name,
        location=row.location,
        department=row.department,
        posting_url=row.posting_url,
        description_preview=row.description_preview,
        is_active=row.is_active,
        processing_state=row.processing_state,
        failure_reason=row.failure_reason,
        last_seen_at=row.last_seen_at,
        last_manual_review_at=row.last_manual_review_at,
        extracted_at=row.extracted_at,
    )


def _serialize_job_detail(row: NormalizedJob, enrichment_out: list[JobEnrichmentOut]) -> NormalizedJobDetailOut:
    return NormalizedJobDetailOut(
        id=str(row.id),
        raw_job_id=str(row.raw_job_id),
        company_id=str(row.company_id),
        external_job_id=row.external_job_id,
        title=row.title,
        company_name=row.company_name,
        location=row.location,
        department=row.department,
        employment_type=row.employment_type,
        posting_url=row.posting_url,
        description_preview=row.description_preview,
        description_text=row.description_text,
        posted_at=row.posted_at,
        reference_at=row.reference_at,
        is_active=row.is_active,
        consecutive_misses=row.consecutive_misses,
        last_seen_at=row.last_seen_at,
        processing_state=row.processing_state,
        failure_reason=row.failure_reason,
        extraction_version=row.extraction_version,
        llm_provider=row.llm_provider,
        llm_model=row.llm_model,
        last_manual_review_at=row.last_manual_review_at,
        extracted_at=row.extracted_at,
        enrichments=enrichment_out,
    )
