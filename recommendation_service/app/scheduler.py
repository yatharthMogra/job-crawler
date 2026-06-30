from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import Settings
from app.notification.company_watch import run_company_watch_processor
from app.notification.digest import run_digest_scheduler


def create_scheduler(settings: Settings) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_digest_scheduler,
        trigger="interval",
        minutes=settings.digest_scheduler_poll_minutes,
        id="digest_scheduler",
        replace_existing=True,
        kwargs={"settings": settings},
    )
    scheduler.add_job(
        run_company_watch_processor,
        trigger="interval",
        minutes=settings.company_watch_poll_minutes,
        id="company_watch_processor",
        replace_existing=True,
        kwargs={"settings": settings},
    )
    return scheduler
