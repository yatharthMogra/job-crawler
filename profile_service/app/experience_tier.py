from __future__ import annotations

from typing import Any, Literal

ExperienceTier = Literal[
    "INTERN",
    "NEW_GRAD",
    "JUNIOR",
    "MID",
    "SENIOR",
    "ABOVE_SENIOR",
    "UNKNOWN",
]

EXPERIENCE_TIER_LEVELS: tuple[str, ...] = (
    "INTERN",
    "NEW_GRAD",
    "JUNIOR",
    "MID",
    "SENIOR",
    "ABOVE_SENIOR",
    "UNKNOWN",
)

EXPERIENCE_TIER_ORDER: tuple[str, ...] = (
    "INTERN",
    "NEW_GRAD",
    "JUNIOR",
    "MID",
    "SENIOR",
    "ABOVE_SENIOR",
)

_LEGACY_TO_CANONICAL: dict[str, str] = {
    "intern": "INTERN",
    "internship": "INTERN",
    "new_grad": "NEW_GRAD",
    "newgrad": "NEW_GRAD",
    "new_graduate": "NEW_GRAD",
    "entry": "JUNIOR",
    "entry_level": "JUNIOR",
    "early_career": "JUNIOR",
    "junior": "JUNIOR",
    "mid": "MID",
    "middle": "MID",
    "mid_level": "MID",
    "senior": "SENIOR",
    "staff": "ABOVE_SENIOR",
    "principal": "ABOVE_SENIOR",
    "management": "ABOVE_SENIOR",
    "director": "ABOVE_SENIOR",
    "vp": "ABOVE_SENIOR",
    "executive": "ABOVE_SENIOR",
    "above_senior": "ABOVE_SENIOR",
    "lead": "ABOVE_SENIOR",
    "unclear": "UNKNOWN",
    "unknown": "UNKNOWN",
}


def normalize_experience_tier(value: str | None) -> str:
    if not value:
        return "UNKNOWN"
    cleaned = value.strip()
    if cleaned in EXPERIENCE_TIER_LEVELS:
        return cleaned
    mapped = _LEGACY_TO_CANONICAL.get(cleaned.lower())
    if mapped:
        return mapped
    upper = cleaned.upper()
    if upper in EXPERIENCE_TIER_LEVELS:
        return upper
    return "UNKNOWN"


def sum_evidence_months(evidence: list[Any]) -> int:
    total = 0
    for item in evidence:
        if getattr(item, "evidence_type", None) != "experience":
            continue
        if not getattr(item, "is_active", True) or not getattr(item, "is_approved", False):
            continue
        data = getattr(item, "normalized_data", None) or {}
        if isinstance(data, dict):
            months = data.get("duration_months")
            if isinstance(months, (int, float)) and months > 0:
                total += int(months)
    return total


def evidence_months_to_years(months: int) -> float:
    return round(months / 12.0, 1) if months > 0 else 0.0


def derive_current_experience_tier(
    *,
    full_time_years: float | None,
    is_currently_enrolled: bool | None,
    expected_graduation: str | None,
    evidence_months: int | None = None,
    internship_only: bool = False,
) -> str:
    years = full_time_years
    if years is None and evidence_months is not None:
        years = evidence_months_to_years(evidence_months)
    if years is None:
        years = 0.0

    enrolled = bool(is_currently_enrolled)

    if enrolled:
        if internship_only:
            return "INTERN"
        if years >= 3:
            return "MID"
        if years >= 1:
            return "JUNIOR"
        return "NEW_GRAD"

    if years <= 0:
        return "NEW_GRAD"
    if years < 2:
        return "JUNIOR"
    if years < 5:
        return "MID"
    return "SENIOR"
