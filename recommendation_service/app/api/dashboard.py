from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.database import get_db
from app.models.shared import NormalizedJob
from app.notification.ranker import deduplicate_ranked_jobs, rank_jobs, select_diversified_jobs
from app.notification.retrieval import (
    build_constraint_filters,
    query_jobs_in_pools,
)
from app.scoring.explainability import generate_explanations
from app.scoring.sponsorship import h1b_info_from_lookup
from app.schemas.applications import (
    UserApplicationOut,
    UserApplicationPatchIn,
    UserApplicationsResponse,
)
from app.schemas.dashboard import (
    CompanyEnrichmentOut,
    DashboardJobOut,
    DashboardJobsResponse,
    DashboardRecommendedJobOut,
    DashboardRecommendedJobsResponse,
    H1BSponsorshipInfo,
)
from app.services.applications import (
    applied_count_by_company,
    apply_to_job,
    get_user_applications,
    patch_application,
)
from app.services.company_enrichment_lookup import load_company_enrichment_lookup
from app.services.h1b_lookup import H1bLookup, load_h1b_summary_lookup
from app.services.h1b_pool_family import pool_family_from_roles
from app.services.profile_loader import UserProfile, load_user_profile
from app.services.recommended_cursor import decode_recommended_cursor, encode_recommended_cursor
from app.services.subscriptions import get_active_pools

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _h1b_sponsorship_for_job(
    job: NormalizedJob,
    h1b_lookup: H1bLookup | None,
) -> H1BSponsorshipInfo | None:
    if h1b_lookup is None:
        return None
    row = h1b_info_from_lookup(
        job.company_id,
        pool_family_from_roles(job.normalized_roles or []),
        h1b_lookup,
    )
    if row is None:
        return None
    return H1BSponsorshipInfo(
        pool_family=row.pool_family,
        total_lca_3yr=row.total_lca_3yr,
        approval_rate_3yr=row.approval_rate_3yr,
        is_top_sponsor=row.is_top_sponsor,
        years_covered=row.years_covered,
    )


def _canonical_posted_at(job: NormalizedJob):
    return job.reference_at or job.posted_at


def _job_to_out(
    job: NormalizedJob,
    *,
    h1b_sponsorship: H1BSponsorshipInfo | None = None,
    company_info: CompanyEnrichmentOut | None = None,
) -> DashboardJobOut:
    return DashboardJobOut(
        id=job.id,
        title=job.title,
        company_name=job.company_name,
        location=job.location,
        posting_url=job.posting_url,
        description_text=job.description_text,
        description_preview=job.description_preview,
        posted_at=_canonical_posted_at(job),
        remote_type=job.remote_type,
        application_effort=job.application_effort,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        opportunity_score=job.opportunity_score,
        retrieval_pools=job.retrieval_pools,
        normalized_roles=job.normalized_roles,
        job_capabilities=job.job_capabilities,
        tech_stack=job.tech_stack,
        skills=job.skills,
        seniority=job.seniority,
        experience_tier=job.experience_tier,
        responsibilities=list(job.responsibilities or []),
        required_qualifications=list(job.required_qualifications or []),
        preferred_qualifications=list(job.preferred_qualifications or []),
        benefits=list(job.benefits or []),
        sponsorship_status=job.sponsorship_status,
        sponsorship_confidence=job.sponsorship_confidence,
        requires_clearance=job.requires_clearance,
        requires_citizenship=job.requires_citizenship,
        h1b_sponsorship=h1b_sponsorship,
        company_info=company_info,
    )


def _needs_sponsorship_data(user_profile: UserProfile | None) -> bool:
    """H-1B company history is informational only; eligibility filtering uses explicit job flags."""
    return False


async def _load_job_enrichment_lookups(
    db: AsyncSession,
    jobs: list[NormalizedJob],
    *,
    needs_sponsorship: bool,
) -> tuple[H1bLookup | None, dict[uuid.UUID, CompanyEnrichmentOut]]:
    company_ids = {job.company_id for job in jobs}
    h1b_lookup = await load_h1b_summary_lookup(db, company_ids) if needs_sponsorship else None
    company_lookup = await load_company_enrichment_lookup(db, company_ids)
    return h1b_lookup, company_lookup


def _enriched_job_out(
    job: NormalizedJob,
    *,
    h1b_lookup: H1bLookup | None,
    company_lookup: dict[uuid.UUID, CompanyEnrichmentOut],
    needs_sponsorship: bool,
) -> DashboardJobOut:
    h1b_info = _h1b_sponsorship_for_job(job, h1b_lookup) if needs_sponsorship else None
    return _job_to_out(
        job,
        h1b_sponsorship=h1b_info,
        company_info=company_lookup.get(job.company_id),
    )


@router.get("/jobs", response_model=DashboardJobsResponse)
async def get_dashboard_jobs(
    candidate_id: uuid.UUID = Query(...),
    location: Optional[str] = Query(default=None),
    remote_type: Optional[str] = Query(default=None),
    salary_min: Optional[int] = Query(default=None),
    role_type: Optional[str] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> DashboardJobsResponse:
    pools = await get_active_pools(db, candidate_id)
    if not pools:
        return DashboardJobsResponse(jobs=[], total=0)

    settings = get_settings()
    user_profile = await load_user_profile(db, candidate_id)
    filters = build_constraint_filters(user_profile, settings) if user_profile else []

    if location:
        filters.append(NormalizedJob.location.ilike(f"%{location}%"))
    if remote_type:
        filters.append(NormalizedJob.remote_type == remote_type)
    if salary_min is not None:
        filters.append(or_(NormalizedJob.salary_min.is_(None), NormalizedJob.salary_min >= salary_min))
    if role_type:
        suffix = f"_{role_type.upper()}"
        matching_pools = [pool for pool in pools if pool.endswith(suffix)]
        if matching_pools:
            filters.append(NormalizedJob.retrieval_pools.overlap(matching_pools))

    jobs = await query_jobs_in_pools(
        db,
        pools=pools,
        filters=filters,
        limit=limit,
        offset=offset,
    )

    count_stmt = select(func.count()).select_from(NormalizedJob).where(
        and_(
            NormalizedJob.retrieval_pools.overlap(pools),
            NormalizedJob.is_active.is_(True),
            NormalizedJob.processing_state == "success",
            NormalizedJob.opportunity_score.is_not(None),
            *filters,
        )
    )
    total = await db.scalar(count_stmt) or 0

    needs_sponsorship = _needs_sponsorship_data(user_profile)
    h1b_lookup, company_lookup = await _load_job_enrichment_lookups(
        db, jobs, needs_sponsorship=needs_sponsorship
    )
    jobs_out = [
        _enriched_job_out(
            job,
            h1b_lookup=h1b_lookup,
            company_lookup=company_lookup,
            needs_sponsorship=needs_sponsorship,
        )
        for job in jobs
    ]
    return DashboardJobsResponse(jobs=jobs_out, total=total)


@router.get("/jobs/recommended", response_model=DashboardRecommendedJobsResponse)
async def get_recommended_jobs(
    candidate_id: uuid.UUID = Query(...),
    scan_batch: int = Query(default=200, ge=1, le=200),
    cursor: Optional[str] = Query(default=None),
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> DashboardRecommendedJobsResponse:
    pools = await get_active_pools(db, candidate_id)
    if not pools:
        return DashboardRecommendedJobsResponse(jobs=[], total=0, has_more=False, scanned=0, returned=0)

    user_profile = await load_user_profile(db, candidate_id)
    if user_profile is None:
        return DashboardRecommendedJobsResponse(jobs=[], total=0, has_more=False, scanned=0, returned=0)

    scan_offset = 0
    if cursor:
        try:
            scan_offset = decode_recommended_cursor(cursor)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid cursor") from exc

    filters = build_constraint_filters(user_profile, settings)
    batch_jobs = await query_jobs_in_pools(
        db,
        pools=pools,
        filters=filters,
        limit=scan_batch,
        offset=scan_offset,
    )
    scanned = len(batch_jobs)
    has_more = scanned == scan_batch

    if scanned == 0:
        return DashboardRecommendedJobsResponse(
            jobs=[],
            total=0,
            next_cursor=None,
            has_more=False,
            scanned=0,
            returned=0,
        )

    needs_sponsorship = _needs_sponsorship_data(user_profile)
    h1b_lookup, company_lookup = await _load_job_enrichment_lookups(
        db, batch_jobs, needs_sponsorship=needs_sponsorship
    )
    scoring_lookup = h1b_lookup if settings.sponsorship_score_enabled and needs_sponsorship else None
    ranked = deduplicate_ranked_jobs(
        rank_jobs(batch_jobs, user_profile, settings, h1b_lookup=scoring_lookup)
    )
    applied_counts = await applied_count_by_company(db, candidate_id)
    diversified = select_diversified_jobs(
        ranked,
        len(ranked),
        applied_count_by_company=applied_counts,
        max_per_company=settings.recommendation_max_jobs_per_company,
        unlock_batch_size=settings.recommendation_company_unlock_batch,
    )

    jobs_out: list[DashboardRecommendedJobOut] = []
    for job, score in diversified:
        base = _enriched_job_out(
            job,
            h1b_lookup=h1b_lookup,
            company_lookup=company_lookup,
            needs_sponsorship=needs_sponsorship,
        )
        jobs_out.append(
            DashboardRecommendedJobOut(
                **base.model_dump(),
                personal_score=score,
                match_reasons=generate_explanations(job, user_profile),
            )
        )

    next_cursor = encode_recommended_cursor(scan_offset + scanned) if has_more else None
    returned = len(jobs_out)
    return DashboardRecommendedJobsResponse(
        jobs=jobs_out,
        total=returned,
        next_cursor=next_cursor,
        has_more=has_more,
        scanned=scanned,
        returned=returned,
    )


@router.get("/jobs/{job_id}", response_model=DashboardJobOut)
async def get_dashboard_job(
    job_id: uuid.UUID,
    candidate_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
) -> DashboardJobOut:
    pools = await get_active_pools(db, candidate_id)
    if not pools:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active subscriptions")

    job = await db.scalar(
        select(NormalizedJob).where(
            NormalizedJob.id == job_id,
            NormalizedJob.retrieval_pools.overlap(pools),
            NormalizedJob.is_active.is_(True),
            NormalizedJob.processing_state == "success",
        )
    )
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    settings = get_settings()
    user_profile = await load_user_profile(db, candidate_id)
    if settings.experience_tier_visibility_enabled and user_profile is not None:
        from app.scoring.experience_tier import job_exceeds_visibility_ceiling

        if job_exceeds_visibility_ceiling(
            job.experience_tier,
            settings.experience_tier_visibility_ceiling,
        ):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    needs_sponsorship = _needs_sponsorship_data(user_profile)
    h1b_lookup, company_lookup = await _load_job_enrichment_lookups(
        db, [job], needs_sponsorship=needs_sponsorship
    )
    return _enriched_job_out(
        job,
        h1b_lookup=h1b_lookup,
        company_lookup=company_lookup,
        needs_sponsorship=needs_sponsorship,
    )


@router.post("/jobs/{job_id}/apply", response_model=UserApplicationOut)
async def mark_job_applied(
    job_id: uuid.UUID,
    candidate_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
) -> UserApplicationOut:
    return await apply_to_job(db, candidate_id=candidate_id, job_id=job_id)


@router.get("/applications", response_model=UserApplicationsResponse)
async def list_applications(
    candidate_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
) -> UserApplicationsResponse:
    applications = await get_user_applications(db, candidate_id)
    return UserApplicationsResponse(applications=applications, total=len(applications))


@router.patch("/applications/{application_id}", response_model=UserApplicationOut)
async def update_application(
    application_id: uuid.UUID,
    payload: UserApplicationPatchIn,
    candidate_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
) -> UserApplicationOut:
    return await patch_application(
        db,
        candidate_id=candidate_id,
        application_id=application_id,
        payload=payload,
    )
