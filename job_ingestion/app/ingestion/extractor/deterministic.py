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


def _parse_workday_date(date_str: Optional[str]) -> Optional[datetime]:
    if not date_str:
        return None
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


_WORKDAY_SCHEDULE_MAP = {
    "Full_Time": "Full-time",
    "Part_Time": "Part-time",
    "Temporary": "Temporary",
    "Internship": "Internship",
    "Contract": "Contract",
}


def _extract_workday_employment_type(job: dict[str, Any]) -> Optional[str]:
    info = job.get("jobPostingInfo") or {}
    schedule = info.get("jobScheduleType", "")
    if schedule in _WORKDAY_SCHEDULE_MAP:
        return _WORKDAY_SCHEDULE_MAP[schedule]
    for bullet in job.get("bulletFields", []):
        lowered = str(bullet).lower()
        if "full" in lowered:
            return "Full-time"
        if "intern" in lowered:
            return "Internship"
        if "part" in lowered:
            return "Part-time"
        if "contract" in lowered:
            return "Contract"
    return None


def _extract_workday_location(job: dict[str, Any], info: dict[str, Any]) -> Optional[str]:
    locations = info.get("locations")
    if isinstance(locations, list):
        names = [loc.get("locationName") or loc.get("name") for loc in locations if isinstance(loc, dict)]
        names = [name for name in names if name]
        if names:
            return " | ".join(names)
    for key in ("location", "locationsText"):
        value = info.get(key) or job.get(key)
        if value:
            return str(value)
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


def _extract_workday(job: dict[str, Any]) -> dict[str, Any]:
    info = job.get("jobPostingInfo") or {}
    return {
        "external_job_id": str(job.get("id")),
        "title": info.get("title") or job.get("title") or "",
        "location": _extract_workday_location(job, info),
        "department": info.get("department") or info.get("supervisoryOrganization"),
        "posting_url": job.get("externalLink"),
        "posted_at": _parse_workday_date(
            info.get("startDate") or info.get("postedOn") or job.get("postedOn")
        ),
        "employment_type": _extract_workday_employment_type(job),
        "raw_html": info.get("jobDescription") or "",
    }


def _parse_oracle_date(date_str: Optional[str]) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _extract_oracle_employment_type(job: dict[str, Any]) -> Optional[str]:
    for field in job.get("requisitionFlexFields", []):
        if not isinstance(field, dict):
            continue
        prompt = (field.get("Prompt") or "").lower()
        if "employment" in prompt or "type" in prompt or "schedule" in prompt:
            value = field.get("Value")
            if value:
                return str(value)

    workplace = job.get("WorkplaceType")
    if workplace:
        return str(workplace)

    return None


def _build_oracle_description_html(job: dict[str, Any]) -> str:
    parts: list[str] = []
    for field in ("ExternalDescriptionStr", "ExternalQualificationsStr", "ExternalResponsibilitiesStr"):
        val = (job.get(field) or "").strip()
        if val:
            parts.append(val)
    return "\n".join(parts)


def _extract_oracle_hcm(job: dict[str, Any]) -> dict[str, Any]:
    locations: list[str] = []
    primary = job.get("PrimaryLocation")
    if primary:
        locations.append(str(primary))
    for loc in job.get("otherWorkLocations", []):
        if not isinstance(loc, dict):
            continue
        name = loc.get("Name") or loc.get("LocationName")
        if name and name not in locations:
            locations.append(str(name))
    location_str = " | ".join(locations) or None

    return {
        "external_job_id": str(job.get("id")),
        "title": job.get("Title") or "",
        "location": location_str,
        "department": job.get("Category"),
        "posting_url": job.get("externalLink"),
        "posted_at": _parse_oracle_date(job.get("PostedDate")),
        "employment_type": _extract_oracle_employment_type(job),
        "raw_html": _build_oracle_description_html(job),
    }


def _parse_icims_date(date_str: Optional[str]) -> Optional[datetime]:
    if not date_str:
        return None
    normalized = date_str.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(normalized)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        return None


def _extract_icims_employment_type(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    raw_lower = raw.lower()
    if "full" in raw_lower:
        return "Full-time"
    if "part" in raw_lower:
        return "Part-time"
    if "intern" in raw_lower:
        return "Internship"
    if "contract" in raw_lower:
        return "Contract"
    if "temporary" in raw_lower or "temp" in raw_lower:
        return "Temporary"
    return raw


def _extract_icims(job: dict[str, Any]) -> dict[str, Any]:
    posting_url = job.get("sitemap_url")
    if not posting_url:
        detail_url = job.get("detail_url", "")
        posting_url = detail_url.replace("?in_iframe=1", "").replace("&in_iframe=1", "")

    return {
        "external_job_id": str(job["id"]),
        "title": job.get("title"),
        "location": job.get("location"),
        "department": job.get("department"),
        "posting_url": posting_url,
        "posted_at": _parse_icims_date(job.get("lastmod")),
        "employment_type": _extract_icims_employment_type(job.get("employment_type_raw")),
        "raw_html": job.get("raw_html", ""),
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
    "workday": _extract_workday,
    "oracle_hcm": _extract_oracle_hcm,
    "icims": _extract_icims,
}


def extract_deterministic_fields(job: dict[str, Any], platform: str = "greenhouse") -> dict[str, Any]:
    extractor = FIELD_EXTRACTORS.get(platform.lower())
    if extractor is None:
        raise ParseError(f"Unsupported extraction platform: {platform}")
    return extractor(job)
