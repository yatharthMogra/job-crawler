from __future__ import annotations

DEFAULT_TARGET_SENIORITY: tuple[str, ...] = ("INTERN", "NEW_GRAD", "ENTRY", "MID", "JUNIOR")

HARD_EXCLUDE_SENIORITIES = frozenset({"MANAGEMENT", "STAFF", "PRINCIPAL"})
SOFT_PENALTY_SENIORITIES = frozenset({"SENIOR"})

_LEGACY_TO_CANONICAL: dict[str, str] = {
    "intern": "INTERN",
    "internship": "INTERN",
    "new_grad": "NEW_GRAD",
    "newgrad": "NEW_GRAD",
    "entry": "ENTRY",
    "early_career": "ENTRY",
    "junior": "JUNIOR",
    "mid": "MID",
    "middle": "MID",
    "senior": "SENIOR",
    "staff": "STAFF",
    "principal": "PRINCIPAL",
    "management": "MANAGEMENT",
    "director": "MANAGEMENT",
    "vp": "MANAGEMENT",
    "c_level": "MANAGEMENT",
    "unclear": "UNKNOWN",
    "unknown": "UNKNOWN",
}

_CANONICAL_LEVELS = (
    "INTERN",
    "NEW_GRAD",
    "ENTRY",
    "JUNIOR",
    "MID",
    "SENIOR",
    "STAFF",
    "PRINCIPAL",
    "MANAGEMENT",
    "UNKNOWN",
)

_CANONICAL_ALIASES: dict[str, frozenset[str]] = {}


def _legacy_keys_for(canonical: str) -> set[str]:
    return {key for key, value in _LEGACY_TO_CANONICAL.items() if value == canonical}


for canonical in _CANONICAL_LEVELS:
    _CANONICAL_ALIASES[canonical] = frozenset({canonical, *_legacy_keys_for(canonical)})


def normalize_seniority(value: str | None) -> str:
    if not value:
        return "UNKNOWN"
    cleaned = value.strip()
    if cleaned in _CANONICAL_LEVELS:
        return cleaned
    mapped = _LEGACY_TO_CANONICAL.get(cleaned.lower())
    if mapped:
        return mapped
    upper = cleaned.upper()
    if upper in _CANONICAL_LEVELS:
        return upper
    return "UNKNOWN"


def expand_seniority_aliases(levels: set[str] | frozenset[str] | list[str]) -> set[str]:
    expanded: set[str] = set()
    for level in levels:
        canonical = normalize_seniority(level)
        expanded.update(_CANONICAL_ALIASES.get(canonical, {canonical}))
    return expanded


def get_target_seniority(constraints: dict) -> list[str]:
    raw = constraints.get("target_seniority")
    if isinstance(raw, list) and raw:
        return [normalize_seniority(str(item)) for item in raw]
    return list(DEFAULT_TARGET_SENIORITY)


def seniority_retrieval_values(target: list[str]) -> set[str]:
    target_set = {normalize_seniority(level) for level in target}
    return expand_seniority_aliases(target_set | {"UNKNOWN"})


def seniority_hard_block_values(target: list[str]) -> set[str]:
    target_set = {normalize_seniority(level) for level in target}
    blocked = HARD_EXCLUDE_SENIORITIES - target_set
    return expand_seniority_aliases(blocked)


def seniority_score_multiplier(job_seniority: str | None, constraints: dict) -> float:
    canonical = normalize_seniority(job_seniority)
    target = {normalize_seniority(level) for level in get_target_seniority(constraints)}
    if canonical in target or canonical == "UNKNOWN":
        return 1.0
    if canonical in SOFT_PENALTY_SENIORITIES:
        return 0.6
    return 1.0
