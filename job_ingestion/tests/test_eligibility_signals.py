from __future__ import annotations

from app.ingestion.extractor.eligibility import (
    apply_eligibility_signals,
    detect_requires_citizenship,
    detect_requires_clearance,
)
from app.ingestion.extractor.llm import BatchJobEnrichment


def test_detect_requires_clearance_from_explicit_language() -> None:
    text = "Must be eligible to obtain and maintain a Secret security clearance."
    assert detect_requires_clearance(text) is True


def test_detect_requires_clearance_false_when_unmentioned() -> None:
    assert detect_requires_clearance("Build backend APIs in Python.") is False


def test_detect_requires_citizenship_from_us_person_requirement() -> None:
    text = "Must be a U.S. person eligible to obtain a security clearance."
    assert detect_requires_citizenship(text) is True


def test_detect_requires_citizenship_from_no_sponsorship() -> None:
    text = "We will not sponsor work visas for this position."
    assert detect_requires_citizenship(text) is True


def test_detect_requires_citizenship_false_when_ambiguous() -> None:
    assert detect_requires_citizenship("Join our engineering team in San Francisco.") is False


def test_apply_eligibility_signals_only_flips_false_to_true() -> None:
    enrichment = BatchJobEnrichment.model_validate(
        {
            "job_id": "abc",
            "is_internship": False,
            "is_new_grad": False,
            "requires_clearance": True,
            "requires_citizenship": False,
        }
    )
    updated = apply_eligibility_signals(
        enrichment,
        "Must be a U.S. citizen. Active TS/SCI clearance required.",
    )
    assert updated.requires_clearance is True
    assert updated.requires_citizenship is True
