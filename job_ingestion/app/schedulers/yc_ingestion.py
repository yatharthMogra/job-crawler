from __future__ import annotations

import structlog
from sqlalchemy import select

from app.config import get_settings
from app.database import AsyncSessionLocal
from app.ingestion.alerts import write_failure_alert
from app.ingestion.connectors.yc_directory import crawl_yc_directory
from app.ingestion.constants import EventCategory, EventSeverity, EventType
from app.ingestion.events import write_event
from app.models.company import Company
from app.models.pipeline_run import CompanyRunResult
from app.utils.yc_company_sync import upsert_discovered_companies

log = structlog.get_logger(__name__)


async def run_yc_directory_crawl_job(*, dry_run: bool = False) -> dict[str, int | bool]:
    settings = get_settings()
    async with AsyncSessionLocal() as db:
        existing_tokens = set((await db.scalars(select(Company.board_token))).all())
        result = await crawl_yc_directory(settings=settings, existing_tokens=existing_tokens)
        summary = {
            "dry_run": dry_run,
            "greenhouse": len(result.greenhouse_tokens),
            "lever": len(result.lever_slugs),
            "ashby": len(result.ashby_slugs),
            "workday": len(result.workday_discoveries),
            "yc_native": len(result.yc_native_companies),
            "skipped_existing": result.skipped_existing,
        }
        if dry_run:
            log.info("yc_directory_crawl_dry_run", **summary)
            return summary

        sync_result = await upsert_discovered_companies(db, result)
        summary.update(
            {
                "inserted": sync_result.inserted,
                "skipped_existing": sync_result.skipped_existing,
                "workday_flagged": sync_result.workday_flagged,
            }
        )
        log.info("yc_directory_crawl_complete", **summary)
        return summary


async def run_yc_waas_health_check_job() -> None:
    settings = get_settings()
    async with AsyncSessionLocal() as db:
        waas_company = await db.scalar(
            select(Company).where(
                Company.platform == "workatastartup",
                Company.is_active.is_(True),
            )
        )
        if waas_company is None:
            log.warning("yc_waas_health_check_skipped", reason="no_active_workatastartup_company")
            return

        recent_runs = (
            await db.scalars(
                select(CompanyRunResult)
                .where(CompanyRunResult.company_id == waas_company.id)
                .order_by(CompanyRunResult.completed_at.desc())
                .limit(3)
            )
        ).all()
        if len(recent_runs) < 3:
            return

        if all(run.jobs_fetched == 0 and run.status == "success" for run in recent_runs):
            message = (
                "YC Work at a Startup connector returned 0 jobs for 3 consecutive pipeline runs"
            )
            write_failure_alert(
                alerts_path=settings.alerts_path,
                company=waas_company,
                consecutive_failures=3,
                last_error=message,
            )
            await write_event(
                db,
                event_type=EventType.SOURCE_FAILURE_THRESHOLD_REACHED,
                category=EventCategory.SOURCE,
                severity=EventSeverity.CRITICAL,
                platform=waas_company.platform,
                company_id=waas_company.id,
                metadata={"health_check": "yc_waas_zero_jobs", "message": message},
            )
            await db.commit()
            log.error("yc_waas_health_check_failed", message=message)
