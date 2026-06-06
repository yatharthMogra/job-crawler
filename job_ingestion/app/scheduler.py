from __future__ import annotations

from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import Settings, get_settings
from app.database import AsyncSessionLocal
from app.ingestion.constants import EventCategory, EventSeverity, EventType
from app.ingestion.events import write_event
from app.ingestion.pipeline import run_pipeline


def build_scheduler(settings: Optional[Settings] = None) -> AsyncIOScheduler:
    settings = settings or get_settings()
    scheduler = AsyncIOScheduler()

    async def scheduled_pipeline() -> None:
        async with AsyncSessionLocal() as db:
            await run_pipeline(db=db, run_type="scheduled", settings=settings)

    scheduler.add_job(
        scheduled_pipeline,
        trigger="interval",
        hours=settings.fetch_cadence_hours,
        id="pipeline-runner",
        max_instances=1,
        coalesce=True,
        replace_existing=True,
    )
    return scheduler


async def emit_scheduler_event(event_type: str) -> None:
    async with AsyncSessionLocal() as db:
        await write_event(
            db,
            event_type=event_type,
            category=EventCategory.SYSTEM,
            severity=EventSeverity.INFO,
        )
        await db.commit()
