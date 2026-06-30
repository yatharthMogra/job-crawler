from __future__ import annotations

import structlog

from app.config import Settings, get_settings
from app.notification.company_watch import run_company_watch_processor
from app.notification.digest import run_digest_scheduler

log = structlog.get_logger(__name__)


async def run_notification_pipeline(settings: Settings | None = None) -> None:
    """Run both digest and company watch processors (manual trigger)."""
    settings = settings or get_settings()
    await run_digest_scheduler(settings)
    await run_company_watch_processor(settings)


async def run_digest_pipeline(settings: Settings | None = None) -> None:
    await run_digest_scheduler(settings or get_settings())


async def run_company_watch_pipeline(settings: Settings | None = None) -> None:
    await run_company_watch_processor(settings or get_settings())
