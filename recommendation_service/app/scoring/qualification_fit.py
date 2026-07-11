"""Qualification fit score: job-anchored coverage + structural adequacy."""

from __future__ import annotations

from dataclasses import dataclass

import structlog

from app.config import Settings
from app.models.shared import NormalizedJob
from app.scoring.coverage import EmbedFn, capability_coverage, skill_coverage_components
from app.scoring.structural import (
    education_adequacy_score,
    experience_adequacy_score,
    qualification_structural_score,
)
from app.services.profile_loader import UserProfile

log = structlog.get_logger(__name__)


@dataclass(frozen=True)
class QualificationFitBreakdown:
    raw: float
    skill_coverage: float
    capability_coverage: float
    structural_score: float
    experience_adequacy: float
    education_adequacy: float
    required_skill_coverage: float
    preferred_skill_coverage: float


def calibrate_qualification_fit_display(
    raw: float,
    *,
    raw_p5: float,
    raw_p95: float,
) -> float:
    if raw_p95 <= raw_p5:
        return max(0.0, min(1.0, raw))
    scaled = (raw - raw_p5) / (raw_p95 - raw_p5)
    return max(0.0, min(1.0, scaled))


def compute_qualification_fit(
    job: NormalizedJob,
    profile: UserProfile,
    settings: Settings,
    *,
    embed_fn: EmbedFn | None = None,
    embedding_min_sim: float = 0.3,
    embedding_max_sim: float = 0.85,
    idf_by_term: dict[str, float] | None = None,
    corpus_size: int = 0,
    avg_doc_len: float = 400.0,
    embed_cache: dict[str, list[float] | None] | None = None,
) -> QualificationFitBreakdown:
    skills, required_skill_cov, preferred_skill_cov = skill_coverage_components(
        job,
        profile,
        settings,
        embed_fn=embed_fn,
        embedding_min_sim=embedding_min_sim,
        embedding_max_sim=embedding_max_sim,
        idf_by_term=idf_by_term,
        corpus_size=corpus_size,
        avg_doc_len=avg_doc_len,
        embed_cache=embed_cache,
    )
    capabilities = capability_coverage(
        job,
        profile,
        settings,
        embed_fn=embed_fn,
        embedding_min_sim=embedding_min_sim,
        embedding_max_sim=embedding_max_sim,
        idf_by_term=idf_by_term,
        corpus_size=corpus_size,
        avg_doc_len=avg_doc_len,
        embed_cache=embed_cache,
    )
    experience = experience_adequacy_score(profile, job)
    education = education_adequacy_score(profile, job)
    structural = qualification_structural_score(profile, job)

    raw = (
        settings.qualification_fit_skill_weight * skills
        + settings.qualification_fit_capability_weight * capabilities
        + settings.qualification_fit_structural_weight * structural
    )
    raw = max(0.0, min(1.0, raw))

    breakdown = QualificationFitBreakdown(
        raw=raw,
        skill_coverage=skills,
        capability_coverage=capabilities,
        structural_score=structural,
        experience_adequacy=experience,
        education_adequacy=education,
        required_skill_coverage=required_skill_cov,
        preferred_skill_coverage=preferred_skill_cov,
    )

    if settings.qualification_fit_shadow_mode:
        log.info(
            "qualification_fit_shadow",
            job_id=str(job.id),
            candidate_id=str(profile.candidate_id),
            **breakdown.__dict__,
        )

    return breakdown
