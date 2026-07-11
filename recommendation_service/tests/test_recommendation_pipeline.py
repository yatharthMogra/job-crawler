"""Unit tests for recommendation pipeline helpers (no DB)."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.constraints.evaluator import RankingJob, filter_jobs_by_constraints
from app.config import Settings
from app.scoring.embedding_similarity import max_cosine_similarity
from app.scoring.rrf import reciprocal_rank_fusion
from app.services.profile_loader import UserProfile


def _job(opp: float, emb: list[float] | None = None, **kw) -> RankingJob:
    now = datetime.now(timezone.utc)
    return RankingJob(
        id=kw.get("id", uuid4()),
        company_id=uuid4(),
        title=kw.get("title", "Engineer"),
        company_name=kw.get("company_name", "Acme"),
        location="SF",
        job_country="US",
        posting_url=None,
        posted_at=now,
        reference_at=now,
        created_at=now,
        remote_type="hybrid",
        application_effort="LOW",
        salary_min=100000,
        salary_max=150000,
        opportunity_score=opp,
        retrieval_pools=["SOFTWARE_ENGINEER_FULLTIME"],
        normalized_roles=["SOFTWARE_ENGINEER"],
        job_capabilities=kw.get("job_capabilities", []),
        tech_stack=[],
        skills=[],
        seniority=kw.get("seniority", "MID"),
        experience_tier="MID",
        is_internship=False,
        is_new_grad=False,
        sponsorship_status="yes",
        sponsorship_confidence="high",
        requires_clearance=kw.get("requires_clearance", False),
        requires_citizenship=False,
        role_intent="IC",
        job_domain="Software",
        job_secondary_domain=None,
        content_embedding=emb,
    )


def test_pipeline_rrf_ordering_with_constraints() -> None:
    """High embedding similarity can surface a job ahead of pure opportunity_score order."""
    resume = [[1.0, 0.0, 0.0]]
    high_opp = _job(0.95, emb=[0.0, 1.0, 0.0])  # orthogonal to resume
    high_emb = _job(0.5, emb=[1.0, 0.0, 0.0])  # identical to resume
    mid = _job(0.7, emb=[0.5, 0.5, 0.0])

    jobs = [high_opp, high_emb, mid]
    sims = {j.id: max_cosine_similarity(j.content_embedding, resume) for j in jobs}
    by_opp = sorted(jobs, key=lambda j: j.opportunity_score or 0, reverse=True)
    by_emb = sorted(jobs, key=lambda j: sims[j.id], reverse=True)
    fused = reciprocal_rank_fusion([[j.id for j in by_opp], [j.id for j in by_emb]], k=60)

    # high_emb should rank above mid after fusion (strong semantic + decent opp)
    assert fused.index(high_emb.id) < fused.index(mid.id)


def test_constraints_preserve_rrf_order() -> None:
    a = _job(0.9, requires_clearance=True)
    b = _job(0.8, requires_clearance=False)
    c = _job(0.7, requires_clearance=False)
    profile = UserProfile(
        candidate_id=uuid4(),
        email="a@b.com",
        name="T",
        constraints={"has_clearance": False},
        preferences={},
        skills={},
    )
    settings = Settings(
        role_intent_filter_enabled=False,
        domain_filter_enabled=False,
        experience_tier_visibility_enabled=False,
    )
    ordered = [a, b, c]
    filtered = filter_jobs_by_constraints(ordered, profile, settings)
    assert [j.id for j in filtered] == [b.id, c.id]
