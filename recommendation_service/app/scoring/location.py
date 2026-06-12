from __future__ import annotations

import re
from typing import Any

from app.scoring.country import extract_job_country, get_effective_countries

_SEGMENT_SPLIT = re.compile(r"[;•|/]+")
_PAREN_RE = re.compile(r"\([^)]*\)")
_NON_ALNUM = re.compile(r"[^a-z0-9\s,]+")

_STATE_ABBR_RE = re.compile(r",\s*([A-Z]{2})(?:\s*,|\s*$|\s+)")

_STATE_MAP = {
    "new york": "NY",
    "california": "CA",
    "washington": "WA",
    "texas": "TX",
    "massachusetts": "MA",
    "colorado": "CO",
    "virginia": "VA",
    "illinois": "IL",
    "georgia": "GA",
    "florida": "FL",
    "pennsylvania": "PA",
    "north carolina": "NC",
    "arizona": "AZ",
    "minnesota": "MN",
    "ohio": "OH",
}

_LOCATION_ALIASES: dict[str, set[str]] = {
    "new_york": {"new york", "nyc", "ny", "new york city", "manhattan", "brooklyn"},
    "san_francisco": {"san francisco", "sf", "bay area"},
    "los_angeles": {"los angeles", "la"},
    "new_jersey": {"new jersey", "nj", "jersey city", "newark"},
    "usa": {"usa", "us", "united states", "u s a"},
    "remote": {"remote", "anywhere", "work from home", "wfh"},
}

_CANONICAL_BY_TOKEN: dict[str, str] = {}
for canonical, aliases in _LOCATION_ALIASES.items():
    for alias in aliases:
        _CANONICAL_BY_TOKEN[alias] = canonical
    _CANONICAL_BY_TOKEN[canonical.replace("_", " ")] = canonical


def _normalize_text(value: str) -> str:
    cleaned = _PAREN_RE.sub(" ", value.lower())
    cleaned = _NON_ALNUM.sub(" ", cleaned)
    return " ".join(cleaned.split())


def _tokens_from_text(value: str) -> set[str]:
    normalized = _normalize_text(value)
    if not normalized:
        return set()

    tokens: set[str] = set()
    words = normalized.split()
    tokens.update(words)

    for size in (2, 3):
        for idx in range(len(words) - size + 1):
            phrase = " ".join(words[idx : idx + size])
            tokens.add(phrase)

    canonical: set[str] = set()
    for token in tokens:
        canonical.add(_CANONICAL_BY_TOKEN.get(token, token.replace(" ", "_")))
    return canonical


def split_job_location_segments(job_location: str | None) -> list[str]:
    if not job_location:
        return []

    raw = job_location.strip()
    segments: list[str] = []
    for part in _SEGMENT_SPLIT.split(raw):
        part = part.strip()
        if not part:
            continue
        if ";" in part:
            segments.extend(split_job_location_segments(part))
            continue
        segments.append(part)

    if not segments and raw:
        segments = [raw]
    return segments


def location_tokens(location: str) -> set[str]:
    tokens: set[str] = set()
    for segment in split_job_location_segments(location):
        tokens.update(_tokens_from_text(segment))
        if "," in segment:
            city, _, region = segment.partition(",")
            tokens.update(_tokens_from_text(city))
            tokens.update(_tokens_from_text(region))
    return tokens


def locations_match(preferred: str, job_location: str | None) -> bool:
    if not preferred or not job_location:
        return False

    preferred_tokens = location_tokens(preferred)
    job_tokens = location_tokens(job_location)
    if not preferred_tokens or not job_tokens:
        return False

    preferred_canonical = {_CANONICAL_BY_TOKEN.get(token, token) for token in preferred_tokens}
    job_canonical = {_CANONICAL_BY_TOKEN.get(token, token) for token in job_tokens}

    if preferred_canonical & job_canonical:
        return True

    preferred_text = _normalize_text(preferred)
    for segment in split_job_location_segments(job_location):
        segment_text = _normalize_text(segment)
        if preferred_text and preferred_text in segment_text:
            return True
        if segment_text and segment_text in preferred_text:
            return True
    return False


def _extract_state(location: str | None) -> str | None:
    if not location:
        return None
    match = _STATE_ABBR_RE.search(location)
    if match:
        return match.group(1)
    loc_lower = location.lower()
    for name, abbr in _STATE_MAP.items():
        if name in loc_lower:
            return abbr
    return None


def _extract_city(location: str | None) -> str | None:
    if not location:
        return None
    return location.split(",")[0].strip()


def _remote_accepts_candidate(remote_preference: str | None) -> bool:
    if not remote_preference:
        return True
    normalized = remote_preference.lower().strip()
    return normalized in {"remote", "hybrid", "hybrid_or_remote", "no_preference", "any"}


def _structured_location_score(
    job_location: str | None,
    job_country: str | None,
    remote_type: str,
    preferences: dict[str, Any],
    constraints: dict[str, Any],
) -> float | None:
    """Return score when structured country prefs or US-auth default applies; None to fall back."""
    preferred_countries = preferences.get("preferred_countries") or []
    preferred_states = preferences.get("preferred_states") or []
    preferred_cities = preferences.get("preferred_cities") or []
    has_structured = bool(preferred_countries or preferred_states or preferred_cities)

    effective_countries = get_effective_countries(preferences, constraints)
    if not has_structured and not effective_countries:
        return None

    if remote_type == "remote":
        if _remote_accepts_candidate(preferences.get("remote_preference")):
            return 1.0
        return 0.7

    if not effective_countries:
        return 0.5

    resolved_country = job_country or extract_job_country(job_location)
    if resolved_country is None:
        return 0.4

    if resolved_country not in effective_countries:
        return 0.15

    if preferred_states:
        job_state = _extract_state(job_location)
        if job_state and job_state.upper() in [str(s).upper() for s in preferred_states]:
            if preferred_cities:
                job_city = _extract_city(job_location)
                if job_city and job_city.lower() in [str(c).lower() for c in preferred_cities]:
                    return 1.0
                return 0.8
            return 0.9
        return 0.55

    return 0.75


def location_alignment_score(
    job_location: str | None,
    remote_type: str,
    preferences: dict[str, Any],
    *,
    job_country: str | None = None,
    constraints: dict[str, Any] | None = None,
) -> tuple[float, str | None]:
    constraints = constraints or {}
    structured = _structured_location_score(
        job_location,
        job_country,
        remote_type,
        preferences,
        constraints,
    )
    if structured is not None:
        return structured, None

    preferred_locations = preferences.get("preferred_locations") or []
    acceptable_locations = preferences.get("acceptable_locations") or []

    if not preferred_locations and not acceptable_locations:
        return 0.5, None

    if remote_type == "remote":
        if any(isinstance(loc, str) and loc.lower() == "remote" for loc in preferred_locations):
            return 1.0, "remote"
        return 0.7, "remote"

    for loc in preferred_locations:
        if isinstance(loc, str) and locations_match(loc, job_location):
            return 1.0, loc

    for loc in acceptable_locations:
        if isinstance(loc, str) and locations_match(loc, job_location):
            return 0.5, loc

    return 0.0, None
