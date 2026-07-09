from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace

from app.config import Settings
from app.models.shared import NormalizedJob
from app.notification.company_watch_batch import select_company_watch_jobs
from app.notification.company_watch_eligibility import job_matches_user_pools
from app.scoring.recommendation import score_job
from app.services.profile_loader import UserProfile


def _job(**kwargs) -> NormalizedJob:
    defaults = {
        "id": uuid.uuid4(),
        "title": "Backend Engineer",
        "company_name": "Google",
        "location": "New York, NY",
        "posting_url": "https://example.com",
        "posted_at": None,
        "is_active": True,
        "processing_state": "success",
        "seniority": "JUNIOR",
        "is_internship": False,
        "is_new_grad": False,
        "sponsorship_status": "yes",
        "sponsorship_confidence": "high",
        "remote_type": "hybrid",
        "tech_stack": ["Python", "AWS"],
        "skills": ["REST"],
        "normalized_roles": ["BACKEND_ENGINEER"],
        "job_capabilities": ["Backend Engineering"],
        "application_effort": "LOW",
        "retrieval_pools": ["BACKEND_ENGINEER_FULLTIME"],
        "salary_min": 120_000,
        "salary_max": 150_000,
        "opportunity_score": 0.8,
        "role_intent": "engineer",
        "created_at": datetime.now(timezone.utc),
    }
    defaults.update(kwargs)
    return NormalizedJob(**defaults)


def _profile(**kwargs) -> UserProfile:
    defaults = {
        "candidate_id": uuid.uuid4(),
        "email": "test@example.com",
        "name": "Test",
        "constraints": {"target_seniority": ["INTERN", "NEW_GRAD", "ENTRY", "JUNIOR"]},
        "preferences": {
            "preferred_locations": ["United States"],
            "primary_role_intents": ["engineer", "researcher"],
        },
        "skills": {
            "languages": ["Python", "Java", "TypeScript"],
            "frameworks": ["FastAPI", "React"],
            "tools": [],
            "databases": ["PostgreSQL"],
            "other": [],
        },
        "capabilities": [SimpleNamespace(capability_name="Backend Engineering")],
    }
    defaults.update(kwargs)
    return UserProfile(**defaults)


def test_job_matches_user_pools_overlap() -> None:
    job = _job(retrieval_pools=["SWE_FULLTIME", "BACKEND_ENGINEER_FULLTIME"])
    assert job_matches_user_pools(job, ["BACKEND_ENGINEER_FULLTIME"]) is True
    assert job_matches_user_pools(job, ["DATA_ANALYST_FULLTIME"]) is False


def test_job_matches_user_pools_empty_pools() -> None:
    job = _job()
    assert job_matches_user_pools(job, []) is False


def test_select_company_watch_jobs_drops_below_threshold() -> None:
    job_high = _job(title="Backend Engineer")
    job_low = _job(title="Unrelated Role", tech_stack=[], job_capabilities=[])
    selected = select_company_watch_jobs(
        [(job_high, 0.75), (job_low, 0.25)],
        min_score=0.5,
        max_jobs=5,
    )
    assert len(selected) == 1
    assert selected[0][0].title == "Backend Engineer"
    assert selected[0][1] == 0.75


def test_select_company_watch_jobs_sorted_by_score() -> None:
    job_a = _job(title="Role A")
    job_b = _job(title="Role B")
    selected = select_company_watch_jobs(
        [(job_a, 0.6), (job_b, 0.9)],
        min_score=0.5,
        max_jobs=5,
    )
    assert [job.title for job, _ in selected] == ["Role B", "Role A"]


def test_select_company_watch_jobs_respects_cap() -> None:
    jobs = [(_job(title=f"Role {index}"), 0.6 + index * 0.01) for index in range(5)]
    selected = select_company_watch_jobs(jobs, min_score=0.5, max_jobs=2)
    assert len(selected) == 2


def test_good_swe_match_scores_above_threshold() -> None:
    settings = Settings()
    profile = _profile()
    job = _job()
    score = score_job(job, profile, settings)
    assert score >= settings.company_watch_min_score


def test_hardware_job_blocked_by_pool_mismatch() -> None:
    user_pools = ["BACKEND_ENGINEER_FULLTIME", "SWE_FULLTIME"]
    hardware_job = _job(
        title="Data Center Mechanical Cooling Engineer",
        retrieval_pools=["HARDWARE_ENGINEER_FULLTIME"],
        normalized_roles=["HARDWARE_ENGINEER"],
        job_capabilities=["Hardware Engineering"],
    )
    assert job_matches_user_pools(hardware_job, user_pools) is False


def test_educator_intent_job_has_wrong_pool_for_swe_user() -> None:
    user_pools = ["SWE_FULLTIME"]
    instructor_job = _job(
        title="Technical Curriculum Developer II",
        retrieval_pools=["OTHER_FULLTIME"],
        role_intent="educator",
        job_capabilities=["Technical Training"],
    )
    assert job_matches_user_pools(instructor_job, user_pools) is False


def test_senior_swe_may_score_below_threshold_for_entry_profile() -> None:
    settings = Settings(company_watch_min_score=0.5)
    profile = _profile(
        constraints={"target_seniority": ["INTERN", "NEW_GRAD", "ENTRY", "JUNIOR"]},
    )
    senior_job = _job(title="Senior Software Engineer", seniority="SENIOR")
    score = score_job(senior_job, profile, settings)
    selected = select_company_watch_jobs(
        [(senior_job, score)],
        min_score=settings.company_watch_min_score,
        max_jobs=5,
    )
    if score < settings.company_watch_min_score:
        assert selected == []
