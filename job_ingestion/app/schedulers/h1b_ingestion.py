from __future__ import annotations

import structlog

from app.database import AsyncSessionLocal
from app.ingestion.h1b.pipeline import run_h1b_ingestion

log = structlog.get_logger(__name__)


async def run_h1b_ingestion_job() -> None:
    """Annual H-1B rebuild: normalization, aggregation, summary (skip raw load)."""
    async with AsyncSessionLocal() as db:
        results = await run_h1b_ingestion(db, skip_load=True)
        log.info("h1b_scheduled_ingestion_complete", results=results)
