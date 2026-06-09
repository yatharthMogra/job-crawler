from __future__ import annotations

import pytest

from app.ingestion.extractor.llm import ENRICHMENT_SYSTEM_PROMPT, JobEnrichment, finalize_enrichment
from app.ingestion.extractor.seniority import (
    apply_seniority_consistency,
    build_batch_job_payload,
    expand_seniority_aliases,
    infer_seniority_from_title,
    normalize_seniority,
)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("mid", "MID"),
        ("senior", "SENIOR"),
        ("internship", "INTERN"),
        ("new_grad", "NEW_GRAD"),
        ("unclear", "UNKNOWN"),
        ("STAFF", "STAFF"),
        ("", "UNKNOWN"),
    ],
)
def test_normalize_seniority(raw: str, expected: str) -> None:
    assert normalize_seniority(raw) == expected


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        ("Software Engineering Intern", "INTERN"),
        ("2026 New Grad Software Engineer", "NEW_GRAD"),
        ("Senior Backend Engineer", "SENIOR"),
        ("Staff Platform Engineer", "STAFF"),
        ("Principal Engineer", "PRINCIPAL"),
        ("Engineering Manager", "MANAGEMENT"),
        ("Entry Level Data Analyst", "ENTRY"),
        ("Backend Engineer", None),
    ],
)
def test_infer_seniority_from_title(title: str, expected: str | None) -> None:
    assert infer_seniority_from_title(title) == expected


def test_apply_seniority_consistency_intern_flags() -> None:
    seniority, is_intern, is_new_grad = apply_seniority_consistency(
        "MID",
        True,
        False,
        title="Software Engineer Intern",
    )
    assert seniority == "INTERN"
    assert is_intern is True
    assert is_new_grad is False


def test_apply_seniority_consistency_new_grad_flags() -> None:
    seniority, is_intern, is_new_grad = apply_seniority_consistency(
        "UNKNOWN",
        False,
        True,
        title="Backend Engineer",
    )
    assert seniority == "NEW_GRAD"
    assert is_intern is False
    assert is_new_grad is True


def test_finalize_enrichment_overrides_from_title() -> None:
    enrichment = JobEnrichment(
        seniority="MID",
        is_internship=False,
        is_new_grad=False,
        sponsorship_status="unclear",
        sponsorship_confidence="low",
        remote_type="unclear",
    )
    finalized = finalize_enrichment(
        enrichment,
        title="Software Engineering Intern",
        employment_type="Internship",
    )
    assert finalized.seniority == "INTERN"
    assert finalized.is_internship is True


def test_build_batch_job_payload_includes_hints() -> None:
    payload = build_batch_job_payload(
        job_id="abc",
        text="description",
        title="New Grad Software Engineer",
        employment_type="Full-time",
    )
    assert payload["seniority_hint"] == "NEW_GRAD"
    assert payload["title"] == "New Grad Software Engineer"


def test_expand_seniority_aliases_includes_legacy() -> None:
    aliases = expand_seniority_aliases({"MID"})
    assert "mid" in aliases
    assert "MID" in aliases


def test_enrichment_prompt_includes_seniority_rules() -> None:
    assert "seniority rules:" in ENRICHMENT_SYSTEM_PROMPT
    assert "INTERN" in ENRICHMENT_SYSTEM_PROMPT
