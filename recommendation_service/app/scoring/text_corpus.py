from __future__ import annotations

import re
from typing import Iterable

_TOKEN_RE = re.compile(r"[a-z0-9]+(?:'[a-z]+)?", re.IGNORECASE)
_PHRASE_SEP_RE = re.compile(r"[\s_/\-]+")


def normalize_phrase(value: str) -> str:
    return _PHRASE_SEP_RE.sub(" ", value.strip().lower())


def collect_protected_phrases(*phrase_groups: Iterable[str]) -> list[str]:
    phrases: list[str] = []
    seen: set[str] = set()
    for group in phrase_groups:
        for raw in group:
            phrase = normalize_phrase(raw)
            if len(phrase) < 2 or phrase in seen:
                continue
            seen.add(phrase)
            phrases.append(phrase)
    phrases.sort(key=len, reverse=True)
    return phrases


def tokenize_text(text: str, *, protected_phrases: Iterable[str] = ()) -> list[str]:
    if not text:
        return []
    lowered = text.lower()
    tokens: list[str] = []
    consumed = [False] * len(lowered)

    for phrase in collect_protected_phrases(protected_phrases):
        needle = phrase.lower()
        if not needle:
            continue
        start = 0
        while True:
            idx = lowered.find(needle, start)
            if idx < 0:
                break
            if not any(consumed[idx : idx + len(needle)]):
                for pos in range(idx, idx + len(needle)):
                    consumed[pos] = True
                tokens.append(needle.replace(" ", "_"))
            start = idx + len(needle)

    for match in _TOKEN_RE.finditer(lowered):
        if any(consumed[match.start() : match.end()]):
            continue
        tokens.append(match.group(0).lower())
    return tokens


def build_job_text(
    *,
    description_text: str | None,
    description_preview: str | None,
    responsibilities: list[str],
    required_qualifications: list[str],
    preferred_qualifications: list[str],
    tech_stack: list[str],
    skills: list[str],
) -> str:
    parts = [
        description_text or "",
        description_preview or "",
        *responsibilities,
        *required_qualifications,
        *preferred_qualifications,
        *tech_stack,
        *skills,
    ]
    return "\n".join(part.strip() for part in parts if part and part.strip())
