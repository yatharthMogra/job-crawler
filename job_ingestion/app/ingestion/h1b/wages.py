from __future__ import annotations

from decimal import Decimal


def normalize_wage_to_annual(wage_from: float | Decimal | None, wage_unit: str | None) -> float | None:
    if wage_from is None:
        return None
    amount = float(wage_from)
    if amount <= 0:
        return None
    unit = (wage_unit or "").strip().lower()
    if unit in ("year", "annual", "yr"):
        return amount
    if unit in ("hour", "hr"):
        return amount * 2080
    if unit in ("week", "wk"):
        return amount * 52
    if unit in ("month", "mo"):
        return amount * 12
    if unit in ("bi-weekly", "biweekly"):
        return amount * 26
    return amount
