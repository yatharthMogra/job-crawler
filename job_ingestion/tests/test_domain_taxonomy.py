from __future__ import annotations

from app.ingestion.extractor.llm import BatchJobEnrichment
from app.ingestion.taxonomy import (
    derive_user_domains,
    is_valid_domain_pair,
    sanitize_job_secondary_domain,
    validate_pools_against_domain,
)


def test_software_aerospace_not_valid_pair() -> None:
    assert is_valid_domain_pair("Software", "Aerospace_Defense") is False


def test_software_data_analytics_valid_pair() -> None:
    assert is_valid_domain_pair("Software", "Data_Analytics") is True


def test_sanitize_strips_software_aerospace_secondary() -> None:
    assert sanitize_job_secondary_domain("Software", "Aerospace_Defense") is None


def test_sanitize_keeps_valid_secondary() -> None:
    assert sanitize_job_secondary_domain("Software", "Data_Analytics") == "Data_Analytics"


def test_validate_pools_strips_cross_domain_pools() -> None:
    pools = ["SWE_FULLTIME", "SYSTEMS_ENGINEER_FULLTIME"]
    validated = validate_pools_against_domain("Aerospace_Defense", pools)
    assert validated == ["SYSTEMS_ENGINEER_FULLTIME"]


def test_validate_pools_allows_secondary_domain_pools() -> None:
    pools = ["SWE_FULLTIME", "DATA_SCIENTIST_FULLTIME"]
    validated = validate_pools_against_domain(
        "Software",
        pools,
        job_secondary_domain="Data_Analytics",
    )
    assert validated == ["SWE_FULLTIME", "DATA_SCIENTIST_FULLTIME"]


def test_derive_user_domains_software_only() -> None:
    caps = [
        "Backend Engineering",
        "Full Stack Development",
        "AI Systems",
        "Distributed Systems",
        "Cloud Infrastructure",
        "DevOps",
    ]
    primary, secondary = derive_user_domains(caps)
    assert primary == "Software"
    assert secondary is None


def test_derive_user_domains_below_threshold_returns_other() -> None:
    primary, secondary = derive_user_domains(["Backend Engineering", "DevOps"])
    assert primary == "Other"
    assert secondary is None


def test_batch_enrichment_strips_invalid_domain_secondary() -> None:
    parsed = BatchJobEnrichment.model_validate(
        {
            "job_id": "abc",
            "is_internship": False,
            "is_new_grad": False,
            "job_domain": "Software",
            "job_secondary_domain": "Aerospace_Defense",
        }
    )
    assert parsed.job_domain == "Software"
    assert parsed.job_secondary_domain is None
