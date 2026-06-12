from __future__ import annotations

import asyncio
import logging
import re
from datetime import date, datetime, timedelta, timezone
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

MAX_PAGE_SIZE = 20
DEFAULT_MAX_POSTED_AGE_DAYS = 30
_JOB_REQ_ID_SUFFIX = re.compile(r"_([^/_]+)$")
_RELATIVE_POSTED_DAYS = re.compile(r"posted\s+(\d+)\s+days?\s+ago", re.IGNORECASE)


class WorkdayConnector(BaseConnector):
    detail_concurrency = 1
    detail_retry_attempts = 5
    detail_retry_base_seconds = 2.0
    detail_delay = 0.35

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        base_url = self._base_url(company)
        public_base_url = self._public_base_url(company)
        max_posted_age_days = self._max_posted_age_days(company)
        reference_date = datetime.now(timezone.utc).date()
        listings = await self._fetch_all_pages(base_url)
        if not listings:
            return []

        jobs_with_detail: list[dict[str, Any]] = []
        semaphore = asyncio.Semaphore(self.detail_concurrency)
        async with httpx.AsyncClient(timeout=30.0) as client:
            for listing in listings:
                external_path = listing.get("externalPath")
                job_req_id = self._resolve_job_req_id(listing)
                if not external_path or not job_req_id:
                    continue

                list_recency = self._listing_recency_hint(
                    listing.get("postedOn"), reference_date, max_posted_age_days
                )
                if list_recency is False:
                    continue

                detail_payload: dict[str, Any] | None = None
                try:
                    detail_payload = await self._fetch_detail(
                        client, base_url, str(external_path), semaphore
                    )
                except Exception as exc:  # noqa: BLE001
                    if structlog:
                        logger.warning(
                            "workday_detail_fetch_failed",
                            company=company.name,
                            external_path=external_path,
                            error=str(exc),
                        )
                    else:
                        logger.warning(
                            "workday_detail_fetch_failed company=%s external_path=%s error=%s",
                            company.name,
                            external_path,
                            exc,
                        )

                if detail_payload is not None:
                    job_posting_info = detail_payload.get("jobPostingInfo", {})
                    if not isinstance(job_posting_info, dict):
                        job_posting_info = {}
                    merged = {**listing, **detail_payload, "jobPostingInfo": job_posting_info}
                else:
                    merged = {**listing, "jobPostingInfo": {}}

                if not self._job_within_posted_window(
                    merged, reference_date, max_posted_age_days
                ):
                    continue

                merged["id"] = str(job_req_id)
                merged["externalLink"] = self._public_posting_url(
                    company, public_base_url, str(external_path)
                )
                jobs_with_detail.append(merged)
                await asyncio.sleep(self.detail_delay)

        return jobs_with_detail

    def _max_posted_age_days(self, company: Company) -> int:
        config = self._platform_config(company)
        value = config.get("max_posted_age_days", DEFAULT_MAX_POSTED_AGE_DAYS)
        try:
            return max(1, int(value))
        except (TypeError, ValueError):
            return DEFAULT_MAX_POSTED_AGE_DAYS

    def _tenant(self, company: Company) -> str:
        config = self._platform_config(company)
        tenant = config.get("tenant")
        if tenant:
            return str(tenant)
        return company.board_token

    @staticmethod
    def _listing_recency_hint(
        posted_on: object,
        reference_date: date,
        max_age_days: int,
    ) -> Optional[bool]:
        if not posted_on or not isinstance(posted_on, str):
            return None
        lowered = posted_on.strip().lower()
        if "30+" in lowered or "more than 30" in lowered:
            return False
        if "today" in lowered or "yesterday" in lowered:
            return True
        match = _RELATIVE_POSTED_DAYS.search(posted_on)
        if match:
            return int(match.group(1)) <= max_age_days
        parsed = WorkdayConnector._parse_posted_date(posted_on)
        if parsed is not None:
            return (reference_date - parsed) <= timedelta(days=max_age_days)
        return None

    @staticmethod
    def _parse_posted_date(value: str) -> Optional[date]:
        for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        return None

    @classmethod
    def _job_within_posted_window(
        cls,
        job: dict[str, Any],
        reference_date: date,
        max_age_days: int,
    ) -> bool:
        info = job.get("jobPostingInfo") or {}
        for candidate in (info.get("startDate"), info.get("postedOn"), job.get("postedOn")):
            if not candidate or not isinstance(candidate, str):
                continue
            parsed = cls._parse_posted_date(candidate)
            if parsed is not None:
                return (reference_date - parsed) <= timedelta(days=max_age_days)
            hint = cls._listing_recency_hint(candidate, reference_date, max_age_days)
            if hint is not None:
                return hint
        return False

    @staticmethod
    def _resolve_job_req_id(listing: dict[str, Any]) -> str | None:
        job_req_id = listing.get("jobReqId")
        if job_req_id:
            return str(job_req_id)

        bullet_fields = listing.get("bulletFields")
        if isinstance(bullet_fields, list):
            for bullet in bullet_fields:
                if bullet:
                    return str(bullet)

        external_path = listing.get("externalPath")
        if isinstance(external_path, str):
            match = _JOB_REQ_ID_SUFFIX.search(external_path)
            if match:
                return match.group(1)
        return None

    def _platform_config(self, company: Company) -> dict[str, Any]:
        config = company.platform_config
        return config if isinstance(config, dict) else {}

    def _base_url(self, company: Company) -> str:
        config = self._platform_config(company)
        instance = config.get("instance", "wd1")
        career_site = config.get("career_site", "External")
        tenant = self._tenant(company)
        return (
            f"https://{tenant}.{instance}.myworkdayjobs.com"
            f"/wday/cxs/{tenant}/{career_site}"
        )

    def _public_base_url(self, company: Company) -> str:
        config = self._platform_config(company)
        instance = config.get("instance", "wd1")
        tenant = self._tenant(company)
        return f"https://{tenant}.{instance}.myworkdayjobs.com"

    def _public_posting_url(
        self,
        company: Company,
        public_base_url: str,
        external_path: str,
    ) -> str:
        config = self._platform_config(company)
        prefix = str(config.get("public_path_prefix") or config.get("career_site") or "").strip("/")
        if prefix:
            if external_path.startswith("/job/"):
                return f"{public_base_url}/{prefix}{external_path}"
            return f"{public_base_url}/{prefix}/job{external_path}"
        if external_path.startswith("/job/"):
            return f"{public_base_url}{external_path}"
        return f"{public_base_url}/job{external_path}"

    @staticmethod
    def _detail_url(base_url: str, external_path: str) -> str:
        if external_path.startswith("/job/"):
            return f"{base_url}{external_path}"
        return f"{base_url}/job{external_path}"

    async def _fetch_all_pages(self, base_url: str) -> list[dict[str, Any]]:
        all_jobs: list[dict[str, Any]] = []
        offset = 0

        async with httpx.AsyncClient(timeout=30.0) as client:
            while True:
                response: httpx.Response | None = None
                last_error: Exception | None = None
                for attempt in range(self.detail_retry_attempts):
                    try:
                        response = await client.post(
                            f"{base_url}/jobs",
                            json={
                                "appliedFacets": {},
                                "limit": MAX_PAGE_SIZE,
                                "offset": offset,
                                "searchText": "",
                            },
                        )
                        if response.status_code in (429, 503):
                            await asyncio.sleep(self.detail_retry_base_seconds * (2**attempt))
                            continue
                        if response.status_code != 200:
                            raise ConnectorFetchError(
                                f"Workday list failed for {base_url}: HTTP {response.status_code}"
                            )
                        break
                    except ConnectorFetchError:
                        raise
                    except Exception as exc:  # noqa: BLE001
                        last_error = exc
                        if attempt + 1 >= self.detail_retry_attempts:
                            break
                        await asyncio.sleep(self.detail_retry_base_seconds * (2**attempt))

                if response is None or response.status_code != 200:
                    raise ConnectorFetchError(
                        f"Workday list fetch failed for {base_url}: {last_error}"
                    ) from last_error

                try:
                    data = response.json()
                except Exception as exc:  # noqa: BLE001
                    raise ParseError(
                        f"Workday list response is not valid JSON for {base_url}"
                    ) from exc

                postings = data.get("jobPostings")
                if not isinstance(postings, list):
                    raise ParseError(
                        f"Workday list response missing jobPostings array for {base_url}"
                    )

                all_jobs.extend(posting for posting in postings if isinstance(posting, dict))
                if not postings:
                    break

                offset += MAX_PAGE_SIZE
                total = data.get("total")
                if isinstance(total, int) and offset >= total:
                    break

        return all_jobs

    async def _fetch_detail(
        self,
        client: httpx.AsyncClient,
        base_url: str,
        external_path: str,
        semaphore: asyncio.Semaphore,
    ) -> dict[str, Any]:
        url = self._detail_url(base_url, external_path)
        payload: dict[str, Any] | None = None
        last_error: Exception | None = None

        async with semaphore:
            for attempt in range(self.detail_retry_attempts):
                try:
                    response = await client.get(url)
                    if response.status_code in (429, 503):
                        await asyncio.sleep(self.detail_retry_base_seconds * (2**attempt))
                        continue
                    if response.status_code != 200:
                        raise ConnectorFetchError(
                            f"Workday detail failed for {external_path}: HTTP {response.status_code}"
                        )
                    try:
                        payload = response.json()
                    except Exception as exc:  # noqa: BLE001
                        raise ParseError(
                            f"Workday detail response is not valid JSON: {external_path}"
                        ) from exc
                    break
                except (ConnectorFetchError, ParseError):
                    raise
                except Exception as exc:  # noqa: BLE001
                    last_error = exc
                    if attempt + 1 >= self.detail_retry_attempts:
                        break
                    await asyncio.sleep(self.detail_retry_base_seconds * (2**attempt))

        if payload is None:
            raise ConnectorFetchError(
                f"Workday detail fetch failed for {external_path}: {last_error}"
            ) from last_error

        if not isinstance(payload, dict):
            raise ParseError(f"Malformed Workday detail response for {external_path}")
        return payload
