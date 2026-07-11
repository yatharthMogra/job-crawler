from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.database import get_db
from app.models.shared import NormalizedJob, QualificationFitCalibration
from app.notification.ranker import deduplicate_ranked_jobs, rank_jobs, select_diversified_jobs
from app.notification.retrieval import (
    build_constraint_filters,
    query_jobs_in_pools,
)
from app.scoring.ats_fit import compute_ats_fit
from app.scoring.bm25_corpus import ensure_idf_cache
from app.scoring.explainability import generate_explanations
from app.scoring.preference_indicators import preference_indicators
from app.scoring.qualification_fit import (
    calibrate_qualification_fit_display,
    compute_qualification_fit,
)
from app.scoring.sponsorship import h1b_info_from_lookup
from app.schemas.applications import (
    UserApplicationOut,
    UserApplicationPatchIn,
    UserApplicationsResponse,
)
from app.schemas.ats_fit import AtsFitOut, AtsFitSignalsOut
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
from app.services.term_embedding import embed_term

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


async def _qualification_calibration(db: AsyncSession) -> tuple[float, float]:
    calibration = await db.get(QualificationFitCalibration, 1)
    if calibration is None or calibration.sample_size <= 0:
        return 0.0, 1.0
    return calibration.raw_p5, calibration.raw_p95


def _qualification_fit_for_response(
    job: NormalizedJob,
    profile: UserProfile,
    settings: Settings,
    calibration: tuple[float, float],
    embed_cache: dict[str, list[float] | None],
) -> float | None:
    if not (settings.qualification_fit_enabled or settings.qualification_fit_shadow_mode):
        return None
    breakdown = compute_qualification_fit(
        job,
        profile,
        settings,
        embed_fn=embed_term,
        embed_cache=embed_cache,
    )
    if not settings.qualification_fit_enabled or settings.qualification_fit_shadow_mode:
        return None
    return calibrate_qualification_fit_display(
        breakdown.raw,
        raw_p5=calibration[0],
        raw_p95=calibration[1],
    )


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
        requires_clearance=bool(job.requires_clearance),
        requires_citizenship=bool(job.requires_citizenship),
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
    reference_token: Optional[str] = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: Optional[int] = Query(default=None, ge=1, le=100),
    # Legacy params — used only when RECOMMENDATION_RRF_ENABLED=false
    scan_batch: int = Query(default=200, ge=1, le=200),
    cursor: Optional[str] = Query(default=None),
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> DashboardRecommendedJobsResponse:
    if settings.recommendation_rrf_enabled:
        return await _get_recommended_jobs_rrf(
            db=db,
            candidate_id=candidate_id,
            reference_token=reference_token,
            offset=offset,
            limit=limit,
            settings=settings,
        )
    return await _get_recommended_jobs_legacy(
        db=db,
        candidate_id=candidate_id,
        scan_batch=scan_batch,
        cursor=cursor,
        settings=settings,
    )


async def _get_recommended_jobs_rrf(
    *,
    db: AsyncSession,
    candidate_id: uuid.UUID,
    reference_token: str | None,
    offset: int,
    limit: int | None,
    settings: Settings,
) -> DashboardRecommendedJobsResponse:
    from app.services.job_fat_fetch import fat_fetch_jobs_by_ids
    from app.services.recommendation_cache import (
        delete_recommendation_session,
        deserialize_profile,
        load_recommendation_session,
        session_is_stale,
        store_recommendation_session,
    )
    from app.services.recommendation_pipeline import (
        PipelineResult,
        run_recommendation_pipeline,
    )

    page_size = limit or settings.recommendation_page_size
    page_size = min(page_size, settings.recommendation_page_size_max)

    session = None
    if reference_token:
        try:
            session = await load_recommendation_session(reference_token)
        except RuntimeError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Recommendation cache unavailable",
            ) from exc
        if session is not None:
            if session.candidate_id != candidate_id:
                session = None
            elif await session_is_stale(db, session):
                await delete_recommendation_session(reference_token)
                session = None

    pipeline_result: PipelineResult | None = None
    token = reference_token
    if session is None:
        try:
            pipeline_result = await run_recommendation_pipeline(db, candidate_id, settings)
        except RuntimeError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(exc),
            ) from exc
        if pipeline_result is None:
            return DashboardRecommendedJobsResponse(
                jobs=[],
                total=0,
                reference_token=None,
                offset=0,
                has_more=False,
                returned=0,
                total_ranked=0,
            )
        try:
            token = await store_recommendation_session(pipeline_result, settings)
        except RuntimeError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Recommendation cache unavailable",
            ) from exc
        ranked_entries = pipeline_result.ranked_entries
        user_profile = pipeline_result.profile
        # Fresh first page always starts at offset 0
        offset = 0
    else:
        ranked_entries = session.ranked_entries
        user_profile = deserialize_profile(session.profile_snapshot)
        token = session.reference_token

    total_ranked = len(ranked_entries)
    page_entries = ranked_entries[offset : offset + page_size]
    page_ids = [e.job_id for e in page_entries]
    score_by_id = {e.job_id: e.personal_score for e in page_entries}

    if not page_ids:
        return DashboardRecommendedJobsResponse(
            jobs=[],
            total=0,
            reference_token=token,
            offset=offset,
            has_more=False,
            returned=0,
            total_ranked=total_ranked,
        )

    batch_jobs = await fat_fetch_jobs_by_ids(db, page_ids)
    needs_sponsorship = _needs_sponsorship_data(user_profile)
    h1b_lookup, company_lookup = await _load_job_enrichment_lookups(
        db, batch_jobs, needs_sponsorship=needs_sponsorship
    )
    calibration = (
        await _qualification_calibration(db)
        if settings.qualification_fit_enabled and not settings.qualification_fit_shadow_mode
        else (0.0, 1.0)
    )
    qualification_embed_cache: dict[str, list[float] | None] = {}

    jobs_out: list[DashboardRecommendedJobOut] = []
    for job in batch_jobs:
        base = _enriched_job_out(
            job,
            h1b_lookup=h1b_lookup,
            company_lookup=company_lookup,
            needs_sponsorship=needs_sponsorship,
        )
        jobs_out.append(
            DashboardRecommendedJobOut(
                **base.model_dump(),
                personal_score=score_by_id.get(job.id, 0.0),
                qualification_fit=_qualification_fit_for_response(
                    job, user_profile, settings, calibration, qualification_embed_cache
                ),
                match_reasons=generate_explanations(job, user_profile),
                preference_indicators=[
                    indicator.__dict__ for indicator in preference_indicators(job, user_profile)
                ],
            )
        )

    returned = len(jobs_out)
    has_more = offset + returned < total_ranked
    return DashboardRecommendedJobsResponse(
        jobs=jobs_out,
        total=returned,
        reference_token=token,
        offset=offset,
        has_more=has_more,
        returned=returned,
        total_ranked=total_ranked,
    )


async def _get_recommended_jobs_legacy(
    *,
    db: AsyncSession,
    candidate_id: uuid.UUID,
    scan_batch: int,
    cursor: str | None,
    settings: Settings,
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
    await ensure_idf_cache(db)
    ranked = deduplicate_ranked_jobs(
        rank_jobs(
            batch_jobs,
            user_profile,
            settings,
            h1b_lookup=scoring_lookup,
            embed_fn=embed_term,
        )
    )
    applied_counts = await applied_count_by_company(db, candidate_id)
    diversified = select_diversified_jobs(
        ranked,
        len(ranked),
        applied_count_by_company=applied_counts,
        max_per_company=settings.recommendation_max_jobs_per_company,
        unlock_batch_size=settings.recommendation_company_unlock_batch,
    )
    calibration = (
        await _qualification_calibration(db)
        if settings.qualification_fit_enabled and not settings.qualification_fit_shadow_mode
        else (0.0, 1.0)
    )
    qualification_embed_cache: dict[str, list[float] | None] = {}

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
                qualification_fit=_qualification_fit_for_response(
                    job, user_profile, settings, calibration, qualification_embed_cache
                ),
                match_reasons=generate_explanations(job, user_profile),
                preference_indicators=[
                    indicator.__dict__ for indicator in preference_indicators(job, user_profile)
                ],
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
    job, user_profile = await _get_accessible_job(db, job_id=job_id, candidate_id=candidate_id)

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


async def _get_accessible_job(
    db: AsyncSession,
    *,
    job_id: uuid.UUID,
    candidate_id: uuid.UUID,
) -> tuple[NormalizedJob, UserProfile | None]:
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
    return job, user_profile


@router.get("/jobs/{job_id}/ats-fit", response_model=AtsFitOut)
async def get_job_ats_fit(
    job_id: uuid.UUID,
    candidate_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> AtsFitOut:
    job, user_profile = await _get_accessible_job(db, job_id=job_id, candidate_id=candidate_id)
    if user_profile is None:
        return AtsFitOut(unavailable_reason="no_resume")

    pools = await get_active_pools(db, candidate_id)
    result = await compute_ats_fit(
        db,
        job=job,
        profile=user_profile,
        user_pools=pools,
        settings=settings,
    )
    return AtsFitOut(
        ats_fit_score=result.ats_fit_score,
        pool_percentile=result.pool_percentile,
        pool_percentile_label=result.pool_percentile_label,
        signals=AtsFitSignalsOut(**result.signals),
        unavailable_reason=result.unavailable_reason,
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
