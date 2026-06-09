from __future__ import annotations

from app.ingestion.constants_taxonomy import ENGINEERING_ROLES, NORMALIZED_ROLES
from app.ingestion.extractor.llm import ENRICHMENT_SYSTEM_PROMPT, JobEnrichment, _coerce_normalized_roles


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
    ):
        assert role in NORMALIZED_ROLES


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


def test_engineering_roles_include_solutions_and_support() -> None:
    assert "SOLUTIONS_ENGINEER" in ENGINEERING_ROLES
    assert "SUPPORT_ENGINEER" in ENGINEERING_ROLES
    assert "SALES" not in ENGINEERING_ROLES
