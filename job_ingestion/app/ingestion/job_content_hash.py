from __future__ import annotations

import re
import unicodedata
from typing import Any

from app.ingestion.extractor.deterministic import extract_deterministic_fields
from app.ingestion.extractor.text_cleaner import clean_job_description
from app.utils.hashing import compute_content_hash

CANONICAL_HASH_VERSION = 2

_INVISIBLE_CHARS = re.compile(r"[\u200b-\u200d\ufeff]")
_MULTI_LOCATION_SUFFIX = re.compile(r"\s*;\s*\+\d+\s+more.*$", re.IGNORECASE)


def normalize_text_for_hash(text: str | None) -> str:
    if not text:
        return ""
    normalized = unicodedata.normalize("NFKC", text)
    normalized = _INVISIBLE_CHARS.sub("", normalized)
    normalized = normalized.replace("\u00a0", " ")
    return " ".join(normalized.split())


def normalize_metadata_for_hash(value: str | None) -> str:
    return normalize_text_for_hash(value).lower()


def normalize_location_for_hash(location: str | None) -> str:
    if not location:
        return ""
    stripped = _MULTI_LOCATION_SUFFIX.sub("", location)
    return normalize_metadata_for_hash(stripped)


def build_description_for_hash(job: dict[str, Any], fields: dict[str, Any]) -> str:
    description_candidates = [
        fields.get("raw_html"),
        job.get("raw_html"),
        job.get("content"),
        job.get("descriptionHtml"),
        job.get("description"),
        job.get("descriptionPlain"),
    ]
    for candidate in description_candidates:
        cleaned = clean_job_description(candidate if isinstance(candidate, str) else None)
        if cleaned:
            return normalize_text_for_hash(cleaned)
    return ""


def build_canonical_hash_payload(job: dict[str, Any], platform: str) -> dict[str, Any]:
    fields = extract_deterministic_fields(job, platform=platform)
    company_label = fields.get("department") or fields.get("company_name") or ""
    return {
        "v": CANONICAL_HASH_VERSION,
        "title": normalize_metadata_for_hash(fields.get("title")),
        "company": normalize_metadata_for_hash(company_label),
        "location": normalize_location_for_hash(fields.get("location")),
        "employment_type": normalize_metadata_for_hash(fields.get("employment_type")),
        "description": build_description_for_hash(job, fields),
    }


def compute_job_content_hash(job: dict[str, Any], platform: str) -> str:
    return compute_content_hash(build_canonical_hash_payload(job, platform))
