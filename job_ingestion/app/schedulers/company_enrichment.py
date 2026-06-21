from __future__ import annotations

from app.database import AsyncSessionLocal
from app.ingestion.company_enrichment.worker import run_company_enrichment_batch


async def run_company_enrichment_job() -> dict[str, int]:
    async with AsyncSessionLocal() as db:
        return await run_company_enrichment_batch(db)
