from __future__ import annotations

import uuid

from app.models.shared import CandidateEvidence, NormalizedJob
from app.scoring.bm25_corpus import normalized_bm25_score
from app.scoring.percentile import percentile_from_score, resolve_pool_percentile
from app.scoring.structural import structural_match_score
from app.services.profile_loader import UserProfile


def _job() -> NormalizedJob:
    return NormalizedJob(
        id=uuid.uuid4(),
        external_job_id="1",
        company_id=uuid.uuid4(),
        title="Data Engineer",
        company_name="Acme",
        location="Remote",
        posting_url="https://example.com",
        description_text="Python Spark SQL Airflow dbt pipelines",
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
        tech_stack=["Python", "Spark", "SQL"],
        skills=["Airflow", "dbt"],
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
        responsibilities=["Build pipelines"],
        required_qualifications=["BS in Computer Science"],
        preferred_qualifications=[],
        benefits=[],
        content_embedding=None,
        content_embedding_model=None,
        pool_percentile_cutoffs={},
    )


def _profile(title: str, resume_text: str) -> UserProfile:
    return UserProfile(
        candidate_id=uuid.uuid4(),
        email="test@example.com",
        name="Test User",
        constraints={"current_experience_tier": "SENIOR"},
        preferences={},
        skills={"languages": ["Python", "SQL"]},
        education={"entries": [{"degree": "BS Computer Science", "university": "State U"}]},
        evidence=[
            CandidateEvidence(
                id=uuid.uuid4(),
                candidate_id=uuid.uuid4(),
                evidence_type="experience",
                is_approved=True,
                is_active=True,
                raw_source_text=resume_text,
                normalized_data={"title": title, "company": "Previous Co"},
            )
        ],
    )


def test_bm25_prefers_relevant_resume() -> None:
    job = _job()
    strong = "Python Spark SQL Airflow dbt data engineering pipelines"
    weak = "marketing brand campaigns social media strategy"
    strong_score = normalized_bm25_score(strong, job.description_text or "", protected_phrases=job.skills)
    weak_score = normalized_bm25_score(weak, job.description_text or "", protected_phrases=job.skills)
    assert strong_score > weak_score


def test_structural_prefers_matching_title() -> None:
    job = _job()
    strong = _profile("Data Engineer", "built pipelines")
    weak = _profile("Marketing Manager", "ran campaigns")
    assert structural_match_score(strong, job) > structural_match_score(weak, job)


def test_percentile_labels() -> None:
    from app.scoring.percentile import PoolCutoffs

    cutoffs = PoolCutoffs(p50=0.55, p75=0.65, p90=0.75, p95=0.82)
    pct, label = percentile_from_score(0.83, cutoffs)
    assert pct == 95
    assert label == "Top 5%"

    pct, label = percentile_from_score(0.76, cutoffs)
    assert pct == 90
    assert label == "Top 10%"


def test_resolve_pool_percentile_uses_overlap_pool() -> None:
    percentile, label = resolve_pool_percentile(
        semantic_score=0.8,
        pool_percentile_cutoffs={
            "DATA_ENGINEERING_FULLTIME": {
                "p50": 0.5,
                "p75": 0.65,
                "p90": 0.75,
                "p95": 0.82,
            }
        },
        job_pools=["DATA_ENGINEERING_FULLTIME", "SWE_FULLTIME"],
        user_pools=["SWE_FULLTIME", "DATA_ENGINEERING_FULLTIME"],
    )
    assert percentile == 90
    assert label == "Top 10%"
