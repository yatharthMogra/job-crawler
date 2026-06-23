from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

try:
    import structlog
except ImportError:  # pragma: no cover
    structlog = None

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.base import BaseConnector
from app.ingestion.rate_limiter import get_eightfold_bucket, parse_retry_after
from app.models.company import Company

logger = structlog.get_logger(__name__) if structlog else logging.getLogger(__name__)

DEFAULT_PAGE_SIZE = 10
DETAIL_RETRY_ATTEMPTS = 5
DETAIL_RETRY_BASE_SECONDS = 2.0
REQUEST_TIMEOUT = 30.0


def _platform_config(company: Company) -> dict[str, Any]:
    config = company.platform_config
    return config if isinstance(config, dict) else {}


class EightfoldConnector(BaseConnector):
    detail_retry_attempts = DETAIL_RETRY_ATTEMPTS
    detail_retry_base_seconds = DETAIL_RETRY_BASE_SECONDS

    def _api_host(self, company: Company) -> str:
        config = _platform_config(company)
        api_host = config.get("api_host")
        if not api_host:
            raise ParseError(f"Eightfold api_host missing for {company.board_token}")
        return str(api_host).rstrip("/").removeprefix("https://").removeprefix("http://")

    def _domain(self, company: Company) -> str:
        config = _platform_config(company)
        domain = config.get("domain")
        if not domain:
            raise ParseError(f"Eightfold domain missing for {company.board_token}")
        return str(domain)

    def _locale(self, company: Company) -> str:
        config = _platform_config(company)
        return str(config.get("locale") or "en")

    def _page_size(self, company: Company) -> int:
        config = _platform_config(company)
        raw = config.get("page_size", DEFAULT_PAGE_SIZE)
        try:
            return max(1, int(raw))
        except (TypeError, ValueError):
            return DEFAULT_PAGE_SIZE

    def _list_url(self, company: Company) -> str:
        return f"https://{self._api_host(company)}/api/apply/v2/jobs"

    def _detail_url(self, company: Company, job_id: str | int) -> str:
        return f"https://{self._api_host(company)}/api/apply/v2/jobs/{job_id}"

    def _list_params(self, company: Company, start: int) -> dict[str, str | int]:
        return {
            "domain": self._domain(company),
            "hl": self._locale(company),
            "start": start,
        }

    def _detail_params(self, company: Company) -> dict[str, str]:
        return {
            "domain": self._domain(company),
            "hl": self._locale(company),
        }

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        summaries = await self._fetch_all_summaries(company)
        if not summaries:
            return []

        needs_detail = [
            summary
            for summary in summaries
            if not (summary.get("job_description") or "").strip()
        ]

        detail_by_id: dict[str, dict[str, Any]] = {}
        detail_failed_count = 0
        if needs_detail:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
                tasks = [
                    self._fetch_job_detail(client, company, summary)
                    for summary in needs_detail
                ]
                details = await asyncio.gather(*tasks)
            for summary, detail in zip(needs_detail, details):
                job_id = summary.get("id")
                if not job_id:
                    continue
                job_key = str(job_id)
                if detail is None:
                    detail_failed_count += 1
                    continue
                detail_by_id[job_key] = detail

        if detail_failed_count:
            self._log_partial_detail_failure(
                board_token=company.board_token,
                failed_count=detail_failed_count,
                total=len(needs_detail),
            )

        jobs: list[dict[str, Any]] = []
        for summary in summaries:
            job_id = summary.get("id")
            if not job_id:
                continue
            job_key = str(job_id)
            if (summary.get("job_description") or "").strip():
                merged = dict(summary)
            elif job_key in detail_by_id:
                merged = {**summary, **detail_by_id[job_key]}
            else:
                merged = dict(summary)
                merged["job_description"] = ""
            merged["id"] = job_key
            jobs.append(merged)
        return jobs

    async def _fetch_all_summaries(self, company: Company) -> list[dict[str, Any]]:
        identifier = company.board_token
        list_url = self._list_url(company)
        page_size = self._page_size(company)
        results: list[dict[str, Any]] = []
        start = 0

        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
                while True:
                    data = await self._get_json(
                        client,
                        company,
                        list_url,
                        params=self._list_params(company, start),
                        context=f"Eightfold list fetch for {identifier}",
                        fail_on_error=True,
                    )

                    positions = data.get("positions")
                    if positions is None:
                        raise ParseError(
                            f"Malformed Eightfold list response for {identifier}"
                        )
                    if not isinstance(positions, list):
                        raise ParseError(
                            f"Malformed Eightfold list response for {identifier}"
                        )

                    for item in positions:
                        if isinstance(item, dict):
                            results.append(item)

                    total_raw = data.get("count", len(results))
                    try:
                        total = int(total_raw)
                    except (TypeError, ValueError):
                        total = len(results)

                    start += page_size
                    if start >= total or not positions:
                        break
        except ParseError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise ConnectorFetchError(
                f"Eightfold fetch failed for {identifier}: {exc}"
            ) from exc

        return results

    async def _fetch_job_detail(
        self,
        client: httpx.AsyncClient,
        company: Company,
        summary: dict[str, Any],
    ) -> dict[str, Any] | None:
        job_id = summary.get("id")
        if not job_id:
            return None

        detail_url = self._detail_url(company, job_id)
        try:
            detail = await self._get_json(
                client,
                company,
                detail_url,
                params=self._detail_params(company),
                context=f"Eightfold detail fetch for {company.board_token}/{job_id}",
                fail_on_error=False,
            )
        except ParseError:
            self._log_detail_fetch_failed(company.board_token, str(job_id))
            return None

        if detail is None or not isinstance(detail, dict):
            return None
        return detail

    async def _get_json(
        self,
        client: httpx.AsyncClient,
        company: Company,
        url: str,
        *,
        params: dict[str, str | int],
        context: str,
        fail_on_error: bool,
    ) -> dict[str, Any] | None:
        bucket = get_eightfold_bucket(self._api_host(company))
        last_error: Exception | None = None
        headers = {"Accept": "application/json"}

        for attempt in range(self.detail_retry_attempts):
            try:
                await bucket.acquire()
                response = await client.get(url, params=params, headers=headers)
                if response.status_code == 404 and not fail_on_error:
                    if structlog:
                        logger.debug(
                            "eightfold_detail_not_found",
                            board_token=company.board_token,
                            url=url,
                        )
                    else:
                        logger.debug(
                            "eightfold_detail_not_found board_token=%s url=%s",
                            company.board_token,
                            url,
                        )
                    return None
                if response.status_code == 429:
                    retry_after = parse_retry_after(response.headers.get("Retry-After"))
                    if retry_after is not None:
                        await asyncio.sleep(retry_after)
                    else:
                        await asyncio.sleep(self.detail_retry_base_seconds * (2**attempt))
                    continue
                response.raise_for_status()
                body = response.json()
                if not isinstance(body, dict):
                    raise ParseError(f"Malformed Eightfold response for {context}")
                return body
            except ParseError:
                raise
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                if attempt + 1 >= self.detail_retry_attempts:
                    break
                await asyncio.sleep(self.detail_retry_base_seconds * (2**attempt))

        if fail_on_error:
            raise ConnectorFetchError(f"{context}: {last_error}") from last_error

        job_id = url.rsplit("/", 1)[-1]
        self._log_detail_fetch_failed(company.board_token, job_id)
        return None

    @staticmethod
    def _log_detail_fetch_failed(board_token: str, job_id: str) -> None:
        if structlog:
            logger.warning(
                "eightfold_detail_fetch_failed",
                board_token=board_token,
                job_id=job_id,
            )
        else:
            logger.warning(
                "eightfold_detail_fetch_failed board_token=%s job_id=%s",
                board_token,
                job_id,
            )

    @staticmethod
    def _log_partial_detail_failure(
        *,
        board_token: str,
        failed_count: int,
        total: int,
    ) -> None:
        if structlog:
            logger.warning(
                "eightfold_partial_detail_failure",
                board_token=board_token,
                failed_count=failed_count,
                total=total,
            )
        else:
            logger.warning(
                "eightfold_partial_detail_failure board_token=%s failed_count=%s total=%s",
                board_token,
                failed_count,
                total,
            )
