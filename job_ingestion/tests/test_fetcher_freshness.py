from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

import pytest

from app.ingestion.fetcher import fetch_company_jobs
from app.models.company import Company


@pytest.mark.asyncio
async def test_fetch_company_jobs_filters_stale_lever_jobs() -> None:
    reference = datetime(2026, 6, 19, tzinfo=timezone.utc)
    fresh_ms = int((reference - timedelta(days=1)).timestamp() * 1000)
    stale_ms = int((reference - timedelta(days=30)).timestamp() * 1000)
    company = Company(
        name="Example",
        board_token="example",
        platform="lever",
        is_active=True,
    )
    payload = [
        {"id": "fresh", "text": "Fresh role", "createdAt": fresh_ms, "categories": {}},
        {"id": "stale", "text": "Stale role", "createdAt": stale_ms, "categories": {}},
    ]

    with patch(
        "app.ingestion.fetcher.LeverConnector.fetch_jobs",
        new=AsyncMock(return_value=payload),
    ):
        jobs, rejected = await fetch_company_jobs(company)

    assert rejected == 1
    assert len(jobs) == 1
    assert jobs[0]["id"] == "fresh"


@pytest.mark.asyncio
async def test_fetch_company_jobs_keeps_stale_jobs_on_baseline_run() -> None:
    reference = datetime(2026, 6, 19, tzinfo=timezone.utc)
    fresh_ms = int((reference - timedelta(days=1)).timestamp() * 1000)
    stale_ms = int((reference - timedelta(days=30)).timestamp() * 1000)
    company = Company(
        name="Example",
        board_token="example",
        platform="lever",
        is_active=True,
    )
    payload = [
        {"id": "fresh", "text": "Fresh role", "createdAt": fresh_ms, "categories": {}},
        {"id": "stale", "text": "Stale role", "createdAt": stale_ms, "categories": {}},
    ]

    with patch(
        "app.ingestion.fetcher.LeverConnector.fetch_jobs",
        new=AsyncMock(return_value=payload),
    ):
        jobs, rejected = await fetch_company_jobs(company, baseline_run=True)

    assert rejected == 0
    assert len(jobs) == 2
