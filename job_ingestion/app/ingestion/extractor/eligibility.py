from __future__ import annotations

import re
from typing import Protocol, TypeVar

_CLEARANCE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"security clearance required", re.IGNORECASE),
    re.compile(r"requires?\s+(?:an?\s+)?(?:active\s+)?(?:top secret|secret|ts/sci|ts sci)", re.IGNORECASE),
    re.compile(r"must (?:hold|have|possess|maintain).{0,40}clearance", re.IGNORECASE),
    re.compile(r"must be (?:able|eligible) to (?:obtain|get|receive).{0,40}clearance", re.IGNORECASE),
    re.compile(r"eligible for (?:a\s+)?(?:top secret|secret|ts/sci|ts sci)", re.IGNORECASE),
    re.compile(r"active (?:top secret|secret|ts/sci|ts sci) clearance", re.IGNORECASE),
)

_CITIZENSHIP_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"u\.?s\.?\s+(?:citizen(?:ship)?|person).{0,30}(?:required|only|must)", re.IGNORECASE),
    re.compile(r"(?:must|required to) be (?:a )?u\.?s\.?\s+(?:citizen|person)", re.IGNORECASE),
    re.compile(r"united states (?:citizen(?:ship)?|person).{0,30}(?:required|only)", re.IGNORECASE),
    re.compile(r"will not sponsor", re.IGNORECASE),
    re.compile(r"(?:no|not|without|unable to|cannot|can't|do not|does not) (?:provide )?(?:visa )?sponsor", re.IGNORECASE),
    re.compile(r"not eligible for (?:visa )?sponsor", re.IGNORECASE),
    re.compile(r"no visa sponsorship", re.IGNORECASE),
    re.compile(r"sponsorship (?:is )?not available", re.IGNORECASE),
    re.compile(r"itar.{0,40}u\.?s\.?\s+person", re.IGNORECASE),
    re.compile(r"export control.{0,40}u\.?s\.?\s+person", re.IGNORECASE),
)


class _EligibilityFields(Protocol):
    requires_clearance: bool
    requires_citizenship: bool


T = TypeVar("T", bound=_EligibilityFields)


def detect_requires_clearance(description_text: str) -> bool:
    if not description_text.strip():
        return False
    return any(pattern.search(description_text) for pattern in _CLEARANCE_PATTERNS)


def detect_requires_citizenship(description_text: str) -> bool:
    if not description_text.strip():
        return False
    return any(pattern.search(description_text) for pattern in _CITIZENSHIP_PATTERNS)


def apply_eligibility_signals(
    enrichment: T,
    description_text: str | None,
) -> T:
    """Conservative merge: only flip false -> true from explicit JD text."""
    text = description_text or ""
    clearance = detect_requires_clearance(text)
    citizenship = detect_requires_citizenship(text)
    if not clearance and not citizenship:
        return enrichment
    return enrichment.model_copy(
        update={
            "requires_clearance": enrichment.requires_clearance or clearance,
            "requires_citizenship": enrichment.requires_citizenship or citizenship,
        }
    )
