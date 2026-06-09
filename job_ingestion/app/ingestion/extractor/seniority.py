from __future__ import annotations

import re
from typing import Literal, TypeVar

SeniorityLevel = Literal[
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
]

SENIORITY_LEVELS: tuple[str, ...] = (
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

_CANONICAL_ALIASES: dict[str, frozenset[str]] = {}


def _legacy_keys_for(canonical: str) -> set[str]:
    return {key for key, value in _LEGACY_TO_CANONICAL.items() if value == canonical}


for canonical in SENIORITY_LEVELS:
    _CANONICAL_ALIASES[canonical] = frozenset({canonical, *_legacy_keys_for(canonical)})


_TITLE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bintern(?:ship)?\b", re.I), "INTERN"),
    (
        re.compile(
            r"\bnew[\s-]?grad(?:uate)?\b|\buniversity[\s-]?grad\b|\baspire\b|\buniversity[\s-]?programs?\b",
            re.I,
        ),
        "NEW_GRAD",
    ),
    (re.compile(r"\b(?:director|vp|vice[\s-]?president|head[\s-]?of|executive)\b", re.I), "MANAGEMENT"),
    (re.compile(r"\b(?:engineering[\s-]?manager|tech[\s-]?lead(?:er)?|manager)\b", re.I), "MANAGEMENT"),
    (re.compile(r"\bprincipal\b", re.I), "PRINCIPAL"),
    (re.compile(r"\b(?:staff|distinguished)\b", re.I), "STAFF"),
    (re.compile(r"\b(?:senior|sr\.?)\b", re.I), "SENIOR"),
    (re.compile(r"\b(?:entry[\s-]?level|associate|junior|jr\.?)\b", re.I), "ENTRY"),
    (re.compile(r"\b(?:mid[\s-]?level|intermediate)\b", re.I), "MID"),
]

SENIORITY_PROMPT_RULES = (
    "seniority rules:\n"
    "- REQUIRED: one of INTERN, NEW_GRAD, ENTRY, JUNIOR, MID, SENIOR, STAFF, PRINCIPAL, "
    "MANAGEMENT, UNKNOWN\n"
    "- Use title and employment_type when provided; UNKNOWN only when truly ambiguous\n"
    "- INTERN: internships, co-ops, summer programs\n"
    "- NEW_GRAD: new grad, university grad, early career programs for recent graduates\n"
    "- ENTRY: entry-level, associate, junior IC roles (0-2 years)\n"
    "- JUNIOR: explicitly junior but not intern/new grad\n"
    "- MID: mid-level IC without senior/staff/principal in title\n"
    "- SENIOR: senior IC roles\n"
    "- STAFF: staff engineer or equivalent\n"
    "- PRINCIPAL: principal or distinguished IC\n"
    "- MANAGEMENT: manager, director, VP, head of, tech lead with people management\n\n"
    "is_internship and is_new_grad:\n"
    "- is_internship=true for internships/co-ops; must align with seniority=INTERN\n"
    "- is_new_grad=true for new grad/university programs; must align with seniority=NEW_GRAD\n"
    "- Do not set both is_internship and is_new_grad to true"
)

T = TypeVar("T")


def normalize_seniority(value: str | None) -> str:
    if not value:
        return "UNKNOWN"
    cleaned = value.strip()
    if cleaned in SENIORITY_LEVELS:
        return cleaned
    mapped = _LEGACY_TO_CANONICAL.get(cleaned.lower())
    if mapped:
        return mapped
    upper = cleaned.upper()
    if upper in SENIORITY_LEVELS:
        return upper
    return "UNKNOWN"


def expand_seniority_aliases(levels: set[str] | frozenset[str] | list[str]) -> set[str]:
    expanded: set[str] = set()
    for level in levels:
        canonical = normalize_seniority(level)
        expanded.update(_CANONICAL_ALIASES.get(canonical, {canonical}))
    return expanded


def infer_seniority_from_title(title: str) -> str | None:
    for pattern, level in _TITLE_PATTERNS:
        if pattern.search(title):
            return level
    return None


def infer_seniority_from_employment_type(employment_type: str | None) -> str | None:
    if not employment_type:
        return None
    lower = employment_type.lower()
    if "intern" in lower:
        return "INTERN"
    return None


def apply_seniority_consistency(
    seniority: str,
    is_internship: bool,
    is_new_grad: bool,
    *,
    title: str | None = None,
    employment_type: str | None = None,
) -> tuple[str, bool, bool]:
    normalized = normalize_seniority(seniority)

    hint = infer_seniority_from_title(title or "")
    if hint is None:
        hint = infer_seniority_from_employment_type(employment_type)

    if hint in ("INTERN", "NEW_GRAD"):
        normalized = hint
    elif hint and normalized == "UNKNOWN":
        normalized = hint

    if is_internship:
        normalized = "INTERN"
        is_new_grad = False
    elif is_new_grad:
        normalized = "NEW_GRAD"
        is_internship = False
    elif normalized == "INTERN":
        is_internship = True
        is_new_grad = False
    elif normalized == "NEW_GRAD":
        is_new_grad = True
        is_internship = False

    return normalized, is_internship, is_new_grad


def build_batch_job_payload(
    *,
    job_id: str,
    text: str,
    title: str | None = None,
    employment_type: str | None = None,
) -> dict[str, str]:
    payload: dict[str, str] = {"job_id": job_id, "text": text}
    if title:
        payload["title"] = title
    if employment_type:
        payload["employment_type"] = employment_type
    hint = infer_seniority_from_title(title or "") or infer_seniority_from_employment_type(employment_type)
    if hint:
        payload["seniority_hint"] = hint
    return payload
