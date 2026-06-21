from __future__ import annotations

import re
from typing import Any, Optional
from urllib.parse import urlparse

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.base import BaseConnector
from app.models.company import Company

BASE_URL = "https://www.tesla.com"
DEFAULT_SITES = ["US"]
JOB_URL_PATTERN = re.compile(r"-(\d+)/?$")
TESLA_BOARD_TOKEN = "tesla"
TESLA_COMPANY_ID = "e686e4bd-4bd4-44c3-80ec-c196fffd9b49"


def _platform_config(company: Company) -> dict[str, Any]:
    config = company.platform_config
    return config if isinstance(config, dict) else {}


def is_manual_push_company(company: Company) -> bool:
    return _platform_config(company).get("ingestion_mode") == "manual_push"


def resolve_tesla_careers_config(company: Company) -> dict[str, Any]:
    config = _platform_config(company)
    sites = config.get("sites")
    if not isinstance(sites, list) or not sites:
        sites = list(DEFAULT_SITES)
    else:
        sites = [str(item).strip() for item in sites if str(item).strip()]
    if not sites:
        sites = list(DEFAULT_SITES)

    return {
        "sites": sites,
        "ingestion_mode": config.get("ingestion_mode"),
        "expected_push_interval_hours": int(config.get("expected_push_interval_hours", 4)),
    }


def extract_job_id_from_url(url: str) -> Optional[str]:
    path = urlparse(url).path.rstrip("/")
    match = JOB_URL_PATTERN.search(path)
    return match.group(1) if match else None


def build_tesla_job_url(job_path: str) -> str:
    normalized = job_path.strip()
    if not normalized:
        raise ParseError("Tesla job missing url path")
    if normalized.startswith("http://") or normalized.startswith("https://"):
        return normalized
    if not normalized.startswith("/"):
        normalized = f"/{normalized}"
    return f"{BASE_URL}{normalized}"


def _flatten_location_values(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    flattened: list[str] = []
    for value in values:
        if isinstance(value, list):
            flattened.extend(str(item) for item in value if item)
        elif value:
            flattened.append(str(value))
    return flattened


def find_country_site(geo: list[dict[str, Any]], site_code: str) -> Optional[dict[str, Any]]:
    for region in geo:
        if not isinstance(region, dict):
            continue
        sites = region.get("sites")
        if not isinstance(sites, list):
            continue
        for site in sites:
            if isinstance(site, dict) and site.get("id") == site_code:
                return site
    return None


def get_location_ids_in_country(
    site: dict[str, Any],
    *,
    city: str = "",
    state: str = "",
) -> list[str]:
    cities = site.get("cities")
    if isinstance(cities, dict):
        if not city:
            return _flatten_location_values(list(cities.values()))
        return [str(item) for item in _flatten_location_values([cities.get(city)]) if item]

    states = site.get("states")
    if not isinstance(states, list):
        return []

    if state:
        matched = next((entry for entry in states if isinstance(entry, dict) and entry.get("id") == state), None)
        if not isinstance(matched, dict):
            return []
        state_cities = matched.get("cities")
        if not isinstance(state_cities, dict):
            return []
        if not city:
            return _flatten_location_values(list(state_cities.values()))
        return [str(item) for item in _flatten_location_values([state_cities.get(city)]) if item]

    location_ids: list[str] = []
    for state_entry in states:
        if not isinstance(state_entry, dict):
            continue
        state_cities = state_entry.get("cities")
        if isinstance(state_cities, dict):
            location_ids.extend(_flatten_location_values(list(state_cities.values())))
    return location_ids


def filter_listings_by_site(state_data: dict[str, Any], site_code: str) -> list[dict[str, Any]]:
    listings = state_data.get("listings")
    if not isinstance(listings, list):
        raise ParseError("Tesla careers state response missing listings")

    geo = state_data.get("geo")
    if not isinstance(geo, list):
        raise ParseError("Tesla careers state response missing geo")

    site = find_country_site(geo, site_code)
    if site is None:
        return []

    allowed_location_ids = set(get_location_ids_in_country(site))
    if not allowed_location_ids:
        return []

    filtered: list[dict[str, Any]] = []
    for listing in listings:
        if not isinstance(listing, dict):
            continue
        location_id = listing.get("l")
        if location_id is None:
            continue
        if str(location_id) in allowed_location_ids:
            filtered.append(listing)
    return filtered


def iter_site_listings(
    state_data: dict[str, Any],
    sites: list[str],
) -> list[tuple[str, dict[str, Any]]]:
    summaries: list[tuple[str, dict[str, Any]]] = []
    seen_ids: set[str] = set()
    for site_code in sites:
        for listing in filter_listings_by_site(state_data, site_code):
            job_id = listing.get("id")
            if job_id is None:
                continue
            job_id_str = str(job_id)
            if job_id_str in seen_ids:
                continue
            seen_ids.add(job_id_str)
            summaries.append((site_code, listing))
    return summaries


def pending_tesla_detail_ids(
    state_data: dict[str, Any],
    sites: list[str],
    known_external_ids: set[str],
) -> list[str]:
    pending: list[str] = []
    for _site_code, listing in iter_site_listings(state_data, sites):
        job_id = listing.get("id")
        if job_id is None:
            continue
        job_id_str = str(job_id)
        if job_id_str not in known_external_ids:
            pending.append(job_id_str)
    return sorted(pending)


def build_tesla_jobs_from_push(
    state_data: dict[str, Any],
    details_by_id: dict[str, dict[str, Any]],
    *,
    sites: list[str],
    previous_raw_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    lookup = state_data.get("lookup") if isinstance(state_data.get("lookup"), dict) else {}
    jobs: list[dict[str, Any]] = []

    for site_code, listing in iter_site_listings(state_data, sites):
        job_id = listing.get("id")
        if job_id is None:
            continue
        job_id_str = str(job_id)
        detail = details_by_id.get(job_id_str)
        if detail is not None:
            jobs.append(
                normalize_tesla_job(
                    listing,
                    detail,
                    site=site_code,
                    lookup=lookup,
                )
            )
            continue
        if job_id_str in previous_raw_by_id:
            jobs.append(previous_raw_by_id[job_id_str])
            continue
        raise ParseError(f"Tesla job {job_id_str} is new but detail payload is missing")

    return jobs


def build_tesla_careers_html(job: dict[str, Any]) -> str:
    sections: list[str] = []

    metadata_parts: list[str] = []
    for label, key in (
        ("Department", "department"),
        ("Job family", "jobFamily"),
        ("Job type", "timeType"),
    ):
        value = job.get(key)
        if isinstance(value, str) and value.strip():
            metadata_parts.append(f"<strong>{label}:</strong> {value.strip()}")
    if metadata_parts:
        sections.append(f"<p>{' | '.join(metadata_parts)}</p>")

    for heading, key in (
        ("What to Expect", "jobDescription"),
        ("What You'll Do", "jobResponsibilities"),
        ("What You'll Bring", "jobRequirements"),
        ("Compensation and Benefits", "jobCompensationAndBenefits"),
    ):
        value = job.get(key)
        if isinstance(value, str) and value.strip():
            sections.append(f"<h3>{heading}</h3>{value.strip()}")

    description = job.get("description")
    if isinstance(description, str) and description.strip() and not sections:
        sections.append(description.strip())

    return "\n".join(sections)


def normalize_tesla_job(
    listing: dict[str, Any],
    detail: dict[str, Any],
    *,
    site: str,
    lookup: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    job_id = detail.get("id") or listing.get("id")
    if job_id is None:
        raise ParseError("Tesla job missing id")

    url_path = detail.get("url")
    if not isinstance(url_path, str) or not url_path.strip():
        title = detail.get("title") or listing.get("t") or str(job_id)
        slug = re.sub(r"[^a-z0-9]+", "-", str(title).lower()).strip("-")
        url_path = f"/careers/search/job/{slug}-{job_id}"

    department = detail.get("department")
    if not department and lookup:
        departments = lookup.get("departments")
        department_id = listing.get("dp")
        if isinstance(departments, dict) and department_id is not None:
            department = departments.get(str(department_id))

    location = detail.get("location")
    if not location and lookup:
        locations = lookup.get("locations")
        location_id = listing.get("l")
        if isinstance(locations, dict) and location_id is not None:
            location = locations.get(str(location_id))

    normalized = {
        **listing,
        **detail,
        "id": str(job_id),
        "title": detail.get("title") or listing.get("t") or "",
        "location": location or "",
        "department": department,
        "site": site,
        "externalLink": build_tesla_job_url(url_path),
        "raw_html": build_tesla_careers_html(detail),
    }
    return normalized


class TeslaCareersConnector(BaseConnector):
    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        raise ConnectorFetchError(
            "Tesla careers is push-only; use the manual browser bridge "
            "(scripts/tesla_careers_bridge.user.js)",
            None,
        )
