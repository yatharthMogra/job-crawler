from __future__ import annotations

from typing import Any

# String column limits on normalized_jobs / job_archive / raw_jobs.
_FIELD_LIMITS: dict[str, int] = {
    "external_job_id": 255,
    "title": 512,
    "company_name": 255,
    "location": 255,
    "job_country": 2,
    "department": 255,
    "employment_type": 255,
    "dedup_fingerprint": 200,
}


def clamp_str(value: str | None, max_len: int) -> str | None:
    if value is None:
        return None
    text = str(value)
    if len(text) <= max_len:
        return text
    return text[:max_len]


def clamp_deterministic_fields(fields: dict[str, Any]) -> dict[str, Any]:
    """Truncate string fields to fit DB column limits before insert."""
    clamped = dict(fields)
    for key, max_len in _FIELD_LIMITS.items():
        if key not in clamped:
            continue
        clamped[key] = clamp_str(clamped.get(key), max_len)
    return clamped
