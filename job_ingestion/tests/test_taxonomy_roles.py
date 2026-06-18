from __future__ import annotations

from app.ingestion.constants_taxonomy import ENGINEERING_ROLES, NORMALIZED_ROLES
from app.ingestion.extractor.llm import ENRICHMENT_SYSTEM_PROMPT, JobEnrichment, _coerce_normalized_roles
from app.ingestion.recommendation_fields import assign_validated_retrieval_pools


def test_normalized_roles_includes_tier1_and_tier2() -> None:
    for role in (
        "SALES",
        "OPERATIONS",
        "CUSTOMER_SUCCESS",
        "SOLUTIONS_CONSULTANT",
        "RECRUITING",
        "FINANCE",
        "LEGAL",
        "PARTNERSHIPS",
        "PRODUCT_DESIGNER",
        "MARKETING",
        "SOLUTIONS_ENGINEER",
        "SUPPORT_ENGINEER",
        "TECHNICAL_PROGRAM_MANAGER",
        "DATA_ANALYST",
        "SYSTEMS_ENGINEER",
        "HARDWARE_ENGINEER",
    ):
        assert role in NORMALIZED_ROLES


def test_engineering_roles_include_systems_and_hardware() -> None:
    assert "SYSTEMS_ENGINEER" in ENGINEERING_ROLES
    assert "HARDWARE_ENGINEER" in ENGINEERING_ROLES


def test_coerce_normalized_roles_filters_invalid() -> None:
    assert _coerce_normalized_roles(["SALES", "NOT_A_ROLE"]) == ["SALES"]
    assert _coerce_normalized_roles([]) == ["OTHER"]


def test_job_enrichment_accepts_new_roles() -> None:
    parsed = JobEnrichment.model_validate(
        {
            "seniority": "MID",
            "is_internship": False,
            "is_new_grad": False,
            "sponsorship_status": "unclear",
            "sponsorship_confidence": "low",
            "remote_type": "remote",
            "normalized_roles": ["SALES", "CUSTOMER_SUCCESS"],
        }
    )
    assert parsed.normalized_roles == ["SALES", "CUSTOMER_SUCCESS"]


def test_enrichment_prompt_includes_role_classification_rules() -> None:
    assert "SALES:" in ENRICHMENT_SYSTEM_PROMPT
    assert "SOLUTIONS_CONSULTANT:" in ENRICHMENT_SYSTEM_PROMPT
    assert "SYSTEMS_ENGINEER:" in ENRICHMENT_SYSTEM_PROMPT
    assert "HARDWARE_ENGINEER:" in ENRICHMENT_SYSTEM_PROMPT
    assert "job_domain:" in ENRICHMENT_SYSTEM_PROMPT
    assert "Software + Aerospace_Defense is not a valid secondary pair" in ENRICHMENT_SYSTEM_PROMPT


def test_engineering_roles_include_solutions_and_support() -> None:
    assert "SOLUTIONS_ENGINEER" in ENGINEERING_ROLES
    assert "SUPPORT_ENGINEER" in ENGINEERING_ROLES
    assert "SALES" not in ENGINEERING_ROLES


def test_new_research_and_aerospace_roles_in_taxonomy() -> None:
    for role in (
        "RESEARCH_SCIENTIST",
        "LIFE_SCIENTIST",
        "AEROSPACE_ENGINEER",
        "FIELD_SERVICE_ENGINEER",
        "CONTROLS_ENGINEER",
    ):
        assert role in NORMALIZED_ROLES


def test_research_scientist_pool_maps_to_research_science_domain() -> None:
    pools = assign_validated_retrieval_pools(
        ["RESEARCH_SCIENTIST"],
        is_internship=False,
        is_new_grad=False,
        job_domain="Research_Science",
    )
    assert pools == ["RESEARCH_SCIENTIST_FULLTIME"]


def test_enrichment_prompt_includes_critical_domain_rule() -> None:
    assert "CRITICAL RULE" in ENRICHMENT_SYSTEM_PROMPT
    assert "company's industry never determines the domain" in ENRICHMENT_SYSTEM_PROMPT
    assert "RESEARCH_SCIENTIST:" in ENRICHMENT_SYSTEM_PROMPT


def test_enrichment_prompt_includes_secondary_domain_and_systems_rules() -> None:
    assert "Management + Business:" in ENRICHMENT_SYSTEM_PROMPT
    assert "NOT for people leadership" in ENRICHMENT_SYSTEM_PROMPT
    assert "SYSTEMS_ENGINEER at tech companies" in ENRICHMENT_SYSTEM_PROMPT
    assert "FIELD_SERVICE_ENGINEER:" in ENRICHMENT_SYSTEM_PROMPT
    assert "CONTROLS_ENGINEER:" in ENRICHMENT_SYSTEM_PROMPT


def test_field_service_and_controls_pools_map_to_domains() -> None:
    field_pools = assign_validated_retrieval_pools(
        ["FIELD_SERVICE_ENGINEER"],
        is_internship=False,
        is_new_grad=False,
        job_domain="Hardware_Electrical",
    )
    assert field_pools == ["FIELD_SERVICE_ENGINEER_FULLTIME"]

    controls_pools = assign_validated_retrieval_pools(
        ["CONTROLS_ENGINEER"],
        is_internship=False,
        is_new_grad=False,
        job_domain="Industrial_Automation",
    )
    assert controls_pools == ["CONTROLS_ENGINEER_FULLTIME"]
