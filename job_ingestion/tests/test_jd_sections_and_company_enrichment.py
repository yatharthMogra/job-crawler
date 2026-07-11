from __future__ import annotations

import json

from app.ingestion.company_enrichment.llm import (
    COMPANY_ENRICHMENT_SYSTEM_PROMPT,
    CompanyEnrichmentResult,
)
from app.ingestion.company_enrichment.resolver import resolve_company_website
from app.ingestion.extractor.llm import (
    ENRICHMENT_SYSTEM_PROMPT,
    BatchJobEnrichmentResponse,
    JobEnrichment,
)
from app.models.company import Company


def test_enrichment_prompt_includes_section_rules() -> None:
    assert "description section rules:" in ENRICHMENT_SYSTEM_PROMPT
    assert "responsibilities:" in ENRICHMENT_SYSTEM_PROMPT
    assert "required_qualifications:" in ENRICHMENT_SYSTEM_PROMPT


def test_job_enrichment_parses_section_fields() -> None:
    payload = {
        "seniority": "MID",
        "is_internship": False,
        "is_new_grad": False,
        "sponsorship_status": "unclear",
        "sponsorship_confidence": "low",
        "remote_type": "hybrid",
        "tech_stack": ["Python"],
        "skills": ["distributed systems"],
        "normalized_roles": ["BACKEND_ENGINEER"],
        "job_capabilities": ["Backend Engineering"],
        "application_effort": "MEDIUM",
        "responsibilities": ["Build APIs", "Own on-call rotation"],
        "required_qualifications": ["5+ years Python"],
        "preferred_qualifications": ["Kubernetes experience"],
        "benefits": ["Equity", "401k match"],
    }
    parsed = JobEnrichment.model_validate(payload)
    assert parsed.responsibilities == ["Build APIs", "Own on-call rotation"]
    assert parsed.required_qualifications == ["5+ years Python"]
    assert parsed.preferred_qualifications == ["Kubernetes experience"]
    assert parsed.benefits == ["Equity", "401k match"]


def test_job_enrichment_defaults_section_fields_to_empty_lists() -> None:
    payload = {
        "seniority": "MID",
        "is_internship": False,
        "is_new_grad": False,
        "sponsorship_status": "unclear",
        "sponsorship_confidence": "low",
        "remote_type": "onsite",
    }
    parsed = JobEnrichment.model_validate(payload)
    assert parsed.responsibilities == []
    assert parsed.required_qualifications == []
    assert parsed.preferred_qualifications == []
    assert parsed.benefits == []
    assert parsed.required_skills == []
    assert parsed.preferred_skills == []


def test_batch_response_parses_section_fields() -> None:
    payload = {
        "items": [
            {
                "job_id": "abc-123",
                "responsibilities": ["Ship features"],
                "required_qualifications": ["BS in CS"],
                "preferred_qualifications": [],
                "benefits": ["Health insurance"],
            }
        ]
    }
    parsed = BatchJobEnrichmentResponse.model_validate_json(json.dumps(payload))
    assert parsed.items[0].responsibilities == ["Ship features"]
    assert parsed.items[0].benefits == ["Health insurance"]


def test_company_enrichment_prompt_exists() -> None:
    assert "founded_year" in COMPANY_ENRICHMENT_SYSTEM_PROMPT


def test_company_enrichment_result_parses_fields() -> None:
    parsed = CompanyEnrichmentResult.model_validate(
        {
            "founded_year": 2015,
            "headquarters": "San Francisco, CA",
            "employee_count_range": "1001-5000",
            "one_line_description": "Payments infrastructure company.",
            "website": "https://stripe.com",
            "linkedin_url": "https://www.linkedin.com/company/stripe",
            "glassdoor_rating": 4.2,
        }
    )
    assert parsed.founded_year == 2015
    assert parsed.glassdoor_rating == 4.2


def test_resolve_company_website_from_platform_config() -> None:
    company = Company(
        name="Acme",
        platform="greenhouse",
        board_token="acme",
        platform_config={"company_website": "https://acme.example"},
    )
    assert resolve_company_website(company) == "https://acme.example"


def test_resolve_company_website_skips_ats_host() -> None:
    company = Company(name="Acme", platform="greenhouse", board_token="acme")
    assert (
        resolve_company_website(company, posting_url="https://boards.greenhouse.io/acme/jobs/1")
        is None
    )
