from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.models.shared import NormalizedJob
from app.notification.ranker import deduplicate_ranked_jobs, normalize_title


def _job(title: str, company: str, location: str, score: float) -> tuple[NormalizedJob, float]:
    job = NormalizedJob(
        id=uuid.uuid4(),
        title=title,
        company_name=company,
        location=location,
        posting_url="https://example.com",
        posted_at=None,
        is_active=True,
        processing_state="success",
        seniority="junior",
        is_internship=False,
        is_new_grad=False,
        sponsorship_status="yes",
        sponsorship_confidence="high",
        remote_type="hybrid",
        tech_stack=[],
        skills=[],
        normalized_roles=[],
        job_capabilities=[],
        application_effort="LOW",
        retrieval_pools=[],
        salary_min=None,
        salary_max=None,
        opportunity_score=score,
        created_at=datetime.now(timezone.utc),
    )
    return job, score


def test_normalize_title_strips_whitespace_and_punctuation() -> None:
    assert normalize_title("  Software Engineer, Robotics.  ") == "software engineer, robotics"


def test_deduplicate_ranked_jobs_keeps_highest_score_first_occurrence() -> None:
    ranked = [
        _job("Software Engineer, Robotics", "Scale AI", "New York, NY", 0.9),
        _job("Software Engineer, Robotics", "Scale AI", "San Francisco, CA", 0.85),
        _job("Data Engineer", "Ramp", "New York, NY", 0.8),
    ]
    deduped = deduplicate_ranked_jobs(ranked)
    assert len(deduped) == 2
    assert deduped[0][0].location == "New York, NY"
    assert deduped[0][0].title == "Software Engineer, Robotics"
    assert deduped[1][0].title == "Data Engineer"


def test_deduplicate_ranked_jobs_allows_same_title_different_company() -> None:
    ranked = [
        _job("Software Engineer", "Scale AI", "New York, NY", 0.9),
        _job("Software Engineer", "Ramp", "New York, NY", 0.85),
    ]
    deduped = deduplicate_ranked_jobs(ranked)
    assert len(deduped) == 2
