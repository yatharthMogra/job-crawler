#!/usr/bin/env python3
"""Spot-check ATS fit score ranking direction on synthetic resume/job pairs."""

from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "recommendation_service"
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from app.config import Settings  # noqa: E402
from app.models.shared import CandidateEvidence, NormalizedJob  # noqa: E402
from app.scoring.ats_fit import compute_ats_fit  # noqa: E402
from app.scoring.bm25_corpus import normalized_bm25_score  # noqa: E402
from app.scoring.qualification_fit import compute_qualification_fit  # noqa: E402
from app.scoring.structural import structural_match_score  # noqa: E402
from app.services.profile_loader import UserProfile  # noqa: E402


class _FakeDb:
    async def scalars(self, *_args, **_kwargs):
        class _Result:
            def all(self):
                return []

        return _Result()

    async def scalar(self, *_args, **_kwargs):
        return None

    async def get(self, *_args, **_kwargs):
        return None


def _job(title: str, *, skills: list[str], quals: list[str]) -> NormalizedJob:
    return NormalizedJob(
        id=uuid.uuid4(),
        external_job_id="1",
        company_id=uuid.uuid4(),
        title=title,
        company_name="Acme",
        location="Remote",
        posting_url="https://example.com",
        description_text=" ".join(skills + quals),
        description_preview=None,
        posted_at=None,
        reference_at=None,
        is_active=True,
        processing_state="success",
        seniority="senior",
        experience_tier="SENIOR",
        is_internship=False,
        is_new_grad=False,
        sponsorship_status="unclear",
        sponsorship_confidence="low",
        remote_type="remote",
        tech_stack=skills,
        skills=skills,
        required_skills=skills,
        preferred_skills=[],
        normalized_roles=["DATA_ENGINEER"],
        job_capabilities=[],
        application_effort="MEDIUM",
        retrieval_pools=["DATA_ENGINEERING_FULLTIME"],
        job_domain="DATA_ENGINEERING",
        job_secondary_domain=None,
        requires_clearance=False,
        requires_citizenship=False,
        role_intent=None,
        salary_min=120000,
        salary_max=180000,
        opportunity_score=0.8,
        created_at=None,
        responsibilities=["Build data pipelines"],
        required_qualifications=quals,
        preferred_qualifications=[],
        benefits=[],
        content_embedding=None,
        content_embedding_model=None,
        pool_percentile_cutoffs={},
    )


def _profile(
    *,
    title: str,
    resume_text: str,
    tier: str = "SENIOR",
    skills: list[str] | None = None,
) -> UserProfile:
    evidence = CandidateEvidence(
        id=uuid.uuid4(),
        candidate_id=uuid.uuid4(),
        evidence_type="experience",
        is_approved=True,
        is_active=True,
        raw_source_text=resume_text,
        normalized_data={"title": title, "company": "Previous Co"},
    )
    return UserProfile(
        candidate_id=uuid.uuid4(),
        email="test@example.com",
        name="Test User",
        constraints={"current_experience_tier": tier},
        preferences={},
        skills={"languages": skills or ["Python", "SQL"]},
        education={"entries": [{"degree": "BS Computer Science", "university": "State U"}]},
        evidence=[evidence],
    )


def main() -> None:
    job = _job(
        "Data Engineer",
        skills=["Python", "SQL", "Spark", "Airflow", "dbt"],
        quals=["3+ years data engineering", "BS in Computer Science"],
    )
    strong_resume = """
    Data Engineer with 6 years building Python and Spark pipelines, Airflow orchestration,
  dbt transformations, and SQL analytics platforms.
    """
    weak_resume = """
    Marketing Manager with campaign analytics, brand strategy, and social media management.
    """

    strong_profile = _profile(
        title="Data Engineer",
        resume_text=strong_resume,
        skills=["Python", "SQL", "Spark", "Airflow", "dbt"],
    )
    weak_profile = _profile(
        title="Marketing Manager",
        resume_text=weak_resume,
        tier="MID",
        skills=["Campaign Analytics", "Brand Strategy"],
    )

    strong_bm25 = normalized_bm25_score(strong_resume, job.description_text or "", protected_phrases=job.skills)
    weak_bm25 = normalized_bm25_score(weak_resume, job.description_text or "", protected_phrases=job.skills)
    assert strong_bm25 > weak_bm25, f"expected strong BM25 > weak BM25 ({strong_bm25} vs {weak_bm25})"

    strong_structural = structural_match_score(strong_profile, job)
    weak_structural = structural_match_score(weak_profile, job)
    assert strong_structural > weak_structural, (
        f"expected strong structural > weak structural ({strong_structural} vs {weak_structural})"
    )

    settings = Settings(ats_fit_enabled=True)
    strong_qualification = compute_qualification_fit(job, strong_profile, settings)
    weak_qualification = compute_qualification_fit(job, weak_profile, settings)
    assert strong_qualification.raw > weak_qualification.raw, (
        "expected strong qualification fit > weak qualification fit "
        f"({strong_qualification.raw} vs {weak_qualification.raw})"
    )
    db = _FakeDb()

    async def _run() -> None:
        strong = await compute_ats_fit(db, job=job, profile=strong_profile, user_pools=["DATA_ENGINEERING_FULLTIME"], settings=settings)
        weak = await compute_ats_fit(db, job=job, profile=weak_profile, user_pools=["DATA_ENGINEERING_FULLTIME"], settings=settings)
        assert strong.ats_fit_score is not None and weak.ats_fit_score is not None
        assert strong.ats_fit_score > weak.ats_fit_score, (
            f"expected strong ATS > weak ATS ({strong.ats_fit_score} vs {weak.ats_fit_score})"
        )
        print(
            {
                "strong": strong.ats_fit_score,
                "weak": weak.ats_fit_score,
                "strong_bm25": round(strong_bm25, 3),
                "weak_bm25": round(weak_bm25, 3),
                "strong_qualification_fit": round(strong_qualification.raw, 3),
                "weak_qualification_fit": round(weak_qualification.raw, 3),
            }
        )

    import asyncio

    asyncio.run(_run())


if __name__ == "__main__":
    main()
