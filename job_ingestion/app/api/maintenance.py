from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.archival.archiver import run_all_cleanup
from app.archival.active_cleanup import run_active_cleanup
from app.archival.archive_cleanup import run_archive_cleanup
from app.database import get_db
from app.ingestion.enrichment_worker import cleanup_orphan_enrichment_queue

router = APIRouter(prefix="/maintenance", tags=["maintenance"])


@router.post("/cleanup")
async def trigger_full_cleanup(db: AsyncSession = Depends(get_db)) -> dict:
    return await run_all_cleanup(db)


@router.post("/cleanup/active")
async def trigger_active_cleanup(db: AsyncSession = Depends(get_db)) -> dict:
    return await run_active_cleanup(db)


@router.post("/cleanup/archive")
async def trigger_archive_cleanup(db: AsyncSession = Depends(get_db)) -> dict:
    return await run_archive_cleanup(db)


@router.post("/cleanup/enrichment-queue")
async def trigger_enrichment_queue_cleanup(db: AsyncSession = Depends(get_db)) -> dict:
    return await cleanup_orphan_enrichment_queue(db)
