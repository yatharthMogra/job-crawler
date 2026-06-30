from __future__ import annotations

from app.experience_tier import derive_current_experience_tier


def test_derive_enrolled_no_experience() -> None:
    assert (
        derive_current_experience_tier(
            full_time_years=0,
            is_currently_enrolled=True,
            expected_graduation="2027-05",
            evidence_months=0,
        )
        == "NEW_GRAD"
    )


def test_derive_enrolled_with_prior_experience() -> None:
    assert (
        derive_current_experience_tier(
            full_time_years=5,
            is_currently_enrolled=True,
            expected_graduation="2027-05",
            evidence_months=60,
        )
        == "MID"
    )


def test_derive_not_enrolled_mid_career() -> None:
    assert (
        derive_current_experience_tier(
            full_time_years=3,
            is_currently_enrolled=False,
            expected_graduation=None,
            evidence_months=36,
        )
        == "MID"
    )


def test_derive_internship_only() -> None:
    assert (
        derive_current_experience_tier(
            full_time_years=0,
            is_currently_enrolled=True,
            expected_graduation="2027-05",
            evidence_months=0,
            internship_only=True,
        )
        == "INTERN"
    )
