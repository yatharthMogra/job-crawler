from __future__ import annotations

import json

from app.ingestion.extractor.llm import (
    ENRICHMENT_SYSTEM_PROMPT,
    BatchJobEnrichmentResponse,
    JobEnrichment,
    enrichment_missing_skill_fields,
)


def test_enrichment_prompt_includes_tech_stack_and_skills_rules() -> None:
    assert "tech_stack rules:" in ENRICHMENT_SYSTEM_PROMPT
    assert "skills rules:" in ENRICHMENT_SYSTEM_PROMPT
    assert "Python" in ENRICHMENT_SYSTEM_PROMPT


def test_job_enrichment_parses_tech_stack_and_skills() -> None:
    payload = {
        "seniority": "mid",
        "is_internship": False,
        "is_new_grad": False,
        "sponsorship_status": "unclear",
        "sponsorship_confidence": "low",
        "remote_type": "hybrid",
        "tech_stack": ["Python", "Kubernetes", "AWS"],
        "skills": ["distributed systems", "data pipelines"],
        "normalized_roles": ["BACKEND_ENGINEER"],
        "job_capabilities": ["Backend Engineering"],
        "application_effort": "MEDIUM",
    }
    parsed = JobEnrichment.model_validate(payload)
    assert parsed.tech_stack == ["Python", "Kubernetes", "AWS"]
    assert parsed.skills == ["distributed systems", "data pipelines"]


def test_batch_response_parses_skill_fields_per_job() -> None:
    payload = {
        "items": [
            {
                "job_id": "abc-123",
                "tech_stack": ["Go", "PostgreSQL"],
                "skills": ["API design"],
                "normalized_roles": ["SWE"],
            }
        ]
    }
    parsed = BatchJobEnrichmentResponse.model_validate_json(json.dumps(payload))
    assert parsed.items[0].tech_stack == ["Go", "PostgreSQL"]
    assert parsed.items[0].skills == ["API design"]


def test_enrichment_missing_skill_fields() -> None:
    assert enrichment_missing_skill_fields([], [], description_chars=500) is True
    assert enrichment_missing_skill_fields(["Python"], [], description_chars=500) is False
    assert enrichment_missing_skill_fields([], ["NLP"], description_chars=500) is False
    assert enrichment_missing_skill_fields([], [], description_chars=100) is False
