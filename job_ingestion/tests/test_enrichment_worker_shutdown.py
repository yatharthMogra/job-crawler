from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from app.config import Settings
from app.ingestion.enrichment_worker import EnrichmentWorker


@pytest.mark.asyncio
async def test_run_forever_exits_promptly_on_stop() -> None:
    settings = Settings(
        gemini_api_keys="test-key",
        enrichment_window_seconds=45,
    )
    worker = EnrichmentWorker(settings, worker_id=0, worker_count=1)

    with patch(
        "app.ingestion.enrichment_worker.process_enrichment_window",
        new=AsyncMock(return_value=(0, 0)),
    ):
        task = asyncio.create_task(worker.run_forever())
        await asyncio.sleep(0.05)
        worker.stop()
        await asyncio.wait_for(task, timeout=1.0)


@pytest.mark.asyncio
async def test_run_forever_skips_window_when_capacity_blocks() -> None:
    settings = Settings(
        gemini_api_keys="test-key",
        enrichment_window_seconds=45,
    )
    worker = EnrichmentWorker(settings, worker_id=0, worker_count=1)
    worker._capacity._mode = "daily_exhausted"

    fake_db = AsyncMock()
    fake_db.commit = AsyncMock()

    class _FakeSession:
        async def __aenter__(self):
            return fake_db

        async def __aexit__(self, *args):
            return None

    process_window = AsyncMock(return_value=(0, 0))
    with patch(
        "app.ingestion.enrichment_worker.AsyncSessionLocal",
        return_value=_FakeSession(),
    ):
        with patch.object(worker._capacity, "load_or_create", new=AsyncMock()):
            with patch.object(worker._capacity, "tick"):
                with patch(
                    "app.ingestion.enrichment_worker.process_enrichment_window",
                    new=process_window,
                ):
                    with patch.object(worker, "_sleep_until_stop", new=AsyncMock(return_value=True)):
                        await worker.run_forever()

    process_window.assert_not_called()
