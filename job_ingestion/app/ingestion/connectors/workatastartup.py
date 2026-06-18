from __future__ import annotations

import asyncio
import html as html_lib
import json
import logging
import re
from typing import Any

from bs4 import BeautifulSoup
from curl_cffi.requests import AsyncSession

try:
    import structlog
except ImportError:  # pragma: no cover
    structlog = None

from app.config import Settings, get_settings
from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.base import BaseConnector
from app.models.company import Company

logger = structlog.get_logger(__name__) if structlog else logging.getLogger(__name__)

ACCOUNT_URL = "https://account.ycombinator.com/"
SIGN_IN_URL = "https://account.ycombinator.com/sign_in"
JOBS_PAGE_URL = "https://www.workatastartup.com/jobs"
COMPANY_PAGE_URL = "https://www.workatastartup.com/companies/{slug}"
BATCH_DELAY = 1.5
BROWSER_IMPERSONATE = "chrome120"
_INERTIA_PAGE_PATTERN = re.compile(r'data-page="([^"]+)"')


class WorkAtAStartupConnector(BaseConnector):
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        email = self._settings.yc_crawler_email
        password = self._settings.yc_crawler_password
        if not email or not password:
            raise ConnectorFetchError(
                "Work at a Startup credentials missing (YC_CRAWLER_EMAIL / YC_CRAWLER_PASSWORD)"
            )

        roles = self._settings.yc_waas_roles_list or ["eng", "ds"]
        extra_slugs = self._extra_company_slugs(company)
        jobs_by_id: dict[str, dict[str, Any]] = {}

        async with AsyncSession(impersonate=BROWSER_IMPERSONATE, timeout=30.0) as client:
            await self._login(client, email=email, password=password)

            listing_slugs: set[str] = set()
            for role in roles:
                listings = await self._fetch_role_listings(client, role)
                for listing in listings:
                    slug = listing.get("companySlug")
                    if slug:
                        listing_slugs.add(str(slug))
                for listing in listings:
                    platform_job = self._listing_to_platform_job(listing)
                    if platform_job is None:
                        continue
                    detail = await self._fetch_job_detail(client, int(listing["id"]))
                    if detail:
                        platform_job = self._merge_job_detail(platform_job, detail)
                    jobs_by_id[platform_job["id"]] = platform_job
                await asyncio.sleep(BATCH_DELAY)

            company_slugs = listing_slugs | extra_slugs
            for slug in sorted(company_slugs):
                for raw_job, raw_company in await self._fetch_company_jobs(client, slug):
                    if not self._company_job_matches_roles(raw_job, roles, force=slug in extra_slugs):
                        continue
                    platform_job = self._company_job_to_platform_job(raw_job, raw_company)
                    jobs_by_id[platform_job["id"]] = platform_job
                await asyncio.sleep(BATCH_DELAY)

        return list(jobs_by_id.values())

    @staticmethod
    def _extra_company_slugs(company: Company) -> set[str]:
        config = company.platform_config if isinstance(company.platform_config, dict) else {}
        slugs = config.get("company_slugs") or config.get("extra_company_slugs") or []
        if isinstance(slugs, str):
            return {slug.strip() for slug in slugs.split(",") if slug.strip()}
        if isinstance(slugs, list):
            return {str(slug).strip() for slug in slugs if slug}
        return set()

    async def _login(self, client: AsyncSession, *, email: str, password: str) -> None:
        try:
            resp = await client.get(
                f"{ACCOUNT_URL}?continue=https%3A%2F%2Fwww.workatastartup.com%2F"
            )
        except Exception as exc:  # noqa: BLE001
            raise ConnectorFetchError(f"YC account page fetch failed: {exc}") from exc

        soup = BeautifulSoup(resp.text, "html.parser")
        csrf_meta = soup.find("meta", {"name": "csrf-token"})
        if not csrf_meta or not csrf_meta.get("content"):
            raise ParseError("CSRF token not found on YC account page")

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRF-Token": csrf_meta["content"],
            "X-Requested-With": "XMLHttpRequest",
        }
        body = {
            "ycid": email,
            "password": password,
            "continue": "https://www.workatastartup.com/",
        }
        try:
            sign_in = await client.post(SIGN_IN_URL, headers=headers, json=body)
        except Exception as exc:  # noqa: BLE001
            raise ConnectorFetchError(f"YC sign_in request failed: {exc}") from exc

        if sign_in.status_code != 200:
            raise ConnectorFetchError(f"YC sign_in failed: status={sign_in.status_code}")

        payload = sign_in.json()
        redirect_to = payload.get("redirectTo")
        if not redirect_to:
            raise ConnectorFetchError("YC sign_in succeeded but no redirectTo was returned")

        await client.get(str(redirect_to))

    async def _fetch_role_listings(self, client: AsyncSession, role: str) -> list[dict[str, Any]]:
        url = f"{JOBS_PAGE_URL}?role={role}&jobType=fulltime"
        try:
            resp = await client.get(url)
            resp.raise_for_status()
        except Exception as exc:  # noqa: BLE001
            raise ConnectorFetchError(f"Work at a Startup jobs page fetch failed: {exc}") from exc

        page = self._parse_inertia_page(resp.text)
        jobs = page.get("props", {}).get("jobs", [])
        if not isinstance(jobs, list):
            raise ParseError(f"Malformed Work at a Startup jobs page for role={role}")
        return [job for job in jobs if isinstance(job, dict)]

    async def _fetch_company_jobs(
        self,
        client: AsyncSession,
        slug: str,
    ) -> list[tuple[dict[str, Any], dict[str, Any]]]:
        url = COMPANY_PAGE_URL.format(slug=slug)
        try:
            resp = await client.get(url)
            if resp.status_code == 404:
                return []
            resp.raise_for_status()
        except Exception as exc:  # noqa: BLE001
            if structlog:
                logger.warning("waas_company_fetch_failed", slug=slug, error=str(exc))
            else:
                logger.warning("waas_company_fetch_failed slug=%s error=%s", slug, exc)
            return []

        page = self._parse_inertia_page(resp.text)
        raw_company = page.get("props", {}).get("rawCompany")
        if not isinstance(raw_company, dict):
            return []

        jobs = raw_company.get("jobs")
        if not isinstance(jobs, list):
            return []

        return [(job, raw_company) for job in jobs if isinstance(job, dict)]

    async def _fetch_job_detail(self, client: AsyncSession, job_id: int) -> dict[str, Any] | None:
        url = f"https://www.workatastartup.com/jobs/{job_id}"
        try:
            resp = await client.get(url)
            resp.raise_for_status()
        except Exception as exc:  # noqa: BLE001
            if structlog:
                logger.warning("waas_job_detail_fetch_failed", job_id=job_id, error=str(exc))
            else:
                logger.warning("waas_job_detail_fetch_failed job_id=%s error=%s", job_id, exc)
            return None

        page = self._parse_inertia_page(resp.text)
        job = page.get("props", {}).get("job")
        return job if isinstance(job, dict) else None

    @staticmethod
    def _parse_inertia_page(text: str) -> dict[str, Any]:
        match = _INERTIA_PAGE_PATTERN.search(text)
        if not match:
            raise ParseError("Inertia page payload not found")
        return json.loads(html_lib.unescape(match.group(1)))

    @staticmethod
    def _company_job_matches_roles(
        job: dict[str, Any],
        roles: list[str],
        *,
        force: bool,
    ) -> bool:
        if force:
            return str(job.get("job_type") or "fulltime").lower() in {"fulltime", "full-time"}
        if str(job.get("job_type") or "fulltime").lower() not in {"fulltime", "full-time"}:
            return False
        if "eng" in roles and job.get("eng_type"):
            return True
        if "ds" in roles and job.get("science_type"):
            return True
        return False

    @staticmethod
    def _listing_to_platform_job(listing: dict[str, Any]) -> dict[str, Any] | None:
        job_id = listing.get("id")
        if job_id is None:
            return None
        external_id = f"yc_{job_id}"
        apply_url = listing.get("applyUrl") or f"https://www.workatastartup.com/jobs/{job_id}"
        location = listing.get("location")
        remote = isinstance(location, str) and "remote" in location.lower()
        return {
            "id": external_id,
            "title": listing.get("title") or "",
            "description": "",
            "location": location,
            "remote": remote,
            "visa_sponsorship": None,
            "created_at": None,
            "apply_url": apply_url,
            "job_type": listing.get("jobType") or "fulltime",
            "company": {
                "name": listing.get("companyName"),
                "slug": listing.get("companySlug"),
                "batch": listing.get("companyBatch"),
                "team_size": None,
                "one_liner": listing.get("companyOneLiner"),
            },
        }

    @staticmethod
    def _merge_job_detail(platform_job: dict[str, Any], detail: dict[str, Any]) -> dict[str, Any]:
        merged = dict(platform_job)
        if detail.get("descriptionHtml"):
            merged["description"] = detail["descriptionHtml"]
        if detail.get("location"):
            merged["location"] = detail["location"]
        if detail.get("sponsorsVisa") is not None:
            merged["visa_sponsorship"] = bool(detail["sponsorsVisa"])
        if detail.get("jobType"):
            merged["job_type"] = detail["jobType"]
        if detail.get("location") and "remote" in str(detail["location"]).lower():
            merged["remote"] = True
        return merged

    @classmethod
    def _company_job_to_platform_job(
        cls,
        job: dict[str, Any],
        company: dict[str, Any],
    ) -> dict[str, Any]:
        job_id = job["id"]
        location = job.get("pretty_location_or_remote") or job.get("location")
        remote_flag = str(job.get("remote") or "").lower() == "yes"
        if location and "remote" in str(location).lower():
            remote_flag = True
        visa = job.get("visa")
        visa_sponsorship = None
        if visa == "yes":
            visa_sponsorship = True
        elif visa == "no":
            visa_sponsorship = False

        return {
            "id": f"yc_{job_id}",
            "title": job.get("title") or "",
            "description": job.get("description") or "",
            "location": location,
            "remote": remote_flag,
            "visa_sponsorship": visa_sponsorship,
            "created_at": job.get("updated_at") or job.get("created_at"),
            "apply_url": f"https://www.workatastartup.com/jobs/{job_id}",
            "job_type": job.get("job_type") or "fulltime",
            "company": {
                "name": company.get("name"),
                "slug": company.get("slug"),
                "batch": company.get("batch"),
                "team_size": company.get("team_size"),
                "one_liner": company.get("one_liner"),
            },
        }
