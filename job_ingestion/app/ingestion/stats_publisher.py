from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.database import AsyncSessionLocal
from app.ingestion.ops_stats import collect_ops_stats

logger = logging.getLogger(__name__)


def _stats_summary_for_log(stats: dict) -> dict:
    fetch_24h = stats.get("fetch", {}).get("last_24h", {})
    enrichment = stats.get("enrichment", {})
    jobs = stats.get("jobs", {})
    return {
        "trigger": stats.get("trigger"),
        "active_jobs": jobs.get("active"),
        "enriched_jobs": jobs.get("enriched"),
        "pending_enrichment": jobs.get("pending_enrichment"),
        "fetch_24h_jobs_new": fetch_24h.get("jobs_new"),
        "fetch_24h_companies_succeeded": fetch_24h.get("companies_succeeded"),
        "enrichment_completed_5m": enrichment.get("completed_last_5m"),
        "enrichment_completed_1h": enrichment.get("completed_last_1h"),
        "enrichment_failed_1h": enrichment.get("failed_last_1h"),
        "queue_queued": enrichment.get("queue", {}).get("queued", 0),
        "queue_in_progress": enrichment.get("queue", {}).get("in_progress", 0),
        "fetch_backpressure_active": stats.get("fetch_backpressure", {}).get("active", False),
        "workers": stats.get("enrichment_workers"),
    }


def write_stats_file(stats: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(f"{path.suffix}.tmp")
    temp_path.write_text(json.dumps(stats, indent=2, default=str), encoding="utf-8")
    temp_path.replace(path)


async def publish_ops_stats(
    db: AsyncSession,
    *,
    settings: Optional[Settings] = None,
    trigger: str = "manual",
) -> dict:
    settings = settings or get_settings()
    stats = await collect_ops_stats(db, settings=settings, trigger=trigger)
    write_stats_file(stats, settings.ingestion_stats_path)
    logger.info("ingestion_stats %s", json.dumps(_stats_summary_for_log(stats), default=str))
    return stats


async def publish_ops_stats_standalone(
    *,
    settings: Optional[Settings] = None,
    trigger: str = "scheduled",
) -> dict:
    settings = settings or get_settings()
    async with AsyncSessionLocal() as db:
        return await publish_ops_stats(db, settings=settings, trigger=trigger)
