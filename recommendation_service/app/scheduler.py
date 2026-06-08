from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import Settings
from app.notification.pipeline import run_notification_pipeline


def create_scheduler(settings: Settings) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_notification_pipeline,
        trigger="interval",
        hours=settings.notification_cadence_hours,
        id="notification_pipeline",
        replace_existing=True,
        kwargs={"settings": settings},
    )
    return scheduler
