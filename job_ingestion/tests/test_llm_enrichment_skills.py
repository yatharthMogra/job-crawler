from __future__ import annotations

import json

from app.ingestion.extractor.llm import (
    ENRICHMENT_SYSTEM_PROMPT,
    BatchJobEnrichmentResponse,
    JobEnrichment,
    _coerce_skill_terms,
    enrichment_missing_required_skills,
    enrichment_missing_skill_fields,
)


def test_enrichment_prompt_includes_skill_split_rules() -> None:
    assert "required_skills rules:" in ENRICHMENT_SYSTEM_PROMPT
    assert "preferred_skills rules:" in ENRICHMENT_SYSTEM_PROMPT
    assert "tech_stack rules:" in ENRICHMENT_SYSTEM_PROMPT
    assert "skills rules:" in ENRICHMENT_SYSTEM_PROMPT
    assert "Python" in ENRICHMENT_SYSTEM_PROMPT


def test_job_enrichment_parses_skill_split_fields() -> None:
    payload = {
        "seniority": "MID",
        "is_internship": False,
        "is_new_grad": False,
        "sponsorship_status": "unclear",
        "sponsorship_confidence": "low",
        "remote_type": "hybrid",
        "tech_stack": ["Python", "Kubernetes", "AWS"],
        "skills": ["distributed systems", "data pipelines"],
        "required_skills": ["Python", "Kubernetes"],
        "preferred_skills": ["AWS"],
        "required_qualifications": ["5+ years backend experience"],
        "preferred_qualifications": ["AWS experience"],
        "normalized_roles": ["BACKEND_ENGINEER"],
        "job_capabilities": ["Backend Engineering"],
        "application_effort": "MEDIUM",
    }
    parsed = JobEnrichment.model_validate(payload)
    assert parsed.tech_stack == ["Python", "Kubernetes", "AWS"]
    assert parsed.skills == ["distributed systems", "data pipelines"]
    assert parsed.required_skills == ["Python", "Kubernetes"]
    assert parsed.preferred_skills == ["AWS"]


def test_batch_response_parses_skill_split_fields_per_job() -> None:
    payload = {
        "items": [
            {
                "job_id": "abc-123",
                "tech_stack": ["Go", "PostgreSQL"],
                "skills": ["API design"],
                "required_skills": ["Go"],
                "preferred_skills": ["PostgreSQL"],
                "normalized_roles": ["SWE"],
            }
        ]
    }
    parsed = BatchJobEnrichmentResponse.model_validate_json(json.dumps(payload))
    assert parsed.items[0].required_skills == ["Go"]
    assert parsed.items[0].preferred_skills == ["PostgreSQL"]


def test_coerce_skill_terms_deduplicates_case_insensitively() -> None:
    assert _coerce_skill_terms(["Python", " python ", "", "Go"]) == ["Python", "Go"]


def test_coerce_skill_terms_non_list() -> None:
    assert _coerce_skill_terms("Python") == []


def test_enrichment_missing_required_skills_soft_qa() -> None:
    assert enrichment_missing_required_skills([], ["5+ years Python"]) is True
    assert enrichment_missing_required_skills(["Python"], ["5+ years Python"]) is False
    assert enrichment_missing_required_skills([], []) is False
    assert enrichment_missing_required_skills(
        [], ["5+ years Python"], normalized_roles=["PRODUCT_MANAGER"]
    ) is False
    assert enrichment_missing_required_skills(
        [], ["5+ years Python"], normalized_roles=["SWE"]
    ) is True


def test_enrichment_missing_skill_fields() -> None:
    assert enrichment_missing_skill_fields([], [], description_chars=500) is True
    assert enrichment_missing_skill_fields(
        [], [], description_chars=500, normalized_roles=["PRODUCT_MANAGER"]
    ) is False
    assert enrichment_missing_skill_fields(
        [], [], description_chars=500, normalized_roles=["SWE"]
    ) is True
    assert enrichment_missing_skill_fields(["Python"], [], description_chars=500) is False
    assert enrichment_missing_skill_fields([], ["NLP"], description_chars=500) is False
    assert enrichment_missing_skill_fields([], [], description_chars=100) is False
