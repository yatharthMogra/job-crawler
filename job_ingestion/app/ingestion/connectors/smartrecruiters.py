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

LIST_URL = "https://api.smartrecruiters.com/v1/companies/{identifier}/postings"
DETAIL_URL = "https://api.smartrecruiters.com/v1/companies/{identifier}/postings/{posting_id}"

PAGE_SIZE = 100
DETAIL_CONCURRENCY = 5
DETAIL_DELAY = 0.3


class SmartRecruitersConnector(BaseConnector):
    page_size = PAGE_SIZE
    detail_concurrency = DETAIL_CONCURRENCY
    detail_delay = DETAIL_DELAY

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        summaries = await self._fetch_all_summaries(company)
        if not summaries:
            return []

        semaphore = asyncio.Semaphore(self.detail_concurrency)
        async with httpx.AsyncClient(timeout=30.0) as client:
            tasks = [
                self._fetch_posting_detail(client, company.board_token, summary, semaphore)
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
            merged["externalLink"] = (
                f"https://jobs.smartrecruiters.com/{company.board_token}/{job_id}"
            )
            jobs.append(merged)
        return jobs

    async def _fetch_all_summaries(self, company: Company) -> list[dict[str, Any]]:
        identifier = company.board_token
        list_url = LIST_URL.format(identifier=identifier)
        results: list[dict[str, Any]] = []
        offset = 0

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                while True:
                    response = await client.get(
                        list_url,
                        params={"limit": self.page_size, "offset": offset},
                    )
                    response.raise_for_status()
                    data = response.json()

                    if not isinstance(data, dict):
                        raise ParseError(
                            f"Malformed SmartRecruiters list response for {identifier}"
                        )

                    content = data.get("content")
                    if content is None:
                        raise ParseError(
                            f"Malformed SmartRecruiters list response for {identifier}"
                        )
                    if not isinstance(content, list):
                        raise ParseError(
                            f"Malformed SmartRecruiters list response for {identifier}"
                        )

                    for item in content:
                        if isinstance(item, dict):
                            results.append(item)

                    total_found = data.get("totalFound", 0)
                    try:
                        total = int(total_found)
                    except (TypeError, ValueError):
                        total = len(results)

                    offset += self.page_size
                    if offset >= total:
                        break
        except ParseError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise ConnectorFetchError(
                f"SmartRecruiters fetch failed for {identifier}: {exc}"
            ) from exc

        return results

    async def _fetch_posting_detail(
        self,
        client: httpx.AsyncClient,
        board_token: str,
        summary: dict[str, Any],
        semaphore: asyncio.Semaphore,
    ) -> dict[str, Any] | None:
        job_id = summary.get("id")
        if not job_id:
            return None

        detail_url = DETAIL_URL.format(identifier=board_token, posting_id=job_id)
        async with semaphore:
            try:
                response = await client.get(detail_url)
                if response.status_code == 404:
                    if structlog:
                        logger.debug(
                            "smartrecruiters_detail_not_found",
                            board_token=board_token,
                            job_id=job_id,
                        )
                    else:
                        logger.debug(
                            "smartrecruiters_detail_not_found board_token=%s job_id=%s",
                            board_token,
                            job_id,
                        )
                    return None
                response.raise_for_status()
                detail = response.json()
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 404:
                    return None
                raise ConnectorFetchError(
                    f"SmartRecruiters detail failed for {board_token}/{job_id}: {exc}"
                ) from exc
            except Exception as exc:  # noqa: BLE001
                raise ConnectorFetchError(
                    f"SmartRecruiters detail failed for {board_token}/{job_id}: {exc}"
                ) from exc
            finally:
                await asyncio.sleep(self.detail_delay)

        if not isinstance(detail, dict):
            raise ParseError(
                f"Malformed SmartRecruiters detail response for {board_token}/{job_id}"
            )
        return detail
