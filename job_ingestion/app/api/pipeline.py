import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.ingestion.pipeline import run_pipeline
from app.models.pipeline_run import CompanyRunResult, PipelineRun
from app.schemas.pipeline import PipelineRunOut, TriggerPipelineOut

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


@router.post("/trigger", response_model=TriggerPipelineOut)
async def trigger_pipeline(db: AsyncSession = Depends(get_db)) -> TriggerPipelineOut:
    snapshot = await run_pipeline(db=db, run_type="manual")
    return TriggerPipelineOut(**snapshot.__dict__)


@router.get("/runs", response_model=list[PipelineRunOut])
async def list_pipeline_runs(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> list[PipelineRunOut]:
    runs = (
        await db.scalars(
            select(PipelineRun).order_by(desc(PipelineRun.started_at)).offset(offset).limit(limit)
        )
    ).all()
    return [
        PipelineRunOut(
            id=str(run.id),
            run_type=run.run_type,
            status=run.status,
            started_at=run.started_at.isoformat(),
            completed_at=run.completed_at.isoformat() if run.completed_at else None,
            total_companies=run.total_companies,
            successful_companies=run.successful_companies,
            failed_companies=run.failed_companies,
            jobs_fetched=run.jobs_fetched,
            jobs_new=run.jobs_new,
            jobs_updated=run.jobs_updated,
            jobs_unchanged=run.jobs_unchanged,
            jobs_removed=run.jobs_removed,
        )
        for run in runs
    ]


@router.get("/runs/{run_id}")
async def get_pipeline_run(run_id: str, db: AsyncSession = Depends(get_db)) -> dict:
    try:
        run_uuid = uuid.UUID(run_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid run id") from exc

    run = await db.get(PipelineRun, run_uuid)
    if run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")

    company_results = (
        await db.scalars(
            select(CompanyRunResult)
            .where(CompanyRunResult.pipeline_run_id == run.id)
            .order_by(CompanyRunResult.started_at.asc())
        )
    ).all()
    return {
        "run": {
            "id": str(run.id),
            "run_type": run.run_type,
            "status": run.status,
            "started_at": run.started_at.isoformat(),
            "completed_at": run.completed_at.isoformat() if run.completed_at else None,
            "total_companies": run.total_companies,
            "successful_companies": run.successful_companies,
            "failed_companies": run.failed_companies,
            "jobs_fetched": run.jobs_fetched,
            "jobs_new": run.jobs_new,
            "jobs_updated": run.jobs_updated,
            "jobs_unchanged": run.jobs_unchanged,
            "jobs_removed": run.jobs_removed,
            "error_summary": run.error_summary,
        },
        "companies": [
            {
                "id": str(row.id),
                "company_id": str(row.company_id),
                "status": row.status,
                "jobs_fetched": row.jobs_fetched,
                "jobs_new": row.jobs_new,
                "jobs_updated": row.jobs_updated,
                "jobs_unchanged": row.jobs_unchanged,
                "jobs_removed": row.jobs_removed,
                "error_message": row.error_message,
                "started_at": row.started_at.isoformat(),
                "completed_at": row.completed_at.isoformat(),
            }
            for row in company_results
        ],
    }
