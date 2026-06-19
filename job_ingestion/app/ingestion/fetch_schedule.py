from __future__ import annotations

import time
import zlib
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.ingestion.fetch_schedule_config import FetchScheduleConfig
from app.models.company import Company

WORKATASTARTUP_PLATFORM = "workatastartup"


@dataclass
class FetchSelectionResult:
    company_ids: list[UUID]
    schedule_metadata: dict


def current_tick(tick_minutes: int, *, now: Optional[float] = None) -> int:
    ts = now if now is not None else time.time()
    return int(ts // (tick_minutes * 60))


def company_shard(board_token: str, num_shards: int) -> int:
    if num_shards <= 1:
        return 0
    return zlib.crc32(board_token.encode("utf-8")) & 0xFFFFFFFF % num_shards


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _is_due(company: Company, interval_minutes: int, now: datetime) -> bool:
    if company.last_successful_fetch_at is None:
        return True
    age_seconds = (now - company.last_successful_fetch_at).total_seconds()
    return age_seconds >= interval_minutes * 60


def _sort_key(company: Company) -> tuple:
    last_fetch = company.last_successful_fetch_at
    if last_fetch is None:
        return (0, company.name.lower())
    return (1, last_fetch.timestamp(), company.name.lower())


def select_due_companies_from_rows(
    companies: list[Company],
    schedule: FetchScheduleConfig,
    *,
    now: Optional[datetime] = None,
    tick: Optional[int] = None,
    exclude_platforms: Optional[set[str]] = None,
) -> FetchSelectionResult:
    now = now or _utcnow()
    tick = tick if tick is not None else current_tick(schedule.tick_minutes)
    exclude = exclude_platforms or set()

    due_candidates: list[Company] = []
    shard_summary: dict[str, int] = {}

    for company in companies:
        if not company.is_active:
            continue
        if company.platform in exclude:
            continue

        interval = schedule.interval_minutes(company.platform, company.fetch_tier)
        if not _is_due(company, interval, now):
            continue

        num_shards = schedule.num_shards(company.platform, company.fetch_tier)
        shard = company_shard(company.board_token, num_shards)
        if shard != tick % num_shards:
            continue

        due_candidates.append(company)
        shard_key = f"{company.platform}:t{company.fetch_tier}"
        shard_summary[shard_key] = shard_summary.get(shard_key, 0) + 1

    due_candidates.sort(key=_sort_key)
    selected = due_candidates[: schedule.batch_cap]

    metadata = {
        "tick": tick,
        "tick_minutes": schedule.tick_minutes,
        "batch_cap": schedule.batch_cap,
        "companies_due": len(due_candidates),
        "companies_selected": len(selected),
        "shard_summary": shard_summary,
    }
    return FetchSelectionResult(
        company_ids=[company.id for company in selected],
        schedule_metadata=metadata,
    )


async def select_due_companies(
    db: AsyncSession,
    settings: Optional[Settings] = None,
) -> FetchSelectionResult:
    settings = settings or get_settings()
    schedule = settings.fetch_schedule()
    exclude = {WORKATASTARTUP_PLATFORM} if schedule.waas.dedicated_job else set()

    companies = (
        await db.scalars(select(Company).where(Company.is_active.is_(True)))
    ).all()
    return select_due_companies_from_rows(
        list(companies),
        schedule,
        exclude_platforms=exclude,
    )


async def select_waas_companies(
    db: AsyncSession,
) -> list[UUID]:
    companies = (
        await db.scalars(
            select(Company).where(
                Company.is_active.is_(True),
                Company.platform == WORKATASTARTUP_PLATFORM,
            )
        )
    ).all()
    return [company.id for company in companies]
