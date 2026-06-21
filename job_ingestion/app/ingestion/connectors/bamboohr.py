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
from app.models.company import Company

logger = structlog.get_logger(__name__) if structlog else logging.getLogger(__name__)

DETAIL_CONCURRENCY = 5
DETAIL_DELAY = 0.3
REQUEST_TIMEOUT = 30.0


def format_bamboohr_location(job: dict[str, Any]) -> str | None:
    ats = job.get("atsLocation")
    if isinstance(ats, dict):
        parts = [ats.get("city"), ats.get("state"), ats.get("country")]
        formatted = ", ".join(str(part) for part in parts if part)
        if formatted:
            return formatted

    location = job.get("location")
    if isinstance(location, dict):
        parts = [location.get("city"), location.get("state")]
        formatted = ", ".join(str(part) for part in parts if part)
        if formatted:
            return formatted

    return None


class BambooHRConnector(BaseConnector):
    detail_concurrency = DETAIL_CONCURRENCY
    detail_delay = DETAIL_DELAY

    def _platform_config(self, company: Company) -> dict[str, Any]:
        config = company.platform_config
        return config if isinstance(config, dict) else {}

    def _base_url(self, company: Company) -> str:
        config = self._platform_config(company)
        if config.get("base_url"):
            return str(config["base_url"]).rstrip("/")
        return f"https://{company.board_token}.bamboohr.com"

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        base_url = self._base_url(company)
        summaries = await self._fetch_summaries(base_url, company.board_token)
        if not summaries:
            return []

        semaphore = asyncio.Semaphore(self.detail_concurrency)
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            tasks = [
                self._fetch_job_detail(client, base_url, company.board_token, summary, semaphore)
                for summary in summaries
            ]
            details = await asyncio.gather(*tasks)

        jobs: list[dict[str, Any]] = []
        for summary, detail in zip(summaries, details):
            if detail is None:
                continue
            job_id = summary.get("id")
            if not job_id:
                continue
            merged = {**summary, **detail}
            merged["id"] = str(job_id)
            merged["externalLink"] = f"{base_url}/careers/{job_id}"
            jobs.append(merged)
        return jobs

    async def _fetch_summaries(self, base_url: str, board_token: str) -> list[dict[str, Any]]:
        list_url = f"{base_url}/careers/list"
        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
                response = await client.get(list_url)
                response.raise_for_status()
                data = response.json()
        except ParseError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise ConnectorFetchError(
                f"BambooHR list fetch failed for {board_token}: {exc}"
            ) from exc

        if not isinstance(data, dict):
            raise ParseError(f"Malformed BambooHR list response for {board_token}")

        result = data.get("result")
        if result is None:
            raise ParseError(f"Malformed BambooHR list response for {board_token}")
        if not isinstance(result, list):
            raise ParseError(f"Malformed BambooHR list response for {board_token}")

        return [item for item in result if isinstance(item, dict)]

    async def _fetch_job_detail(
        self,
        client: httpx.AsyncClient,
        base_url: str,
        board_token: str,
        summary: dict[str, Any],
        semaphore: asyncio.Semaphore,
    ) -> dict[str, Any] | None:
        job_id = summary.get("id")
        if not job_id:
            return None

        detail_url = f"{base_url}/careers/{job_id}/detail"
        async with semaphore:
            try:
                response = await client.get(detail_url)
                if response.status_code == 404:
                    if structlog:
                        logger.debug(
                            "bamboohr_detail_not_found",
                            board_token=board_token,
                            job_id=job_id,
                        )
                    else:
                        logger.debug(
                            "bamboohr_detail_not_found board_token=%s job_id=%s",
                            board_token,
                            job_id,
                        )
                    return None
                response.raise_for_status()
                data = response.json()
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 404:
                    return None
                raise ConnectorFetchError(
                    f"BambooHR detail failed for {board_token}/{job_id}: {exc}"
                ) from exc
            except Exception as exc:  # noqa: BLE001
                raise ConnectorFetchError(
                    f"BambooHR detail failed for {board_token}/{job_id}: {exc}"
                ) from exc
            finally:
                await asyncio.sleep(self.detail_delay)

        if not isinstance(data, dict):
            raise ParseError(
                f"Malformed BambooHR detail response for {board_token}/{job_id}"
            )

        result = data.get("result")
        if not isinstance(result, dict):
            raise ParseError(
                f"Malformed BambooHR detail response for {board_token}/{job_id}"
            )

        job_opening = result.get("jobOpening")
        if not isinstance(job_opening, dict):
            raise ParseError(
                f"Malformed BambooHR detail response for {board_token}/{job_id}"
            )

        return job_opening
