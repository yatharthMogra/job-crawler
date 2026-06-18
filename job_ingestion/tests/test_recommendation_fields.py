from __future__ import annotations

from datetime import datetime, timezone

from app.config import Settings
from app.ingestion.recommendation_fields import (
    assign_retrieval_pools,
    assign_validated_retrieval_pools,
    compute_opportunity_score,
    fields_for_job_enrichment_record,
)


def test_assign_retrieval_pools_internship() -> None:
    pools = assign_retrieval_pools(["ML_ENGINEER", "BACKEND_ENGINEER"], is_internship=True, is_new_grad=False)
    assert pools == ["ML_ENGINEER_INTERNSHIP", "BACKEND_ENGINEER_INTERNSHIP"]


def test_assign_retrieval_pools_new_grad() -> None:
    pools = assign_retrieval_pools(["SWE"], is_internship=False, is_new_grad=True)
    assert pools == ["SWE_NEW_GRAD"]


def test_assign_retrieval_pools_fulltime() -> None:
    pools = assign_retrieval_pools(["DATA_SCIENTIST"], is_internship=False, is_new_grad=False)
    assert pools == ["DATA_SCIENTIST_FULLTIME"]


def test_assign_validated_retrieval_pools_keeps_pools_on_domain_mismatch() -> None:
    pools = assign_validated_retrieval_pools(
        ["TECHNICAL_PROGRAM_MANAGER"],
        is_internship=False,
        is_new_grad=False,
        job_domain="Management",
    )
    assert pools == ["TECHNICAL_PROGRAM_MANAGER_FULLTIME"]


def test_compute_opportunity_score_high_effort_low_comp() -> None:
    settings = Settings(
        opportunity_score_freshness_decay=0.01,
        comp_floor=40_000,
        comp_ceiling=250_000,
    )
    posted_at = datetime.now(timezone.utc)
    score = compute_opportunity_score(
        posted_at,
        salary_min=50_000,
        salary_max=60_000,
        application_effort="HIGH",
        settings=settings,
    )
    assert 0.0 <= score <= 1.0
    assert score < 0.8


def test_compute_opportunity_score_unknown_salary_neutral() -> None:
    settings = Settings()
    posted_at = datetime.now(timezone.utc)
    score = compute_opportunity_score(posted_at, None, None, "LOW", settings=settings)
    assert score > 0.5


def test_fields_for_job_enrichment_record_strips_domain_keys() -> None:
    fields = {
        "normalized_roles": ["SWE"],
        "job_capabilities": ["Backend Engineering"],
        "application_effort": "MEDIUM",
        "retrieval_pools": ["SWE_FULLTIME"],
        "job_domain": "Software",
        "job_secondary_domain": None,
        "salary_min": 100_000,
        "salary_max": 150_000,
        "opportunity_score": 0.7,
        "opportunity_score_computed_at": datetime.now(timezone.utc),
    }
    audit = fields_for_job_enrichment_record(fields)
    assert "job_domain" not in audit
    assert "job_secondary_domain" not in audit
    assert audit["normalized_roles"] == ["SWE"]
    assert audit["salary_min"] == 100_000
