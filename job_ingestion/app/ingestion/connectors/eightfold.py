from __future__ import annotations

import asyncio
import logging
from typing import Any
from urllib.parse import urlencode

import httpx

try:
    import structlog
except ImportError:  # pragma: no cover
    structlog = None

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.base import BaseConnector
from app.models.company import Company

logger = structlog.get_logger(__name__) if structlog else logging.getLogger(__name__)

DETAIL_CONCURRENCY = 5
DETAIL_DELAY = 0.3
REQUEST_TIMEOUT = 30.0
PAGE_SIZE = 50
USER_AGENT = "Mozilla/5.0 (compatible; CareerMatchBot/1.0)"


class EightfoldConnector(BaseConnector):
    detail_concurrency = DETAIL_CONCURRENCY
    detail_delay = DETAIL_DELAY

    def _platform_config(self, company: Company) -> dict[str, Any]:
        config = company.platform_config
        return config if isinstance(config, dict) else {}

    def _api_host(self, company: Company) -> str:
        config = self._platform_config(company)
        api_host = config.get("api_host")
        if not api_host:
            raise ParseError(f"Eightfold api_host missing for {company.name}")
        return str(api_host).rstrip("/")

    def _domain(self, company: Company) -> str:
        config = self._platform_config(company)
        domain = config.get("domain")
        if not domain:
            raise ParseError(f"Eightfold domain missing for {company.name}")
        return str(domain)

    def _extra_params(self, company: Company) -> dict[str, str]:
        config = self._platform_config(company)
        extra = config.get("extra_params")
        if not isinstance(extra, dict):
            return {}
        return {str(key): str(value) for key, value in extra.items()}

    def _public_job_url(self, company: Company, job_id: str) -> str:
        api_host = self._api_host(company)
        domain = self._domain(company)
        extra = self._extra_params(company)
        query = urlencode({"domain": domain, **extra})
        return f"https://{api_host}/careers/job/{job_id}?{query}"

    def _list_params(self, company: Company, *, start: int) -> dict[str, str]:
        params = {
            "domain": self._domain(company),
            "hl": "en",
            "start": str(start),
            "num": str(PAGE_SIZE),
        }
        params.update(self._extra_params(company))
        return params

    def _detail_params(self, company: Company) -> dict[str, str]:
        params = {"domain": self._domain(company), "hl": "en"}
        params.update(self._extra_params(company))
        return params

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        api_host = self._api_host(company)
        headers = {"User-Agent": USER_AGENT}

        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT, headers=headers) as client:
                summaries = await self._fetch_all_summaries(client, api_host, company)
                if not summaries:
                    return []

                semaphore = asyncio.Semaphore(self.detail_concurrency)
                tasks = [
                    self._fetch_job_detail(client, api_host, company, summary, semaphore)
                    for summary in summaries
                ]
                details = await asyncio.gather(*tasks)
        except ParseError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise ConnectorFetchError(
                f"Eightfold fetch failed for {company.board_token}: {exc}"
            ) from exc

        jobs: list[dict[str, Any]] = []
        for summary, detail in zip(summaries, details):
            if detail is None:
                continue
            job_id = summary.get("id")
            if not job_id:
                continue
            merged = {**summary, **detail}
            merged["id"] = str(job_id)
            merged["externalLink"] = self._public_job_url(company, str(job_id))
            jobs.append(merged)
        return jobs

    async def _fetch_all_summaries(
        self,
        client: httpx.AsyncClient,
        api_host: str,
        company: Company,
    ) -> list[dict[str, Any]]:
        start = 0
        total_count: int | None = None
        summaries: list[dict[str, Any]] = []

        while True:
            response = await client.get(
                f"https://{api_host}/api/apply/v2/jobs",
                params=self._list_params(company, start=start),
            )
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict):
                raise ParseError(f"Malformed Eightfold list response for {company.board_token}")

            if total_count is None:
                raw_total = data.get("count")
                try:
                    total_count = int(raw_total) if raw_total is not None else None
                except (TypeError, ValueError):
                    total_count = None

            positions = data.get("positions")
            if not isinstance(positions, list) or not positions:
                break

            for position in positions:
                if isinstance(position, dict) and position.get("id") is not None:
                    summaries.append(position)

            start += len(positions)
            if total_count is not None and start >= total_count:
                break
            if len(positions) < PAGE_SIZE:
                break

            await asyncio.sleep(0.2)

        return summaries

    async def _fetch_job_detail(
        self,
        client: httpx.AsyncClient,
        api_host: str,
        company: Company,
        summary: dict[str, Any],
        semaphore: asyncio.Semaphore,
    ) -> dict[str, Any] | None:
        job_id = summary.get("id")
        if not job_id:
            return None

        async with semaphore:
            try:
                response = await client.get(
                    f"https://{api_host}/api/apply/v2/jobs/{job_id}",
                    params=self._detail_params(company),
                )
                if response.status_code == 404:
                    return None
                response.raise_for_status()
                data = response.json()
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 404:
                    return None
                raise ConnectorFetchError(
                    f"Eightfold detail failed for {company.board_token}/{job_id}: {exc}"
                ) from exc
            except Exception as exc:  # noqa: BLE001
                raise ConnectorFetchError(
                    f"Eightfold detail failed for {company.board_token}/{job_id}: {exc}"
                ) from exc
            finally:
                await asyncio.sleep(self.detail_delay)

        if not isinstance(data, dict):
            raise ParseError(
                f"Malformed Eightfold detail response for {company.board_token}/{job_id}"
            )

        position = data.get("position")
        if isinstance(position, dict):
            return position
        return data
