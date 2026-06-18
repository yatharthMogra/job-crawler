"""A/B validation: sponsorship scoring changes ranking order when enabled."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace

from app.config import Settings
from app.models.shared import NormalizedJob
from app.notification.ranker import rank_jobs
from app.services.h1b_lookup import H1bSummaryRow
from app.services.profile_loader import UserProfile


def _job(company_id: uuid.UUID, *, title: str, caps: list[str]) -> NormalizedJob:
    return NormalizedJob(
        id=uuid.uuid4(),
        job_archive_id=None,
        external_job_id="1",
        company_id=company_id,
        title=title,
        company_name="Co",
        location="NYC",
        job_country="US",
        posting_url=None,
        posted_at=datetime.now(timezone.utc),
        is_active=True,
        processing_state="success",
        seniority="MID",
        is_internship=False,
        is_new_grad=False,
        sponsorship_status="unclear",
        sponsorship_confidence="low",
        remote_type="hybrid",
        tech_stack=["Python"],
        skills=["Python"],
        normalized_roles=["BACKEND_ENGINEER"],
        job_capabilities=caps,
        application_effort="MEDIUM",
        retrieval_pools=["BACKEND_ENGINEER_FULLTIME"],
        job_domain="Software",
        job_secondary_domain=None,
        requires_clearance=False,
        role_intent="engineer",
        salary_min=120000,
        salary_max=180000,
        opportunity_score=0.5,
        created_at=datetime.now(timezone.utc),
    )


def test_sponsorship_scoring_boosts_known_sponsor() -> None:
    sponsor_id = uuid.uuid4()
    unknown_id = uuid.uuid4()
    profile = UserProfile(
        candidate_id=uuid.uuid4(),
        email="test@example.com",
        name="Test",
        capabilities=[SimpleNamespace(capability_name="Backend Engineering")],
        skills={"languages": ["Python"], "frameworks": [], "tools": [], "databases": [], "other": []},
        preferences={},
        constraints={"sponsorship_required": True},
    )
    jobs = [
        _job(unknown_id, title="Backend A", caps=["Backend Engineering"]),
        _job(sponsor_id, title="Backend B", caps=["Backend Engineering"]),
    ]
    lookup = {
        (sponsor_id, "SWE"): H1bSummaryRow("SWE", 100, 0.95, True, [2022, 2023, 2024]),
    }

    settings_off = Settings(sponsorship_score_enabled=False)
    settings_on = Settings(sponsorship_score_enabled=True)

    ranked_off = rank_jobs(jobs, profile, settings_off)
    ranked_on = rank_jobs(jobs, profile, settings_on, h1b_lookup=lookup)

    off_scores = {item[0].company_id: item[1] for item in ranked_off}
    assert off_scores[sponsor_id] == off_scores[unknown_id]

    assert ranked_on[0][0].company_id == sponsor_id
    assert ranked_on[0][1] > ranked_on[1][1]
