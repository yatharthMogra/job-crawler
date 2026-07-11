"""ATS fit score: BM25 + semantic (max-of-5 resumes) + structural blend."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.models.shared import CandidateEvidence, EmbeddingCalibration, JobTermIdf, NormalizedJob
from app.scoring.bm25_corpus import normalized_bm25_score
from app.scoring.embedding_similarity import calibrate_similarity, max_cosine_similarity
from app.scoring.percentile import resolve_pool_percentile
from app.scoring.structural import structural_match_score, structural_signal_breakdown
from app.scoring.text_corpus import build_job_text, collect_protected_phrases
from app.services.profile_loader import UserProfile
from app.services.resume_embedding_loader import load_resume_embeddings


@dataclass
class AtsFitResult:
    ats_fit_score: int | None
    pool_percentile: int | None
    pool_percentile_label: str | None
    signals: dict[str, float | None]
    unavailable_reason: str | None


async def _load_idf_stats(db: AsyncSession) -> tuple[dict[str, float], int, float]:
    rows = (await db.scalars(select(JobTermIdf))).all()
    if not rows:
        return {}, 0, 400.0
    corpus_size = rows[0].corpus_size
    idf_by_term = {row.term: row.idf for row in rows}
    avg_doc_len = sum(row.document_frequency for row in rows) / max(len(rows), 1)
    return idf_by_term, corpus_size, float(avg_doc_len)


async def _load_embedding_calibration(db: AsyncSession) -> tuple[float, float]:
    row = await db.get(EmbeddingCalibration, 1)
    if row is None:
        return 0.3, 0.85
    return row.min_similarity, row.max_similarity


def _flatten_profile_skills(skills: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for group in skills.values():
        if isinstance(group, list):
            names.extend(str(item) for item in group)
        elif isinstance(group, dict):
            for value in group.values():
                if isinstance(value, list):
                    names.extend(str(item) for item in value)
    return names


async def _resume_text_fallback(db: AsyncSession, profile: UserProfile) -> str:
    evidence_rows = (
        await db.scalars(
            select(CandidateEvidence).where(
                CandidateEvidence.candidate_id == profile.candidate_id,
                CandidateEvidence.is_active.is_(True),
                CandidateEvidence.is_approved.is_(True),
            )
        )
    ).all()
    parts = [row.raw_source_text for row in evidence_rows if row.raw_source_text]
    parts.extend(_flatten_profile_skills(profile.skills or {}))
    return "\n".join(part.strip() for part in parts if part and part.strip())


def _blend_score(
    bm25: float,
    semantic: float | None,
    structural: float,
    settings: Settings,
) -> float:
    bm25_w = settings.ats_fit_bm25_weight
    semantic_w = settings.ats_fit_semantic_weight if semantic is not None else 0.0
    structural_w = settings.ats_fit_structural_weight
    total = bm25_w + semantic_w + structural_w
    if total <= 0:
        return 0.0
    semantic_value = semantic if semantic is not None else 0.0
    return (bm25_w * bm25 + semantic_w * semantic_value + structural_w * structural) / total


async def compute_ats_fit(
    db: AsyncSession,
    *,
    job: NormalizedJob,
    profile: UserProfile,
    user_pools: list[str],
    settings: Settings,
) -> AtsFitResult:
    if not settings.ats_fit_enabled:
        return AtsFitResult(
            ats_fit_score=None,
            pool_percentile=None,
            pool_percentile_label=None,
            signals={},
            unavailable_reason="feature_disabled",
        )

    resume_bundle = await load_resume_embeddings(db, profile.candidate_id)
    resume_text = resume_bundle.latest_raw_text or await _resume_text_fallback(db, profile)
    if not resume_text.strip():
        return AtsFitResult(
            ats_fit_score=None,
            pool_percentile=None,
            pool_percentile_label=None,
            signals={},
            unavailable_reason="no_resume",
        )

    job_text = build_job_text(
        description_text=job.description_text,
        description_preview=job.description_preview,
        responsibilities=job.responsibilities or [],
        required_qualifications=job.required_qualifications or [],
        preferred_qualifications=job.preferred_qualifications or [],
        tech_stack=job.tech_stack or [],
        skills=job.skills or [],
    )
    phrases = collect_protected_phrases(job.tech_stack or [], job.skills or [])
    idf_by_term, corpus_size, avg_doc_len = await _load_idf_stats(db)
    bm25 = normalized_bm25_score(
        resume_text,
        job_text,
        protected_phrases=phrases,
        idf_by_term=idf_by_term,
        corpus_size=corpus_size,
        avg_doc_len=avg_doc_len,
    )

    semantic: float | None = None
    raw_semantic: float | None = None
    if resume_bundle.embeddings and job.content_embedding:
        min_sim, max_sim = await _load_embedding_calibration(db)
        raw_similarity = max_cosine_similarity(job.content_embedding, resume_bundle.embeddings)
        if raw_similarity > 0:
            raw_semantic = raw_similarity
            semantic = calibrate_similarity(raw_similarity, min_sim, max_sim)

    structural = structural_match_score(profile, job)
    breakdown = structural_signal_breakdown(profile, job)
    blended = _blend_score(bm25, semantic, structural, settings)
    ats_score = int(round(max(0.0, min(1.0, blended)) * 100))

    percentile_score = raw_semantic if raw_semantic is not None else blended
    pool_percentile, pool_label = resolve_pool_percentile(
        semantic_score=percentile_score,
        pool_percentile_cutoffs=getattr(job, "pool_percentile_cutoffs", None) or {},
        job_pools=job.retrieval_pools or [],
        user_pools=user_pools,
    )

    return AtsFitResult(
        ats_fit_score=ats_score,
        pool_percentile=pool_percentile,
        pool_percentile_label=pool_label,
        signals={
            "bm25": round(bm25, 4),
            "semantic": round(semantic, 4) if semantic is not None else None,
            "structural": round(structural, 4),
            "title": round(breakdown["title"], 4),
            "experience": round(breakdown["experience"], 4),
            "education": round(breakdown["education"], 4),
        },
        unavailable_reason=None,
    )
