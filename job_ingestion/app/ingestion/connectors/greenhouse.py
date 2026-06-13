from __future__ import annotations

import asyncio
import logging
import re
from typing import Any
from urllib.parse import urlparse

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

BROWSER_IMPERSONATE = "chrome120"
REQUEST_TIMEOUT = 30.0
DETAIL_CONCURRENCY = 4
DETAIL_DELAY = 0.2

GH_JID_PATTERN = re.compile(r"gh_jid=(\d+)", re.IGNORECASE)
GH_BOARD_JOB_PATTERN = re.compile(
    r"(?:boards|job-boards)\.greenhouse\.io/[^/\"'\s]+/jobs/(\d+)",
    re.IGNORECASE,
)
CAREERS_JOB_PATH_PATTERN = re.compile(r"/jobs/(\d+)(?:[/?\"'\s]|$)", re.IGNORECASE)

GREENHOUSE_SIGNALS = (
    "greenhouse",
    "gh_jid",
    "boards-api.greenhouse.io",
    "boards.greenhouse.io",
    "job-boards.greenhouse.io",
    "?for=",
)


def _platform_config(company: Company) -> dict[str, Any]:
    config = company.platform_config
    return config if isinstance(config, dict) else {}


def _careers_urls(company: Company) -> list[str]:
    config = _platform_config(company)
    urls: list[str] = []
    primary = config.get("careers_url")
    if primary:
        urls.append(str(primary).strip())
    extras = config.get("careers_urls")
    if isinstance(extras, list):
        for item in extras:
            if item:
                urls.append(str(item).strip())
    seen: set[str] = set()
    result: list[str] = []
    for url in urls:
        if url and url not in seen:
            seen.add(url)
            result.append(url)
    return result


def _board_token(company: Company) -> str:
    config = _platform_config(company)
    override = config.get("board_token_override")
    if override:
        return str(override)
    return company.board_token


def _should_validate_domain(company: Company) -> bool:
    config = _platform_config(company)
    if "validate_absolute_url_domain" in config:
        return bool(config["validate_absolute_url_domain"])
    return bool(_careers_urls(company))


def _root_domain(url_or_host: str) -> str:
    if "://" in url_or_host:
        host = urlparse(url_or_host).netloc
    else:
        host = url_or_host
    host = host.lower().removeprefix("www.")
    parts = host.split(".")
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return host


def discover_job_ids_from_html(html: str, page_url: str = "") -> set[str]:
    """Extract Greenhouse job IDs from careers page HTML."""
    ids: set[str] = set()

    for match in GH_JID_PATTERN.finditer(html):
        ids.add(match.group(1))

    for match in GH_BOARD_JOB_PATTERN.finditer(html):
        ids.add(match.group(1))

    has_greenhouse_signal = any(signal.lower() in html.lower() for signal in GREENHOUSE_SIGNALS)
    if has_greenhouse_signal:
        for match in CAREERS_JOB_PATH_PATTERN.finditer(html):
            ids.add(match.group(1))

    return ids


def _merge_jobs(
    list_jobs: list[dict[str, Any]],
    extra_jobs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for job in list_jobs:
        job_id = job.get("id")
        if job_id is not None:
            merged[str(job_id)] = job
    for job in extra_jobs:
        job_id = job.get("id")
        if job_id is None:
            continue
        key = str(job_id)
        if key not in merged:
            merged[key] = job
    return list(merged.values())


def _is_valid_detail_job(job: dict[str, Any]) -> bool:
    return bool(job.get("id") and job.get("title") and job.get("content"))


def _job_passes_domain_check(
    job: dict[str, Any],
    careers_urls: list[str],
) -> bool:
    absolute_url = job.get("absolute_url")
    if not absolute_url or not careers_urls:
        return True
    job_domain = _root_domain(str(absolute_url))
    allowed = {_root_domain(url) for url in careers_urls}
    # Also allow greenhouse.io domains — API may return boards.greenhouse.io URLs
    allowed.add("greenhouse.io")
    return job_domain in allowed


class GreenhouseConnector(BaseConnector):
    base_url = "https://boards-api.greenhouse.io/v1/boards"
    detail_concurrency = DETAIL_CONCURRENCY
    detail_delay = DETAIL_DELAY

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        list_jobs = await self._fetch_board_list(company)
        careers_urls = _careers_urls(company)
        if not careers_urls:
            return list_jobs

        known_ids = {str(job["id"]) for job in list_jobs if job.get("id") is not None}
        discovered = await self._discover_careers_job_ids(company, careers_urls)
        extra_ids = sorted(discovered - known_ids)
        if not extra_ids:
            return list_jobs

        extra_jobs = await self._fetch_job_details(company, extra_ids, careers_urls)
        return _merge_jobs(list_jobs, extra_jobs)

    async def _fetch_board_list(self, company: Company) -> list[dict[str, Any]]:
        token = _board_token(company)
        url = f"{self.base_url}/{token}/jobs"
        params = {"content": "true"}
        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                payload = response.json()
        except Exception as exc:  # noqa: BLE001
            raise ConnectorFetchError(
                f"Greenhouse fetch failed for {token}: {exc}"
            ) from exc

        if not isinstance(payload, dict) or not isinstance(payload.get("jobs"), list):
            raise ParseError(f"Malformed Greenhouse response for {token}")
        return payload["jobs"]

    async def _discover_careers_job_ids(
        self,
        company: Company,
        careers_urls: list[str],
    ) -> set[str]:
        discovered: set[str] = set()
        for page_url in careers_urls:
            try:
                html = await self._fetch_careers_html(page_url)
            except Exception as exc:  # noqa: BLE001
                if structlog:
                    logger.warning(
                        "greenhouse_careers_fetch_failed",
                        company=company.name,
                        url=page_url,
                        error=str(exc),
                    )
                else:
                    logger.warning(
                        "greenhouse_careers_fetch_failed company=%s url=%s error=%s",
                        company.name,
                        page_url,
                        exc,
                    )
                continue
            discovered.update(discover_job_ids_from_html(html, page_url))
        return discovered

    async def _fetch_careers_html(self, url: str) -> str:
        if AsyncSession is not None:
            async with AsyncSession(impersonate=BROWSER_IMPERSONATE, timeout=REQUEST_TIMEOUT) as session:
                response = await session.get(url)
                if response.status_code >= 400:
                    raise ConnectorFetchError(
                        f"Careers page fetch failed ({response.status_code}): {url}"
                    )
                text = response.text
                if isinstance(text, bytes):
                    return text.decode("utf-8", errors="replace")
                return str(text)

        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT, follow_redirects=True) as client:
            response = await client.get(
                url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; JobCrawler/1.0)"},
            )
            response.raise_for_status()
            return response.text

    async def _fetch_job_details(
        self,
        company: Company,
        job_ids: list[str],
        careers_urls: list[str],
    ) -> list[dict[str, Any]]:
        token = _board_token(company)
        validate_domain = _should_validate_domain(company)
        results: list[dict[str, Any]] = []
        semaphore = asyncio.Semaphore(self.detail_concurrency)

        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            for job_id in job_ids:
                job = await self._fetch_single_job_detail(client, token, job_id, semaphore)
                if job is None:
                    continue
                if not _is_valid_detail_job(job):
                    if structlog:
                        logger.warning(
                            "greenhouse_detail_incomplete",
                            company=company.name,
                            job_id=job_id,
                        )
                    else:
                        logger.warning(
                            "greenhouse_detail_incomplete company=%s job_id=%s",
                            company.name,
                            job_id,
                        )
                    continue
                if validate_domain and not _job_passes_domain_check(job, careers_urls):
                    if structlog:
                        logger.warning(
                            "greenhouse_detail_domain_mismatch",
                            company=company.name,
                            job_id=job_id,
                            absolute_url=job.get("absolute_url"),
                        )
                    else:
                        logger.warning(
                            "greenhouse_detail_domain_mismatch company=%s job_id=%s url=%s",
                            company.name,
                            job_id,
                            job.get("absolute_url"),
                        )
                    continue
                results.append(job)
                await asyncio.sleep(self.detail_delay)

        return results

    async def _fetch_single_job_detail(
        self,
        client: httpx.AsyncClient,
        token: str,
        job_id: str,
        semaphore: asyncio.Semaphore,
    ) -> dict[str, Any] | None:
        url = f"{self.base_url}/{token}/jobs/{job_id}"
        params = {"content": "true"}
        async with semaphore:
            try:
                response = await client.get(url, params=params)
                if response.status_code == 404:
                    return None
                response.raise_for_status()
                payload = response.json()
            except Exception as exc:  # noqa: BLE001
                if structlog:
                    logger.warning(
                        "greenhouse_detail_fetch_failed",
                        token=token,
                        job_id=job_id,
                        error=str(exc),
                    )
                else:
                    logger.warning(
                        "greenhouse_detail_fetch_failed token=%s job_id=%s error=%s",
                        token,
                        job_id,
                        exc,
                    )
                return None

        if not isinstance(payload, dict):
            return None
        return payload
