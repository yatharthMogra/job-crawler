from __future__ import annotations

from datetime import date, datetime


def fiscal_year_from_date(value: date | datetime | None) -> int | None:
    """US federal fiscal year: Oct 1 – Sep 30."""
    if value is None:
        return None
    if isinstance(value, datetime):
        value = value.date()
    if value.month >= 10:
        return value.year + 1
    return value.year


def current_fiscal_year(*, as_of: date | None = None) -> int:
    return fiscal_year_from_date(as_of or date.today()) or date.today().year
