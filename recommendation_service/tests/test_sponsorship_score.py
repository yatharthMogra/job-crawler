from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from app.config import Settings
from app.scoring.sponsorship import compute_sponsorship_score, h1b_info_from_lookup
from app.services.h1b_lookup import H1bSummaryRow


def _settings(*, enabled: bool) -> Settings:
    return Settings(sponsorship_score_enabled=enabled)


def test_sponsorship_score_neutral_when_not_required() -> None:
    assert compute_sponsorship_score(uuid.uuid4(), "SWE", False, {}) == 0.5


def test_sponsorship_score_no_data_penalty() -> None:
    assert compute_sponsorship_score(uuid.uuid4(), "SWE", True, {}) == 0.1


def test_sponsorship_score_top_sponsor() -> None:
    company_id = uuid.uuid4()
    lookup = {
        (company_id, "SWE"): H1bSummaryRow(
            pool_family="SWE",
            total_lca_3yr=100,
            approval_rate_3yr=0.95,
            is_top_sponsor=True,
            years_covered=[2022, 2023, 2024],
        )
    }
    assert compute_sponsorship_score(company_id, "SWE", True, lookup) == 1.0


def test_sponsorship_score_tier_thresholds() -> None:
    company_id = uuid.uuid4()
    lookup_mid = {
        (company_id, "SWE"): H1bSummaryRow("SWE", 10, None, False, [2024]),
    }
    lookup_low = {
        (company_id, "SWE"): H1bSummaryRow("SWE", 2, None, False, [2024]),
    }
    assert compute_sponsorship_score(company_id, "SWE", True, lookup_mid) == 0.5
    assert compute_sponsorship_score(company_id, "SWE", True, lookup_low) == 0.2


def test_h1b_info_from_lookup() -> None:
    company_id = uuid.uuid4()
    row = H1bSummaryRow("DATA_SCIENTIST", 25, 0.9, False, [2023, 2024])
    lookup = {(company_id, "DATA_SCIENTIST"): row}
    assert h1b_info_from_lookup(company_id, "DATA_SCIENTIST", lookup) == row
    assert h1b_info_from_lookup(company_id, None, lookup) is None
