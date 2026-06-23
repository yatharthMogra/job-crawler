from __future__ import annotations

import html
import logging
import re
from typing import Any, Optional

import httpx

try:
    from curl_cffi.requests import AsyncSession
except ImportError:  # pragma: no cover
    AsyncSession = None  # type: ignore[misc, assignment]

try:
    import structlog
except ImportError:  # pragma: no cover
    structlog = None

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.base import BaseConnector
from app.models.company import Company

logger = structlog.get_logger(__name__) if structlog else logging.getLogger(__name__)

BASE_URL = "https://www.uber.com"
SEARCH_PATH = "/api/loadSearchJobsResults"
DEFAULT_LOCALE_PATH = "us/en"
PAGE_SIZE = 50
PAGE_DELAY = 0.3
REQUEST_TIMEOUT = 30.0
USER_AGENT = "Mozilla/5.0 (compatible; CareerMatchBot/1.0)"
BROWSER_IMPERSONATE = "chrome120"
CSRF_TOKEN = "x"

DEFAULT_SEARCH_PARAMS: dict[str, Any] = {
    "department": [],
    "lineOfBusinessName": [],
    "location": [],
    "programAndPlatform": [],
    "query": "",
    "team": [],
    "type": [],
}

BLOCKED_STATUS_CODES = frozenset({403, 406, 429})


def _platform_config(company: Company) -> dict[str, Any]:
    config = company.platform_config
    return config if isinstance(config, dict) else {}


def resolve_uber_careers_config(company: Company) -> dict[str, Any]:
    config = _platform_config(company)
    locale_path = config.get("locale_path") or DEFAULT_LOCALE_PATH
    if not isinstance(locale_path, str) or not locale_path.strip():
        locale_path = DEFAULT_LOCALE_PATH
    locale_path = locale_path.strip().strip("/")

    search_params = config.get("search_params")
    if not isinstance(search_params, dict):
        search_params = dict(DEFAULT_SEARCH_PARAMS)
    else:
        merged = dict(DEFAULT_SEARCH_PARAMS)
        merged.update(search_params)
        search_params = merged

    return {
        "locale_path": locale_path,
        "search_params": search_params,
    }


def careers_list_url(locale_path: str) -> str:
    return f"{BASE_URL}/{locale_path}/careers/list/"


def build_uber_search_body(
    *,
    limit: int,
    offset: int,
    params: dict[str, Any],
) -> dict[str, Any]:
    return {
        "limit": limit,
        "offset": offset,
        "params": params,
    }


def parse_uber_total_results(total_results: object) -> Optional[int]:
    if isinstance(total_results, int):
        return total_results
    if isinstance(total_results, dict):
        low = total_results.get("low")
        if isinstance(low, int):
            return low
        if isinstance(low, str) and low.isdigit():
            return int(low)
    return None


def _format_location_entry(entry: object) -> Optional[str]:
    if not isinstance(entry, dict):
        return None
    parts = [
        entry.get("city"),
        entry.get("region"),
        entry.get("countryName") or entry.get("country"),
    ]
    formatted = ", ".join(str(part).strip() for part in parts if part and str(part).strip())
    return formatted or None


def build_uber_job_location(job: dict[str, Any]) -> str:
    all_locations = job.get("allLocations")
    if isinstance(all_locations, list) and all_locations:
        parts: list[str] = []
        seen: set[str] = set()
        for entry in all_locations:
            loc = _format_location_entry(entry)
            if not loc:
                continue
            key = loc.lower()
            if key in seen:
                continue
            seen.add(key)
            parts.append(loc)
        if parts:
            return " | ".join(parts)

    single = _format_location_entry(job.get("location"))
    return single or ""


def build_uber_job_url(job_id: object, locale_path: str) -> str:
    return f"{BASE_URL}/{locale_path.strip('/')}/careers/list/{job_id}/"


def _description_to_html(description: str) -> str:
    stripped = description.strip()
    if not stripped:
        return ""
    paragraphs = re.split(r"\n\s*\n", stripped)
    html_parts: list[str] = []
    for paragraph in paragraphs:
        text = paragraph.strip()
        if not text:
            continue
        escaped = html.escape(text)
        escaped = escaped.replace("\n", "<br>")
        html_parts.append(f"<p>{escaped}</p>")
    return "\n".join(html_parts)


def build_uber_careers_html(job: dict[str, Any]) -> str:
    sections: list[str] = []

    metadata_parts: list[str] = []
    for label, key in (
        ("Department", "department"),
        ("Team", "team"),
        ("Employment type", "timeType"),
    ):
        value = job.get(key)
        if isinstance(value, str) and value.strip():
            metadata_parts.append(f"<strong>{label}:</strong> {html.escape(value.strip())}")
    if metadata_parts:
        sections.append(f"<p>{' | '.join(metadata_parts)}</p>")

    description = job.get("description")
    if isinstance(description, str) and description.strip():
        sections.append(_description_to_html(description))

    return "\n".join(sections)


def normalize_uber_job(raw: dict[str, Any], *, locale_path: str) -> dict[str, Any]:
    job_id = raw.get("id")
    if job_id is None:
        raise ParseError("Uber job missing id")

    normalized = dict(raw)
    normalized["id"] = str(job_id)
    normalized["title"] = raw.get("title") or ""
    normalized["location"] = build_uber_job_location(raw)
    normalized["externalLink"] = build_uber_job_url(job_id, locale_path)
    normalized["raw_html"] = build_uber_careers_html(raw)
    return normalized


def _search_headers(locale_path: str) -> dict[str, str]:
    return {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-csrf-token": CSRF_TOKEN,
        "Referer": careers_list_url(locale_path),
    }


def _careers_page_headers() -> dict[str, str]:
    return {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    }


def _parse_search_response(data: object, board_token: str) -> tuple[list[dict[str, Any]], Optional[int]]:
    if not isinstance(data, dict):
        raise ParseError(f"Malformed Uber Careers response for {board_token}")
    if data.get("status") != "success":
        raise ParseError(f"Malformed Uber Careers response for {board_token}")

    payload = data.get("data")
    if not isinstance(payload, dict):
        raise ParseError(f"Malformed Uber Careers response for {board_token}")

    results = payload.get("results")
    if not isinstance(results, list):
        raise ParseError(f"Malformed Uber Careers response for {board_token}")

    total = parse_uber_total_results(payload.get("totalResults"))
    jobs = [item for item in results if isinstance(item, dict)]
    return jobs, total


class UberCareersConnector(BaseConnector):
    page_size = PAGE_SIZE
    page_delay = PAGE_DELAY
    max_limit = 1000

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        config = resolve_uber_careers_config(company)
        locale_path = config["locale_path"]
        search_params = config["search_params"]
        headers = _search_headers(locale_path)
        list_url = careers_list_url(locale_path)
        search_url = f"{BASE_URL}{SEARCH_PATH}"

        try:
            async with httpx.AsyncClient(
                timeout=REQUEST_TIMEOUT,
                headers=headers,
                follow_redirects=True,
            ) as client:
                probe_body = build_uber_search_body(
                    limit=self.page_size,
                    offset=0,
                    params=search_params,
                )
                probe_jobs, total = await self._post_search_page(
                    client=client,
                    search_url=search_url,
                    list_url=list_url,
                    body=probe_body,
                    board_token=company.board_token,
                    locale_path=locale_path,
                )

                if total is None:
                    total = len(probe_jobs)

                if total <= len(probe_jobs):
                    raw_jobs = probe_jobs
                else:
                    fetch_limit = min(total, self.max_limit)
                    full_body = build_uber_search_body(
                        limit=fetch_limit,
                        offset=0,
                        params=search_params,
                    )
                    raw_jobs, full_total = await self._post_search_page(
                        client=client,
                        search_url=search_url,
                        list_url=list_url,
                        body=full_body,
                        board_token=company.board_token,
                        locale_path=locale_path,
                    )
                    if full_total is not None:
                        total = full_total
                    if total > fetch_limit:
                        if structlog:
                            logger.warning(
                                "uber_careers_total_exceeds_max_limit",
                                board_token=company.board_token,
                                total=total,
                                fetch_limit=fetch_limit,
                            )
                        else:
                            logger.warning(
                                "uber_careers_total_exceeds_max_limit board_token=%s total=%s fetch_limit=%s",
                                company.board_token,
                                total,
                                fetch_limit,
                            )
        except ParseError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise ConnectorFetchError(
                f"Uber Careers fetch failed for {company.board_token}: {exc}"
            ) from exc

        results: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        for raw_job in raw_jobs:
            job_id = raw_job.get("id")
            if job_id is None:
                continue
            job_id_str = str(job_id)
            if job_id_str in seen_ids:
                continue
            seen_ids.add(job_id_str)
            results.append(normalize_uber_job(raw_job, locale_path=locale_path))

        return results

    async def _post_search_page(
        self,
        *,
        client: httpx.AsyncClient,
        search_url: str,
        list_url: str,
        body: dict[str, Any],
        board_token: str,
        locale_path: str,
    ) -> tuple[list[dict[str, Any]], Optional[int]]:
        response = await client.post(search_url, json=body)
        if response.status_code not in BLOCKED_STATUS_CODES:
            response.raise_for_status()
            return _parse_search_response(response.json(), board_token)

        await client.get(list_url, headers=_careers_page_headers())
        response = await client.post(search_url, json=body)
        if response.status_code not in BLOCKED_STATUS_CODES:
            response.raise_for_status()
            return _parse_search_response(response.json(), board_token)

        if AsyncSession is None:
            raise ConnectorFetchError(
                f"Uber Careers fetch blocked for {board_token} (HTTP {response.status_code})",
                None,
            )

        async with AsyncSession(
            impersonate=BROWSER_IMPERSONATE,
            timeout=REQUEST_TIMEOUT,
        ) as session:
            session.headers.update(_search_headers(locale_path))
            await session.get(list_url, headers=_careers_page_headers())
            fallback = await session.post(search_url, json=body)
            if fallback.status_code >= 400:
                raise ConnectorFetchError(
                    f"Uber Careers fetch blocked for {board_token} (HTTP {fallback.status_code})",
                    None,
                )
            return _parse_search_response(fallback.json(), board_token)
