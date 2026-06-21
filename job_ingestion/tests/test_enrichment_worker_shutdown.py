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
