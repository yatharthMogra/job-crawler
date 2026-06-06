from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.ingestion_event import IngestionEvent
from app.schemas.events import EventSummaryOut, IngestionEventOut

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[IngestionEventOut])
async def list_events(
    category: Optional[str] = Query(default=None),
    severity: Optional[str] = Query(default=None),
    platform: Optional[str] = Query(default=None),
    company_id: Optional[str] = Query(default=None),
    since: Optional[datetime] = Query(default=None),
    until: Optional[datetime] = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> list[IngestionEventOut]:
    stmt = select(IngestionEvent).order_by(IngestionEvent.created_at.desc()).offset(offset).limit(limit)
    if category:
        stmt = stmt.where(IngestionEvent.event_category == category)
    if severity:
        stmt = stmt.where(IngestionEvent.severity == severity)
    if platform:
        stmt = stmt.where(IngestionEvent.platform == platform)
    if company_id:
        try:
            stmt = stmt.where(IngestionEvent.company_id == uuid.UUID(company_id))
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid company_id") from exc
    if since:
        stmt = stmt.where(IngestionEvent.created_at >= since)
    if until:
        stmt = stmt.where(IngestionEvent.created_at <= until)

    rows = (await db.scalars(stmt)).all()
    return [
        IngestionEventOut(
            id=str(row.id),
            event_type=row.event_type,
            event_category=row.event_category,
            severity=row.severity,
            platform=row.platform,
            company_id=str(row.company_id) if row.company_id else None,
            pipeline_run_id=str(row.pipeline_run_id) if row.pipeline_run_id else None,
            normalized_job_id=str(row.normalized_job_id) if row.normalized_job_id else None,
            metadata=row.event_metadata,
            created_at=row.created_at,
        )
        for row in rows
    ]


@router.get("/summary", response_model=list[EventSummaryOut])
async def events_summary(db: AsyncSession = Depends(get_db)) -> list[EventSummaryOut]:
    rows = (
        await db.execute(
            select(
                IngestionEvent.event_type,
                IngestionEvent.event_category,
                IngestionEvent.severity,
                func.count().label("count"),
            )
            .group_by(IngestionEvent.event_type, IngestionEvent.event_category, IngestionEvent.severity)
            .order_by(func.count().desc())
        )
    ).all()
    return [
        EventSummaryOut(
            event_type=event_type,
            event_category=event_category,
            severity=severity,
            count=int(count),
        )
        for event_type, event_category, severity, count in rows
    ]
