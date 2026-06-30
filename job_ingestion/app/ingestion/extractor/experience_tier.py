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

EXPERIENCE_TIER_PROMPT_RULES = (
    "experience_tier rules (domain-agnostic; separate from seniority field):\n"
    "- REQUIRED: one of INTERN, NEW_GRAD, JUNIOR, MID, SENIOR, ABOVE_SENIOR, UNKNOWN\n"
    "- Classify the level of professional experience a realistic candidate needs\n"
    "- Do NOT extract literal years of experience; use judgment from title, tone, and responsibilities\n"
    "- Weight responsibilities and expectations at least as heavily as the job title\n"
    "- Title alone is unreliable (e.g. 'Senior Analyst' at one company may be junior elsewhere)\n"
    "- INTERN: internships, co-ops, summer programs for students still in school\n"
    "- NEW_GRAD: new graduate or university programs expecting a completed degree soon\n"
    "- JUNIOR: early-career roles with limited prior full-time experience expected\n"
    "- MID: solid individual contributor experience expected; owns meaningful workstreams\n"
    "- SENIOR: experienced IC or equivalent; leads projects or mentors others\n"
    "- ABOVE_SENIOR: staff/principal/distinguished IC, engineering manager, director, VP, "
    "head of, or org-level leadership regardless of domain\n"
    "- UNKNOWN: only when the posting gives nothing usable to classify confidently\n"
    "- Applies across all domains (software, finance, operations, design, etc.)"
)


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
    """Return tier labels strictly above the ceiling (UNKNOWN never hidden)."""
    ceiling_norm = normalize_experience_tier(ceiling)
    if ceiling_norm == "UNKNOWN":
        return frozenset()
    try:
        ceiling_idx = EXPERIENCE_TIER_ORDER.index(ceiling_norm)
    except ValueError:
        return frozenset()
    return frozenset(EXPERIENCE_TIER_ORDER[ceiling_idx + 1 :])


def apply_experience_tier_consistency(
    experience_tier: str,
    is_internship: bool,
    is_new_grad: bool,
) -> str:
    normalized = normalize_experience_tier(experience_tier)
    if is_internship:
        return "INTERN"
    if is_new_grad:
        return "NEW_GRAD"
    if normalized == "INTERN" and not is_new_grad:
        return "INTERN"
    if normalized == "NEW_GRAD" and not is_internship:
        return "NEW_GRAD"
    return normalized
