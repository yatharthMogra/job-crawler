from app.utils.constraints import normalize_constraints


def test_normalize_constraints_from_eeo_requires_sponsorship() -> None:
    out = normalize_constraints({"eeo": {"requires_sponsorship": True}})
    assert out["sponsorship_required"] is True


def test_normalize_constraints_from_visa_type() -> None:
    out = normalize_constraints({"visa_type": "F1"})
    assert out["sponsorship_required"] is True


def test_normalize_constraints_from_work_authorization() -> None:
    out = normalize_constraints({"work_authorization": "OPT"})
    assert out["sponsorship_required"] is True


def test_normalize_constraints_preserves_explicit_false() -> None:
    out = normalize_constraints(
        {
            "sponsorship_required": False,
            "visa_type": "US_CITIZEN",
        }
    )
    assert out["sponsorship_required"] is False
