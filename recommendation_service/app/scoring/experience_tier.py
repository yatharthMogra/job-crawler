from __future__ import annotations

from typing import Literal

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

NEUTRAL_TIER_SCORE = 0.5
TIER_DISTANCE_STEP = 0.2

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


def tier_index(tier: str) -> int | None:
    normalized = normalize_experience_tier(tier)
    if normalized == "UNKNOWN":
        return None
    try:
        return EXPERIENCE_TIER_ORDER.index(normalized)
    except ValueError:
        return None


def tiers_above_ceiling(ceiling: str) -> frozenset[str]:
    ceiling_norm = normalize_experience_tier(ceiling)
    if ceiling_norm == "UNKNOWN":
        return frozenset()
    try:
        ceiling_idx = EXPERIENCE_TIER_ORDER.index(ceiling_norm)
    except ValueError:
        return frozenset()
    return frozenset(EXPERIENCE_TIER_ORDER[ceiling_idx + 1 :])


def experience_tier_distance_score(job_tier: str | None, candidate_tier: str | None) -> float:
    job_norm = normalize_experience_tier(job_tier)
    candidate_norm = normalize_experience_tier(candidate_tier)
    if job_norm == "UNKNOWN" or candidate_norm == "UNKNOWN":
        return NEUTRAL_TIER_SCORE
    job_idx = tier_index(job_norm)
    candidate_idx = tier_index(candidate_norm)
    if job_idx is None or candidate_idx is None:
        return NEUTRAL_TIER_SCORE
    distance = abs(job_idx - candidate_idx)
    return max(0.0, 1.0 - distance * TIER_DISTANCE_STEP)


def job_exceeds_visibility_ceiling(job_tier: str | None, ceiling: str) -> bool:
    normalized = normalize_experience_tier(job_tier)
    if normalized == "UNKNOWN":
        return False
    return normalized in tiers_above_ceiling(ceiling)
