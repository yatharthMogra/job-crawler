from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from app.ingestion.h1b.fiscal_year import current_fiscal_year
from app.ingestion.h1b.rebuild_summary import _LOOKBACK_YEARS, _TOP_SPONSOR_LIMIT


def test_lookback_constants() -> None:
    assert _LOOKBACK_YEARS == 3
    assert _TOP_SPONSOR_LIMIT == 500


def test_current_fiscal_year_october() -> None:
    assert current_fiscal_year(as_of=date(2024, 10, 15)) == 2025
