from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.ingestion.reprocessor import reprocess_jobs
from app.models.ingestion_event import IngestionEvent
from app.schemas.reprocessing import ReprocessingRequest, ReprocessingResponse

router = APIRouter(prefix="/reprocessing", tags=["reprocessing"])


@router.post("/jobs", response_model=ReprocessingResponse)
async def trigger_reprocessing(
    payload: ReprocessingRequest, db: AsyncSession = Depends(get_db)
) -> ReprocessingResponse:
    settings = get_settings()
    result = await reprocess_jobs(
        db=db,
        settings=settings,
        filters=payload.filters,
        target_version=payload.target_version,
        dry_run=payload.dry_run,
    )
    return ReprocessingResponse(
        matched_jobs=result.matched_jobs,
        processed_jobs=result.processed_jobs,
        success_count=result.success_count,
        failed_count=result.failed_count,
        dry_run=result.dry_run,
    )


@router.get("/runs")
async def list_reprocessing_runs(db: AsyncSession = Depends(get_db)) -> list[dict]:
    rows = (
        await db.scalars(
            select(IngestionEvent)
            .where(IngestionEvent.event_type == "reprocessing_completed")
            .order_by(desc(IngestionEvent.created_at))
            .limit(50)
        )
    ).all()
    return [
        {
            "id": str(row.id),
            "created_at": row.created_at.isoformat(),
            "metadata": row.event_metadata,
        }
        for row in rows
    ]
