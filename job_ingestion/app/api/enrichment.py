from __future__ import annotations

import uuid
from datetime import date, datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import String, and_, case, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.models.enrichment_batch import EnrichmentBatch
from app.models.enrichment_batch_item import EnrichmentBatchItem
from app.models.enrichment_queue import EnrichmentQueue
from app.models.job_enrichment import JobEnrichment
from app.models.normalized_job import NormalizedJob
from app.models.pipeline_run import PipelineRun
from app.models.raw_job import RawJob

router = APIRouter(prefix="/enrichment", tags=["enrichment"])
compat_router = APIRouter(prefix="/enrichments", tags=["enrichment"])


@router.get("/queue")
async def list_enrichment_queue(
    status_filter: str | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    stmt = select(EnrichmentQueue).order_by(desc(EnrichmentQueue.updated_at)).limit(limit)
    if status_filter:
        stmt = stmt.where(EnrichmentQueue.status == status_filter)
    rows = (await db.scalars(stmt)).all()
    return [
        {
            "id": str(row.id),
            "normalized_job_id": str(row.normalized_job_id),
            "pipeline_run_id": str(row.pipeline_run_id) if row.pipeline_run_id else None,
            "source": row.source,
            "status": row.status,
            "attempt_count": row.attempt_count,
            "priority": row.priority,
            "next_retry_at": row.next_retry_at.isoformat() if row.next_retry_at else None,
            "estimated_input_tokens": row.estimated_input_tokens,
            "last_actual_input_tokens": row.last_actual_input_tokens,
            "last_actual_output_tokens": row.last_actual_output_tokens,
            "last_failure_reason": row.last_failure_reason,
            "last_error": row.last_error,
            "created_at": row.created_at.isoformat(),
            "updated_at": row.updated_at.isoformat(),
        }
        for row in rows
    ]


@router.get("/batches")
async def list_enrichment_batches(
    limit: int = Query(default=100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    rows = (await db.scalars(select(EnrichmentBatch).order_by(desc(EnrichmentBatch.started_at)).limit(limit))).all()
    return [
        {
            "id": str(row.id),
            "pipeline_run_id": str(row.pipeline_run_id) if row.pipeline_run_id else None,
            "source": row.source,
            "status": row.status,
            "jobs_total": row.jobs_total,
            "jobs_first_attempt": row.jobs_first_attempt,
            "jobs_retry": row.jobs_retry,
            "estimated_input_tokens": row.estimated_input_tokens,
            "actual_input_tokens": row.actual_input_tokens,
            "actual_output_tokens": row.actual_output_tokens,
            "latency_ms": row.latency_ms,
            "failure_reason": row.failure_reason,
            "last_error": row.last_error,
            "started_at": row.started_at.isoformat(),
            "completed_at": row.completed_at.isoformat() if row.completed_at else None,
        }
        for row in rows
    ]


@router.get("/batches/{batch_id}")
async def get_enrichment_batch(batch_id: str, db: AsyncSession = Depends(get_db)) -> dict:
    try:
        batch_uuid = uuid.UUID(batch_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid batch id") from exc

    batch = await db.get(EnrichmentBatch, batch_uuid)
    if batch is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")

    items = (
        await db.scalars(
            select(EnrichmentBatchItem)
            .where(EnrichmentBatchItem.batch_id == batch.id)
            .order_by(EnrichmentBatchItem.created_at.asc())
        )
    ).all()
    return {
        "batch": {
            "id": str(batch.id),
            "pipeline_run_id": str(batch.pipeline_run_id) if batch.pipeline_run_id else None,
            "source": batch.source,
            "status": batch.status,
            "jobs_total": batch.jobs_total,
            "jobs_first_attempt": batch.jobs_first_attempt,
            "jobs_retry": batch.jobs_retry,
            "estimated_input_tokens": batch.estimated_input_tokens,
            "actual_input_tokens": batch.actual_input_tokens,
            "actual_output_tokens": batch.actual_output_tokens,
            "latency_ms": batch.latency_ms,
            "failure_reason": batch.failure_reason,
            "last_error": batch.last_error,
            "started_at": batch.started_at.isoformat(),
            "completed_at": batch.completed_at.isoformat() if batch.completed_at else None,
        },
        "items": [
            {
                "id": str(item.id),
                "queue_id": str(item.queue_id) if item.queue_id else None,
                "normalized_job_id": str(item.normalized_job_id),
                "status": item.status,
                "priority_bucket": item.priority_bucket,
                "attempt_number": item.attempt_number,
                "estimated_input_tokens": item.estimated_input_tokens,
                "actual_input_tokens": item.actual_input_tokens,
                "actual_output_tokens": item.actual_output_tokens,
                "failure_reason": item.failure_reason,
                "last_error": item.last_error,
                "created_at": item.created_at.isoformat(),
            }
            for item in items
        ],
    }


@router.get("/jobs/{job_id}/history")
async def get_job_enrichment_history(job_id: str, db: AsyncSession = Depends(get_db)) -> dict:
    try:
        job_uuid = uuid.UUID(job_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid job id") from exc

    queue_row = await db.scalar(select(EnrichmentQueue).where(EnrichmentQueue.normalized_job_id == job_uuid))
    batch_items = (
        await db.scalars(
            select(EnrichmentBatchItem)
            .where(EnrichmentBatchItem.normalized_job_id == job_uuid)
            .order_by(desc(EnrichmentBatchItem.created_at))
        )
    ).all()
    enrichments = (
        await db.scalars(
            select(JobEnrichment)
            .where(JobEnrichment.normalized_job_id == job_uuid)
            .order_by(desc(JobEnrichment.created_at))
            .limit(50)
        )
    ).all()
    return {
        "queue": (
            {
                "id": str(queue_row.id),
                "status": queue_row.status,
                "attempt_count": queue_row.attempt_count,
                "estimated_input_tokens": queue_row.estimated_input_tokens,
                "last_actual_input_tokens": queue_row.last_actual_input_tokens,
                "last_actual_output_tokens": queue_row.last_actual_output_tokens,
                "last_failure_reason": queue_row.last_failure_reason,
                "updated_at": queue_row.updated_at.isoformat(),
            }
            if queue_row
            else None
        ),
        "batch_items": [
            {
                "id": str(item.id),
                "batch_id": str(item.batch_id),
                "status": item.status,
                "priority_bucket": item.priority_bucket,
                "attempt_number": item.attempt_number,
                "estimated_input_tokens": item.estimated_input_tokens,
                "actual_input_tokens": item.actual_input_tokens,
                "actual_output_tokens": item.actual_output_tokens,
                "failure_reason": item.failure_reason,
                "created_at": item.created_at.isoformat(),
            }
            for item in batch_items
        ],
        "enrichments": [
            {
                "id": str(row.id),
                "batch_id": str(row.enrichment_batch_id) if row.enrichment_batch_id else None,
                "status": row.status,
                "failure_reason": row.failure_reason,
                "input_tokens": row.input_tokens,
                "output_tokens": row.output_tokens,
                "latency_ms": row.latency_ms,
                "created_at": row.created_at.isoformat(),
            }
            for row in enrichments
        ],
    }


@compat_router.get("/usage")
async def get_enrichment_usage(
    period: str = Query(default="day", pattern="^(day|month|run)$"),
    split_by: str = Query(default="platform", pattern="^(platform|company)$"),
    date_value: str | None = Query(default=None, alias="date"),
    month: str | None = Query(default=None),
    run_id: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> dict:
    settings = get_settings()
    time_filters = await _build_time_filters(
        period=period,
        date_value=date_value,
        month=month,
        run_id=run_id,
        db=db,
    )
    split_col = RawJob.platform if split_by == "platform" else NormalizedJob.company_name
    split_key = "platform" if split_by == "platform" else "company"
    success_expr = func.sum(case((JobEnrichment.status == "success", 1), else_=0))
    failure_expr = func.sum(case((JobEnrichment.status != "success", 1), else_=0))
    query = (
        select(
            split_col.label(split_key),
            func.coalesce(func.sum(JobEnrichment.input_tokens), 0).label("input_tokens"),
            func.coalesce(func.sum(JobEnrichment.output_tokens), 0).label("output_tokens"),
            func.count(JobEnrichment.id).label("enrichment_count"),
            func.coalesce(failure_expr, 0).label("failure_count"),
            func.coalesce(func.avg(JobEnrichment.latency_ms), 0).label("avg_latency_ms"),
            func.coalesce(success_expr, 0).label("success_count"),
        )
        .select_from(JobEnrichment)
        .join(NormalizedJob, NormalizedJob.id == JobEnrichment.normalized_job_id)
        .join(RawJob, RawJob.id == NormalizedJob.raw_job_id, isouter=True)
        .where(and_(*time_filters))
        .group_by(split_col)
        .order_by(func.coalesce(func.sum(JobEnrichment.input_tokens), 0).desc())
    )
    rows = (await db.execute(query)).all()
    breakdown = []
    total_input = 0
    total_output = 0
    total_enrichments = 0
    total_failures = 0
    for row in rows:
        input_tokens = int(row.input_tokens or 0)
        output_tokens = int(row.output_tokens or 0)
        enrichment_count = int(row.enrichment_count or 0)
        failure_count = int(row.failure_count or 0)
        avg_latency = float(row.avg_latency_ms or 0)
        estimated_cost = _calculate_estimated_cost(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            input_price=settings.llm_input_token_cost_per_1k,
            output_price=settings.llm_output_token_cost_per_1k,
        )
        breakdown.append(
            {
                split_key: row[0] or "unknown",
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "enrichment_count": enrichment_count,
                "failure_count": failure_count,
                "avg_latency_ms": avg_latency,
                "estimated_cost": estimated_cost,
            }
        )
        total_input += input_tokens
        total_output += output_tokens
        total_enrichments += enrichment_count
        total_failures += failure_count

    failure_rate = (total_failures / total_enrichments * 100) if total_enrichments else 0
    return {
        "period": period,
        "split_by": split_by,
        "summary": {
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "estimated_cost": _calculate_estimated_cost(
                input_tokens=total_input,
                output_tokens=total_output,
                input_price=settings.llm_input_token_cost_per_1k,
                output_price=settings.llm_output_token_cost_per_1k,
            ),
            "enrichment_count": total_enrichments,
            "failure_count": total_failures,
            "enrichment_failure_rate": round(failure_rate, 2),
        },
        "breakdown": breakdown,
    }


@compat_router.get("/usage/trend")
async def get_enrichment_usage_trend(
    period: str = Query(default="day", pattern="^(day|month|run)$"),
    days: int = Query(default=30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
) -> dict:
    settings = get_settings()
    if period == "run":
        query = (
            select(
                func.coalesce(PipelineRun.id.cast(String), "unknown").label("bucket"),
                func.coalesce(func.sum(JobEnrichment.input_tokens), 0).label("input_tokens"),
                func.coalesce(func.sum(JobEnrichment.output_tokens), 0).label("output_tokens"),
            )
            .select_from(JobEnrichment)
            .join(EnrichmentBatch, EnrichmentBatch.id == JobEnrichment.enrichment_batch_id, isouter=True)
            .join(PipelineRun, PipelineRun.id == EnrichmentBatch.pipeline_run_id, isouter=True)
            .group_by(PipelineRun.id)
            .order_by(func.max(JobEnrichment.created_at).desc())
            .limit(days)
        )
    else:
        now = datetime.now(timezone.utc)
        earliest = now - timedelta(days=days)
        bucket = (
            func.date_trunc("month", JobEnrichment.created_at)
            if period == "month"
            else func.date_trunc("day", JobEnrichment.created_at)
        )
        query = (
            select(
                bucket.label("bucket"),
                func.coalesce(func.sum(JobEnrichment.input_tokens), 0).label("input_tokens"),
                func.coalesce(func.sum(JobEnrichment.output_tokens), 0).label("output_tokens"),
            )
            .where(JobEnrichment.created_at >= earliest)
            .group_by(bucket)
            .order_by(bucket.asc())
        )

    rows = (await db.execute(query)).all()
    points = []
    for row in rows:
        input_tokens = int(row.input_tokens or 0)
        output_tokens = int(row.output_tokens or 0)
        points.append(
            {
                "bucket": str(row.bucket),
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "estimated_cost": _calculate_estimated_cost(
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    input_price=settings.llm_input_token_cost_per_1k,
                    output_price=settings.llm_output_token_cost_per_1k,
                ),
            }
        )
    return {"period": period, "points": points}


def _calculate_estimated_cost(
    *,
    input_tokens: int,
    output_tokens: int,
    input_price: float,
    output_price: float,
) -> float:
    return round((input_tokens / 1000 * input_price) + (output_tokens / 1000 * output_price), 6)


async def _build_time_filters(
    *,
    period: str,
    date_value: str | None,
    month: str | None,
    run_id: str | None,
    db: AsyncSession,
) -> list:
    filters = []
    if period == "day":
        if date_value:
            selected = date.fromisoformat(date_value)
            start = datetime(selected.year, selected.month, selected.day, tzinfo=timezone.utc)
        else:
            now = datetime.now(timezone.utc)
            start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
        end = start + timedelta(days=1)
        filters.extend([JobEnrichment.created_at >= start, JobEnrichment.created_at < end])
    elif period == "month":
        if month:
            parts = month.split("-")
            if len(parts) != 2:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid month format")
            start = datetime(int(parts[0]), int(parts[1]), 1, tzinfo=timezone.utc)
        else:
            now = datetime.now(timezone.utc)
            start = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
        end = datetime(start.year + (1 if start.month == 12 else 0), (start.month % 12) + 1, 1, tzinfo=timezone.utc)
        filters.extend([JobEnrichment.created_at >= start, JobEnrichment.created_at < end])
    elif period == "run":
        if not run_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="run_id is required for period=run")
        try:
            run_uuid = uuid.UUID(run_id)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid run_id") from exc
        run = await db.get(PipelineRun, run_uuid)
        if run is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pipeline run not found")
        end = run.completed_at or datetime.now(timezone.utc)
        filters.extend([JobEnrichment.created_at >= run.started_at, JobEnrichment.created_at <= end])
    return filters


