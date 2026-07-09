from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

import httpx
import pytest

from app.ingestion.connectors.apple_careers import AppleCareersConnector
from app.models.company import Company


def _apple_company() -> Company:
    return Company(
        id=__import__("uuid").uuid4(),
        name="Apple",
        platform="apple_careers",
        board_token="apple",
        platform_config={
            "locale": "en-us",
            "location": "united-states-USA",
            "teams": ["apps-and-frameworks-SFTWR-AF"],
        },
        is_active=True,
    )


@pytest.mark.asyncio
async def test_fetch_jobs_tolerates_partial_detail_failures(monkeypatch) -> None:
    connector = AppleCareersConnector()
    company = _apple_company()
    summaries = [
        {"id": "200000001-0001", "title": "One", "externalLink": "https://jobs.apple.com/en-us/details/200000001-0001/one"},
        {"id": "200000002-0002", "title": "Two", "externalLink": "https://jobs.apple.com/en-us/details/200000002-0002/two"},
    ]

    monkeypatch.setattr(connector, "_fetch_all_summaries", AsyncMock(return_value=summaries))

    async def _detail(_client, summary, _sem):  # noqa: ANN001
        if summary["id"] == "200000001-0001":
            raise httpx.ReadTimeout("timed out")
        return {"raw_html": "<p>ok</p>"}

    monkeypatch.setattr(connector, "_fetch_job_detail", _detail)

    jobs = await connector.fetch_jobs(company)

    assert len(jobs) == 1
    assert jobs[0]["id"] == "200000002-0002"
    assert jobs[0]["raw_html"] == "<p>ok</p>"
