from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from app.config import Settings
from app.ingestion.enrichment_worker import _purge_if_stale_before_enrichment
from app.ingestion.job_freshness import FreshnessVerdict, refresh_posted_at_verdict


def test_refresh_posted_at_verdict_stale_lever() -> None:
    reference = datetime(2026, 6, 19, tzinfo=timezone.utc)
    stale_ms = int((reference - timedelta(days=30)).timestamp() * 1000)
    posted_at, verdict = refresh_posted_at_verdict(
        None,
        {"id": "1", "createdAt": stale_ms, "categories": {}},
        "lever",
        settings=Settings(job_max_age_days=7),
    )
    assert posted_at is not None
    assert verdict == FreshnessVerdict.STALE


@pytest.mark.asyncio
async def test_purge_if_stale_before_enrichment_purges_old_job() -> None:
    settings = Settings(job_max_age_days=7)
    reference = datetime(2026, 6, 19, tzinfo=timezone.utc)
    stale_ms = int((reference - timedelta(days=30)).timestamp() * 1000)
    normalized = SimpleNamespace(
        id=uuid4(),
        raw_job_id=uuid4(),
        job_archive_id=None,
        posted_at=None,
        external_job_id="lever-1",
    )
    raw_job = SimpleNamespace(
        raw_api_response={"id": "lever-1", "createdAt": stale_ms, "categories": {}},
    )
    company = SimpleNamespace(platform="lever", id=uuid4())
    queue_row = SimpleNamespace(pipeline_run_id=None)
    db = AsyncMock()

    with patch("app.ingestion.enrichment_worker.write_event", new=AsyncMock()):
        with patch("app.ingestion.enrichment_worker.purge_normalized_jobs", new=AsyncMock(return_value=1)) as purge:
            purged = await _purge_if_stale_before_enrichment(
                db,
                normalized=normalized,
                raw_job=raw_job,
                company=company,
                queue_row=queue_row,
                settings=settings,
            )

    assert purged is True
    purge.assert_awaited_once()


@pytest.mark.asyncio
async def test_purge_if_stale_before_enrichment_keeps_fresh_job() -> None:
    settings = Settings(job_max_age_days=7)
    reference = datetime(2026, 6, 19, tzinfo=timezone.utc)
    fresh_ms = int((reference - timedelta(days=2)).timestamp() * 1000)
    normalized = SimpleNamespace(
        id=uuid4(),
        raw_job_id=uuid4(),
        job_archive_id=None,
        posted_at=None,
        external_job_id="lever-1",
    )
    raw_job = SimpleNamespace(
        raw_api_response={"id": "lever-1", "createdAt": fresh_ms, "categories": {}},
    )
    company = SimpleNamespace(platform="lever", id=uuid4())
    queue_row = SimpleNamespace(pipeline_run_id=None)
    db = AsyncMock()

    with patch("app.ingestion.enrichment_worker.purge_normalized_jobs", new=AsyncMock()) as purge:
        purged = await _purge_if_stale_before_enrichment(
            db,
            normalized=normalized,
            raw_job=raw_job,
            company=company,
            queue_row=queue_row,
            settings=settings,
        )

    assert purged is False
    purge.assert_not_awaited()
