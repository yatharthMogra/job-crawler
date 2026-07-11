"""Full recommendation ranking pipeline: skinny retrieval → RRF → constraints → score → diversify."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from datetime import timezone

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.constraints.evaluator import RankingJob, filter_jobs_by_constraints
from app.models.shared import NormalizedJob
from app.notification.ranker import (
    deduplicate_ranked_jobs,
    rank_jobs,
    select_diversified_jobs,
)
from app.notification.retrieval import query_jobs_for_ranking
from app.scoring.bm25_corpus import ensure_idf_cache
from app.scoring.embedding_similarity import max_cosine_similarity
from app.scoring.rrf import reciprocal_rank_fusion
from app.services.applications import applied_count_by_company
from app.services.profile_loader import UserProfile, load_user_profile
from app.services.resume_embedding_loader import load_resume_embeddings
from app.services.subscriptions import get_active_pools
from app.services.term_embedding import embed_term

log = structlog.get_logger(__name__)


@dataclass
class RankedJobEntry:
    job_id: uuid.UUID
    personal_score: float
    opportunity_score: float
    reference_timestamp: float
    company_name: str = ""


@dataclass
class AuxSnapshot:
    applied_counts: dict[str, int] = field(default_factory=dict)


@dataclass
class PipelineResult:
    ranked_entries: list[RankedJobEntry]
    profile: UserProfile
    profile_version: int
    resume_fingerprint: str
    aux_snapshot: AuxSnapshot


def _reference_timestamp(job: NormalizedJob | RankingJob) -> float:
    ts = job.reference_at or job.posted_at
    if ts is None:
        ts = job.created_at
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return ts.timestamp()


def _to_ranking_job(job: NormalizedJob) -> RankingJob:
    return RankingJob(
        id=job.id,
        company_id=job.company_id,
        title=job.title,
        company_name=job.company_name,
        location=job.location,
        job_country=job.job_country,
        posting_url=job.posting_url,
        posted_at=job.posted_at,
        reference_at=job.reference_at,
        created_at=job.created_at,
        remote_type=job.remote_type,
        application_effort=job.application_effort,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        opportunity_score=job.opportunity_score,
        retrieval_pools=list(job.retrieval_pools or []),
        normalized_roles=list(job.normalized_roles or []),
        job_capabilities=list(job.job_capabilities or []),
        tech_stack=list(job.tech_stack or []),
        skills=list(job.skills or []),
        seniority=job.seniority,
        experience_tier=job.experience_tier or "UNKNOWN",
        is_internship=job.is_internship,
        is_new_grad=job.is_new_grad,
        sponsorship_status=job.sponsorship_status,
        sponsorship_confidence=job.sponsorship_confidence,
        requires_clearance=job.requires_clearance,
        requires_citizenship=job.requires_citizenship,
        role_intent=job.role_intent,
        job_domain=job.job_domain,
        job_secondary_domain=job.job_secondary_domain,
        content_embedding=list(job.content_embedding) if job.content_embedding else None,
        responsibilities=list(job.responsibilities or []),
        required_qualifications=list(job.required_qualifications or []),
        preferred_qualifications=list(job.preferred_qualifications or []),
        required_skills=list(job.required_skills or []),
        preferred_skills=list(job.preferred_skills or []),
        benefits=list(job.benefits or []),
        is_active=job.is_active,
        processing_state=job.processing_state,
    )


async def _load_profile_version(db: AsyncSession, candidate_id: uuid.UUID) -> int:
    from sqlalchemy import select

    from app.models.shared import CandidateProfile

    version = await db.scalar(
        select(CandidateProfile.version).where(
            CandidateProfile.candidate_id == candidate_id,
            CandidateProfile.is_current.is_(True),
        )
    )
    return int(version) if version is not None else 0


async def run_recommendation_pipeline(
    db: AsyncSession,
    candidate_id: uuid.UUID,
    settings: Settings,
) -> PipelineResult | None:
    """Run full ranking pipeline. Returns None if candidate has no pools or profile."""
    t0 = time.perf_counter()

    pools = await get_active_pools(db, candidate_id)
    if not pools:
        return None

    user_profile = await load_user_profile(db, candidate_id)
    if user_profile is None:
        return None

    profile_version = await _load_profile_version(db, candidate_id)
    resume_bundle = await load_resume_embeddings(db, candidate_id)
    applied_counts = await applied_count_by_company(db, candidate_id)

    t_retrieve = time.perf_counter()
    orm_jobs = await query_jobs_for_ranking(db, pools=pools, settings=settings)
    ranking_jobs = [_to_ranking_job(job) for job in orm_jobs]
    log.info(
        "recommendation_retrieval",
        candidate_id=str(candidate_id),
        job_count=len(ranking_jobs),
        ms=round((time.perf_counter() - t_retrieve) * 1000, 1),
    )

    if not ranking_jobs:
        return PipelineResult(
            ranked_entries=[],
            profile=user_profile,
            profile_version=profile_version,
            resume_fingerprint=resume_bundle.fingerprint,
            aux_snapshot=AuxSnapshot(applied_counts=applied_counts),
        )

    # Embedding similarity (max-of-5 resumes)
    similarities: dict[uuid.UUID, float] = {
        job.id: max_cosine_similarity(job.content_embedding, resume_bundle.embeddings)
        for job in ranking_jobs
    }

    # Two ranked lists for RRF
    by_opportunity = sorted(
        ranking_jobs,
        key=lambda j: j.opportunity_score or 0.0,
        reverse=True,
    )
    by_embedding = sorted(
        ranking_jobs,
        key=lambda j: similarities.get(j.id, 0.0),
        reverse=True,
    )

    t_rrf = time.perf_counter()
    fused_ids = reciprocal_rank_fusion(
        [[j.id for j in by_opportunity], [j.id for j in by_embedding]],
        k=settings.recommendation_rrf_k,
    )
    jobs_by_id = {job.id: job for job in ranking_jobs}
    rrf_ordered = [jobs_by_id[job_id] for job_id in fused_ids if job_id in jobs_by_id]
    log.info(
        "recommendation_rrf",
        candidate_id=str(candidate_id),
        ms=round((time.perf_counter() - t_rrf) * 1000, 1),
    )

    # Hard constraints in-process (preserve RRF order)
    eligible = filter_jobs_by_constraints(rrf_ordered, user_profile, settings)

    # score_job / personal_score on full surviving set
    t_score = time.perf_counter()
    await ensure_idf_cache(db)
    ranked = deduplicate_ranked_jobs(
        rank_jobs(eligible, user_profile, settings, embed_fn=embed_term)
    )
    diversified = select_diversified_jobs(
        ranked,
        len(ranked),
        applied_count_by_company=applied_counts,
        max_per_company=settings.recommendation_max_jobs_per_company,
        unlock_batch_size=settings.recommendation_company_unlock_batch,
    )
    log.info(
        "recommendation_scoring",
        candidate_id=str(candidate_id),
        eligible=len(eligible),
        returned=len(diversified),
        ms=round((time.perf_counter() - t_score) * 1000, 1),
    )

    entries = [
        RankedJobEntry(
            job_id=job.id,
            personal_score=score,
            opportunity_score=job.opportunity_score or 0.0,
            reference_timestamp=_reference_timestamp(job),
            company_name=job.company_name,
        )
        for job, score in diversified
    ]

    log.info(
        "recommendation_pipeline_complete",
        candidate_id=str(candidate_id),
        total_ms=round((time.perf_counter() - t0) * 1000, 1),
        ranked=len(entries),
    )

    return PipelineResult(
        ranked_entries=entries,
        profile=user_profile,
        profile_version=profile_version,
        resume_fingerprint=resume_bundle.fingerprint,
        aux_snapshot=AuxSnapshot(applied_counts=applied_counts),
    )
