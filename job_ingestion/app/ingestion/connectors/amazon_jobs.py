from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Optional

import httpx

try:
    import structlog
except ImportError:  # pragma: no cover
    structlog = None

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.base import BaseConnector
from app.models.company import Company

logger = structlog.get_logger(__name__) if structlog else logging.getLogger(__name__)

BASE_URL = "https://www.amazon.jobs"
PAGE_SIZE = 100
PAGE_DELAY = 0.5
REQUEST_TIMEOUT = 30.0
USER_AGENT = "Mozilla/5.0 (compatible; CareerMatchBot/1.0)"

DEFAULT_JOB_CATEGORIES = [
    "software-development",
    "data-science",
    "research-science",
    "project-program-product-management-technical",
    "hardware-development",
    "solutions-architect",
]

DEFAULT_EXCLUDE_JOB_CATEGORIES = [
    "Fulfillment & Operations Management",
    "Medical, Health, & Safety",
]

DEFAULT_EXCLUDE_JOB_FAMILIES = [
    "Fulfillment Center",
    "Fulfillment Associates",
]


def _platform_config(company: Company) -> dict[str, Any]:
    config = company.platform_config
    return config if isinstance(config, dict) else {}


def resolve_amazon_jobs_config(company: Company) -> dict[str, Any]:
    config = _platform_config(company)
    locale = config.get("locale") or "en"
    if not isinstance(locale, str) or not locale.strip():
        locale = "en"

    job_categories = config.get("job_categories")
    if not isinstance(job_categories, list) or not job_categories:
        job_categories = list(DEFAULT_JOB_CATEGORIES)
    else:
        job_categories = [str(item).strip() for item in job_categories if str(item).strip()]

    exclude_job_categories = config.get("exclude_job_categories")
    if not isinstance(exclude_job_categories, list) or not exclude_job_categories:
        exclude_job_categories = list(DEFAULT_EXCLUDE_JOB_CATEGORIES)
    else:
        exclude_job_categories = [
            str(item).strip() for item in exclude_job_categories if str(item).strip()
        ]

    exclude_job_families = config.get("exclude_job_families")
    if not isinstance(exclude_job_families, list) or not exclude_job_families:
        exclude_job_families = list(DEFAULT_EXCLUDE_JOB_FAMILIES)
    else:
        exclude_job_families = [
            str(item).strip() for item in exclude_job_families if str(item).strip()
        ]

    return {
        "locale": locale.strip(),
        "job_categories": job_categories,
        "exclude_job_categories": exclude_job_categories,
        "exclude_job_families": exclude_job_families,
    }


def search_url_for_locale(locale: str) -> str:
    normalized = locale.strip().strip("/")
    return f"{BASE_URL}/{normalized}/search.json"


def build_amazon_search_params(
    config: dict[str, Any],
    *,
    offset: int,
    page_size: int,
) -> list[tuple[str, str | int]]:
    params: list[tuple[str, str | int]] = [
        ("offset", offset),
        ("result_limit", page_size),
    ]
    for category in config.get("job_categories") or []:
        params.append(("category[]", category))
    return params


def parse_amazon_posted_date(value: object) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped:
        return None
    try:
        return datetime.strptime(stripped, "%B %d, %Y")
    except ValueError:
        return None


def _parse_location_entry(raw: object) -> Optional[str]:
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(parsed, dict):
        return None
    normalized = parsed.get("normalizedLocation") or parsed.get("location")
    if isinstance(normalized, str) and normalized.strip():
        return normalized.strip()
    return None


def build_amazon_job_location(job: dict[str, Any]) -> str:
    normalized = job.get("normalized_location")
    if isinstance(normalized, str) and normalized.strip():
        primary = normalized.strip()
    else:
        primary = ""

    locations = job.get("locations")
    if not isinstance(locations, list):
        return primary

    parts: list[str] = []
    seen: set[str] = set()
    if primary:
        parts.append(primary)
        seen.add(primary.lower())

    for entry in locations:
        loc = _parse_location_entry(entry)
        if not loc:
            continue
        key = loc.lower()
        if key in seen:
            continue
        seen.add(key)
        parts.append(loc)

    if parts:
        return " | ".join(parts)

    location = job.get("location")
    if isinstance(location, str) and location.strip():
        return location.strip()
    return ""


def should_exclude_amazon_job(job: dict[str, Any], config: dict[str, Any]) -> bool:
    job_category = job.get("job_category")
    if isinstance(job_category, str) and job_category in config.get("exclude_job_categories", []):
        return True

    job_family = job.get("job_family")
    if isinstance(job_family, str) and job_family in config.get("exclude_job_families", []):
        return True

    return False


def build_amazon_jobs_html(job: dict[str, Any]) -> str:
    sections: list[str] = []

    metadata_parts: list[str] = []
    for label, key in (
        ("Business unit", "business_category"),
        ("Job category", "job_category"),
        ("Job family", "job_family"),
    ):
        value = job.get(key)
        if isinstance(value, str) and value.strip():
            metadata_parts.append(f"<strong>{label}:</strong> {value.strip()}")
    if metadata_parts:
        sections.append(f"<p>{' | '.join(metadata_parts)}</p>")

    for heading, key in (
        ("Description", "description"),
        ("Basic Qualifications", "basic_qualifications"),
        ("Preferred Qualifications", "preferred_qualifications"),
    ):
        value = job.get(key)
        if isinstance(value, str) and value.strip():
            sections.append(f"<h3>{heading}</h3>{value.strip()}")

    return "\n".join(sections)


def normalize_amazon_job(raw: dict[str, Any]) -> dict[str, Any]:
    job_id = raw.get("id_icims")
    if job_id is None:
        raise ParseError("Amazon job missing id_icims")

    job_path = raw.get("job_path")
    if not isinstance(job_path, str) or not job_path.strip():
        raise ParseError(f"Amazon job {job_id} missing job_path")

    normalized = dict(raw)
    normalized["id"] = str(job_id)
    normalized["externalLink"] = f"{BASE_URL}{job_path}"
    normalized["raw_html"] = build_amazon_jobs_html(raw)
    return normalized


class AmazonJobsConnector(BaseConnector):
    page_size = PAGE_SIZE
    page_delay = PAGE_DELAY

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        config = resolve_amazon_jobs_config(company)
        if not config["job_categories"]:
            raise ParseError(
                f"Amazon Jobs fetch for {company.board_token} requires job_categories"
            )

        search_url = search_url_for_locale(config["locale"])
        headers = {"User-Agent": USER_AGENT}
        results: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        offset = 0
        total_hits: Optional[int] = None

        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT, headers=headers) as client:
                while True:
                    params = build_amazon_search_params(
                        config,
                        offset=offset,
                        page_size=self.page_size,
                    )
                    response = await client.get(search_url, params=params)
                    response.raise_for_status()
                    data = response.json()

                    if not isinstance(data, dict):
                        raise ParseError(
                            f"Malformed Amazon Jobs response for {company.board_token}"
                        )

                    jobs = data.get("jobs")
                    if jobs is None:
                        raise ParseError(
                            f"Malformed Amazon Jobs response for {company.board_token}"
                        )
                    if not isinstance(jobs, list):
                        raise ParseError(
                            f"Malformed Amazon Jobs response for {company.board_token}"
                        )

                    hits = data.get("hits")
                    if isinstance(hits, int):
                        total_hits = hits
                        if hits == 10000:
                            if structlog:
                                logger.warning(
                                    "amazon_jobs_hits_capped",
                                    board_token=company.board_token,
                                    hits=hits,
                                )
                            else:
                                logger.warning(
                                    "amazon_jobs_hits_capped board_token=%s hits=%s",
                                    company.board_token,
                                    hits,
                                )

                    if not jobs:
                        break

                    for raw_job in jobs:
                        if not isinstance(raw_job, dict):
                            continue
                        if should_exclude_amazon_job(raw_job, config):
                            continue
                        try:
                            job = normalize_amazon_job(raw_job)
                        except ParseError:
                            continue
                        job_id = job.get("id")
                        if not job_id or job_id in seen_ids:
                            continue
                        seen_ids.add(str(job_id))
                        results.append(job)

                    offset += self.page_size
                    if total_hits is not None and offset >= total_hits:
                        break
                    if len(jobs) < self.page_size:
                        break
                    await asyncio.sleep(self.page_delay)
        except ParseError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise ConnectorFetchError(
                f"Amazon Jobs fetch failed for {company.board_token}: {exc}"
            ) from exc

        return results
