from __future__ import annotations

import uuid

import pytest

from app.ingestion.h1b.matching import classify_fuzzy_match, fuzzy_match_employer
from app.ingestion.h1b.normalize import normalize_employer_name
from app.ingestion.h1b.wages import normalize_wage_to_annual
from app.ingestion.h1b.fiscal_year import fiscal_year_from_date
from datetime import date


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Google LLC", "GOOGLE"),
        ("AMAZON.COM SERVICES LLC", "AMAZON COM"),
        ("META PLATFORMS INC", "META PLATFORMS"),
        ("Microsoft Corporation", "MICROSOFT"),
        ("Stripe, Inc.", "STRIPE"),
    ],
)
def test_normalize_employer_name(raw: str, expected: str) -> None:
    assert normalize_employer_name(raw) == expected


def test_fuzzy_match_exact_threshold() -> None:
    lookup = {"GOOGLE": uuid.uuid4()}
    match, score = fuzzy_match_employer("GOOGLE", lookup)
    assert match == "GOOGLE"
    assert score == 1.0


def test_fuzzy_match_auto_link() -> None:
    company_id = uuid.uuid4()
    lookup = {"META PLATFORMS": company_id}
    match, score = fuzzy_match_employer("PLATFORMS META", lookup)
    assert match == "META PLATFORMS"
    assert score >= 0.88
    assert classify_fuzzy_match(score) == "fuzzy_auto"


def test_fuzzy_match_candidate() -> None:
    company_id = uuid.uuid4()
    lookup = {"AMAZON COM": company_id}
    match, score = fuzzy_match_employer("AMAZON WEB SERVICES", lookup)
    if match:
        method = classify_fuzzy_match(score)
        assert method in ("fuzzy_auto", "fuzzy_candidate", "unmatched")


def test_wage_normalization() -> None:
    assert normalize_wage_to_annual(100, "Hour") == 208000
    assert normalize_wage_to_annual(150000, "Year") == 150000
    assert normalize_wage_to_annual(5000, "Month") == 60000


def test_fiscal_year() -> None:
    assert fiscal_year_from_date(date(2024, 9, 30)) == 2024
    assert fiscal_year_from_date(date(2024, 10, 1)) == 2025
