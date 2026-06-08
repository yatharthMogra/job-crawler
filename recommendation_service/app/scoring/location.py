from __future__ import annotations

import re
from typing import Any

_SEGMENT_SPLIT = re.compile(r"[;•|/]+")
_PAREN_RE = re.compile(r"\([^)]*\)")
_NON_ALNUM = re.compile(r"[^a-z0-9\s,]+")

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

    preferred_canonical = {
        _CANONICAL_BY_TOKEN.get(token, token) for token in preferred_tokens
    }
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


def location_alignment_score(
    job_location: str | None,
    remote_type: str,
    preferences: dict[str, Any],
) -> tuple[float, str | None]:
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
