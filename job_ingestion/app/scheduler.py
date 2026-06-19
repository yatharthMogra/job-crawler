from __future__ import annotations

from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.archival.active_cleanup import run_active_cleanup
from app.archival.archive_cleanup import run_archive_cleanup
from app.config import Settings, get_settings
from app.database import AsyncSessionLocal
from app.ingestion.constants import EventCategory, EventSeverity, EventType
from app.ingestion.events import write_event
from app.ingestion.fetch_schedule import select_waas_companies
from app.ingestion.pipeline import run_pipeline


def build_scheduler(settings: Optional[Settings] = None) -> AsyncIOScheduler:
    settings = settings or get_settings()
    schedule = settings.fetch_schedule()
    scheduler = AsyncIOScheduler()

    async def scheduled_fetch_tick() -> None:
        async with AsyncSessionLocal() as db:
            await run_pipeline(db=db, run_type="scheduled", settings=settings)

    async def scheduled_waas_fetch() -> None:
        async with AsyncSessionLocal() as db:
            company_ids = await select_waas_companies(db)
            if not company_ids:
                return
            await run_pipeline(
                db=db,
                run_type="scheduled_waas",
                settings=settings,
                company_ids=company_ids,
                schedule_metadata={"waas_dedicated": True, "companies_selected": len(company_ids)},
            )

    async def run_active_cleanup_job() -> None:
        async with AsyncSessionLocal() as db:
            await run_active_cleanup(db)

    async def run_archive_cleanup_job() -> None:
        async with AsyncSessionLocal() as db:
            await run_archive_cleanup(db)

    async def run_h1b_ingestion_job() -> None:
        from app.schedulers.h1b_ingestion import run_h1b_ingestion_job as _run_h1b

        await _run_h1b()

    async def run_yc_directory_crawl_job() -> None:
        from app.schedulers.yc_ingestion import run_yc_directory_crawl_job as _run_yc_directory

        await _run_yc_directory()

    async def run_yc_waas_health_check_job() -> None:
        from app.schedulers.yc_ingestion import run_yc_waas_health_check_job as _run_yc_health

        await _run_yc_health()

    async def publish_stats_job() -> None:
        from app.ingestion.stats_publisher import publish_ops_stats_standalone

        await publish_ops_stats_standalone(settings=settings, trigger="scheduled")

    scheduler.add_job(
        publish_stats_job,
        trigger="interval",
        minutes=settings.ingestion_stats_interval_minutes,
        id="ops-stats",
        max_instances=1,
        coalesce=True,
        replace_existing=True,
    )
    scheduler.add_job(
        scheduled_fetch_tick,
        trigger="interval",
        minutes=schedule.tick_minutes,
        id="fetch-tick",
        max_instances=1,
        coalesce=True,
        replace_existing=True,
    )
    if schedule.waas.dedicated_job:
        scheduler.add_job(
            scheduled_waas_fetch,
            trigger="interval",
            minutes=schedule.waas.interval_minutes,
            id="waas-fetch",
            max_instances=1,
            coalesce=True,
            replace_existing=True,
        )
    scheduler.add_job(
        run_active_cleanup_job,
        trigger="cron",
        hour=2,
        minute=0,
        id="active_cleanup",
        replace_existing=True,
    )
    scheduler.add_job(
        run_archive_cleanup_job,
        trigger="cron",
        hour=2,
        minute=30,
        id="archive_cleanup",
        replace_existing=True,
    )
    scheduler.add_job(
        run_h1b_ingestion_job,
        trigger="cron",
        month=2,
        day=15,
        hour=3,
        minute=0,
        id="h1b-ingestion",
        max_instances=1,
        replace_existing=True,
    )
    scheduler.add_job(
        run_yc_directory_crawl_job,
        trigger="cron",
        day_of_week="sun",
        hour=1,
        minute=0,
        id="yc-directory-crawl",
        max_instances=1,
        replace_existing=True,
    )
    scheduler.add_job(
        run_yc_waas_health_check_job,
        trigger="cron",
        hour=4,
        minute=0,
        id="yc-waas-health-check",
        max_instances=1,
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
