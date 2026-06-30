from __future__ import annotations

import json

import pytest

from app.ingestion.extractor.llm import (
    BatchJobEnrichment,
    BatchJobEnrichmentResponse,
    JobEnrichment,
    _coerce_job_capabilities,
    _coerce_salary,
    parse_batch_enrichment_response,
)


def _base_payload() -> dict:
    return {
        "seniority": "MID",
        "experience_tier": "MID",
        "is_internship": False,
        "is_new_grad": False,
        "sponsorship_status": "unclear",
        "sponsorship_confidence": "low",
        "remote_type": "hybrid",
        "tech_stack": ["Python"],
        "skills": ["API design"],
        "normalized_roles": ["BACKEND_ENGINEER"],
        "job_capabilities": ["Backend Engineering"],
        "application_effort": "MEDIUM",
    }


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (120_000.0, 120_000),
        (185_000.5, 185_000),
        ("120000", 120_000),
        ("$120,000", 120_000),
        ("120k", 120_000),
        (None, None),
        ("", None),
        (True, None),
    ],
)
def test_coerce_salary(raw: object, expected: int | None) -> None:
    assert _coerce_salary(raw) == expected


def test_job_enrichment_coerces_float_salary() -> None:
    payload = {**_base_payload(), "salary_min": 100_000.0, "salary_max": 150_000.0}
    parsed = JobEnrichment.model_validate(payload)
    assert parsed.salary_min == 100_000
    assert parsed.salary_max == 150_000


def test_batch_job_enrichment_filters_invalid_capabilities() -> None:
    payload = {
        "job_id": "job-1",
        **_base_payload(),
        "job_capabilities": ["Backend Engineering", "Not A Real Capability"],
    }
    parsed = BatchJobEnrichment.model_validate(payload)
    assert parsed.job_capabilities == ["Backend Engineering"]


def test_coerce_job_capabilities_non_list() -> None:
    assert _coerce_job_capabilities("Backend Engineering") == []


def test_parse_batch_enrichment_response_lenient_skips_bad_item() -> None:
    payload = {
        "items": [
            {
                "job_id": "good",
                **_base_payload(),
                "salary_min": 90_000.0,
                "salary_max": 110_000.0,
            },
            {
                "job_id": "bad",
                **_base_payload(),
                "sponsorship_status": "maybe",
            },
        ]
    }
    parsed = parse_batch_enrichment_response(json.dumps(payload))
    assert len(parsed.items) == 1
    assert parsed.items[0].job_id == "good"
    assert parsed.items[0].salary_min == 90_000


def test_parse_batch_enrichment_response_fenced_json() -> None:
    payload = {"items": [{"job_id": "abc", **_base_payload(), "salary_min": "80k"}]}
    text = f"```json\n{json.dumps(payload)}\n```"
    parsed = parse_batch_enrichment_response(text)
    assert parsed.items[0].salary_min == 80_000


def test_batch_response_strict_with_coercion() -> None:
    payload = {
        "items": [
            {
                "job_id": "abc-123",
                "tech_stack": ["Go"],
                "skills": ["API design"],
                "normalized_roles": ["SWE"],
                "salary_max": 200_000.0,
            }
        ]
    }
    parsed = BatchJobEnrichmentResponse.model_validate_json(json.dumps(payload))
    assert parsed.items[0].salary_max == 200_000
