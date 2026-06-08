from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Optional

from app.exceptions import ParseError

def _extract_greenhouse_employment_type(metadata: Optional[list[dict[str, Any]]]) -> Optional[str]:
    if not metadata:
        return None
    for entry in metadata:
        name = str(entry.get("name", "")).lower()
        if "employment" in name or "type" in name:
            value = entry.get("value")
            if value:
                return str(value)
    return None


def _parse_iso_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def _parse_epoch_ms(value: Any) -> Optional[datetime]:
    if value in (None, ""):
        return None
    try:
        return datetime.fromtimestamp(float(value) / 1000.0, tz=timezone.utc)
    except (TypeError, ValueError):
        return None


def _extract_greenhouse(job: dict[str, Any]) -> dict[str, Any]:
    location = (job.get("location") or {}).get("name")
    departments = job.get("departments") or []
    department = departments[0].get("name") if departments else None
    metadata = job.get("metadata") or []
    return {
        "external_job_id": str(job.get("id")),
        "title": job.get("title") or "",
        "location": location,
        "department": department,
        "posting_url": job.get("absolute_url"),
        "posted_at": _parse_iso_datetime(job.get("updated_at")),
        "employment_type": _extract_greenhouse_employment_type(metadata),
        "raw_html": job.get("content") or "",
    }


def _extract_lever(job: dict[str, Any]) -> dict[str, Any]:
    categories = job.get("categories") or {}
    return {
        "external_job_id": str(job.get("id")),
        "title": job.get("text") or "",
        "location": categories.get("location"),
        "department": categories.get("department") or categories.get("team"),
        "posting_url": job.get("hostedUrl"),
        "posted_at": _parse_epoch_ms(job.get("createdAt")),
        "employment_type": categories.get("commitment"),
        "raw_html": job.get("description") or job.get("descriptionPlain") or "",
    }


def _extract_ashby(job: dict[str, Any]) -> dict[str, Any]:
    secondary_names = job.get("secondaryLocationNames")
    if isinstance(secondary_names, list):
        secondary_location_names = [name for name in secondary_names if name]
    else:
        secondary_locations = job.get("secondaryLocations") or []
        secondary_location_names = [loc.get("locationName") for loc in secondary_locations if loc.get("locationName")]
    location_parts = [job.get("locationName")] + secondary_location_names
    location = " | ".join([part for part in location_parts if part])
    return {
        "external_job_id": str(job.get("id")),
        "title": job.get("title") or "",
        "location": location or None,
        "department": job.get("departmentName"),
        "posting_url": job.get("externalLink"),
        "posted_at": _parse_iso_datetime(job.get("publishedDate") or job.get("publishedAt")),
        "employment_type": job.get("employmentType"),
        "raw_html": job.get("descriptionHtml") or "",
    }


FIELD_EXTRACTORS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "greenhouse": _extract_greenhouse,
    "lever": _extract_lever,
    "ashby": _extract_ashby,
}


def extract_deterministic_fields(job: dict[str, Any], platform: str = "greenhouse") -> dict[str, Any]:
    extractor = FIELD_EXTRACTORS.get(platform.lower())
    if extractor is None:
        raise ParseError(f"Unsupported extraction platform: {platform}")
    return extractor(job)
