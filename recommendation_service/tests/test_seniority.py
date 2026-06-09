from __future__ import annotations

from app.scoring.seniority import (
    expand_seniority_aliases,
    get_target_seniority,
    normalize_seniority,
    seniority_hard_block_values,
    seniority_retrieval_values,
    seniority_score_multiplier,
)


def test_get_target_seniority_defaults() -> None:
    assert get_target_seniority({}) == ["INTERN", "NEW_GRAD", "ENTRY", "MID", "JUNIOR"]


def test_get_target_seniority_from_constraints() -> None:
    assert get_target_seniority({"target_seniority": ["mid", "SENIOR"]}) == ["MID", "SENIOR"]


def test_seniority_retrieval_includes_unknown_and_senior() -> None:
    allowed = seniority_retrieval_values(["INTERN", "NEW_GRAD"])
    assert "UNKNOWN" in allowed
    assert "unclear" in allowed
    assert "SENIOR" in allowed
    assert "senior" in allowed
    assert "MID" not in allowed
    assert "mid" not in allowed


def test_seniority_hard_block_excludes_leadership() -> None:
    blocked = seniority_hard_block_values(["INTERN", "NEW_GRAD"])
    assert "MANAGEMENT" in blocked
    assert "STAFF" in blocked
    assert "PRINCIPAL" in blocked


def test_seniority_hard_block_allows_when_targeted() -> None:
    blocked = seniority_hard_block_values(["STAFF", "PRINCIPAL", "MANAGEMENT"])
    assert blocked == set()


def test_seniority_score_multiplier_soft_penalty() -> None:
    constraints = {"target_seniority": ["INTERN", "NEW_GRAD", "ENTRY", "MID"]}
    assert seniority_score_multiplier("SENIOR", constraints) == 0.6
    assert seniority_score_multiplier("MID", constraints) == 1.0
    assert seniority_score_multiplier("UNKNOWN", constraints) == 1.0


def test_normalize_seniority_legacy() -> None:
    assert normalize_seniority("junior") == "JUNIOR"
    assert normalize_seniority("unclear") == "UNKNOWN"
