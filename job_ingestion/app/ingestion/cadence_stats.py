from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Literal, Optional
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.ingestion.fetch_schedule_config import FetchScheduleConfig

CadenceHealth = Literal["on_target", "drifting", "behind", "never_fetched"]

# Observed interval needs at least two successful polls.
_MAX_SUCCESS_SAMPLES = 8


@dataclass(frozen=True)
class CompanyCadenceRow:
    id: str
    name: str
    platform: str
    tier: int
    is_active: bool
    target_cadence_hours: float
    actual_cadence_hours: Optional[float]
    hours_since_last_success: Optional[float]
    observed_interval_hours: Optional[float]
    last_successful_fetch_at: Optional[datetime]
    consecutive_failures: int
    health: CadenceHealth
    drift_ratio: Optional[float]


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def compute_health(
    *,
    actual_cadence_hours: Optional[float],
    target_cadence_hours: float,
) -> CadenceHealth:
    if actual_cadence_hours is None:
        return "never_fetched"
    if target_cadence_hours <= 0:
        return "behind"
    ratio = actual_cadence_hours / target_cadence_hours
    if ratio <= 1.10:
        return "on_target"
    if ratio <= 1.40:
        return "drifting"
    return "behind"


def _mean_success_interval_hours(timestamps: list[datetime]) -> Optional[float]:
    """Mean gap between consecutive successful poll times (newest first or any order)."""
    if len(timestamps) < 2:
        return None
    ordered = sorted(timestamps)
    gaps: list[float] = []
    for prev, curr in zip(ordered, ordered[1:]):
        delta_hours = (curr - prev).total_seconds() / 3600.0
        if delta_hours > 0:
            gaps.append(delta_hours)
    if not gaps:
        return None
    return sum(gaps) / len(gaps)


def _resolve_actual_cadence(
    *,
    observed_interval_hours: Optional[float],
    hours_since_last_success: Optional[float],
) -> Optional[float]:
    if observed_interval_hours is not None:
        return observed_interval_hours
    return hours_since_last_success


def build_company_cadence(
    *,
    company_id: UUID | str,
    name: str,
    platform: str,
    fetch_tier: int,
    is_active: bool,
    consecutive_fetch_failures: int,
    last_successful_fetch_at: Optional[datetime],
    success_timestamps: list[datetime],
    schedule: FetchScheduleConfig,
    now: Optional[datetime] = None,
) -> CompanyCadenceRow:
    now = now or _utcnow()
    tier = int(fetch_tier)
    target_minutes = schedule.interval_minutes(platform, tier)
    target_hours = target_minutes / 60.0

    hours_since: Optional[float] = None
    if last_successful_fetch_at is not None:
        last = last_successful_fetch_at
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        hours_since = max(0.0, (now - last).total_seconds() / 3600.0)

    observed = _mean_success_interval_hours(success_timestamps)
    actual = _resolve_actual_cadence(
        observed_interval_hours=observed,
        hours_since_last_success=hours_since,
    )
    # Never fetched: no last success and no observed interval.
    if last_successful_fetch_at is None and observed is None:
        actual = None

    health = compute_health(actual_cadence_hours=actual, target_cadence_hours=target_hours)
    drift_ratio = (actual / target_hours) if actual is not None and target_hours > 0 else None

    return CompanyCadenceRow(
        id=str(company_id),
        name=name,
        platform=platform,
        tier=tier,
        is_active=is_active,
        target_cadence_hours=round(target_hours, 4),
        actual_cadence_hours=round(actual, 4) if actual is not None else None,
        hours_since_last_success=round(hours_since, 4) if hours_since is not None else None,
        observed_interval_hours=round(observed, 4) if observed is not None else None,
        last_successful_fetch_at=last_successful_fetch_at,
        consecutive_failures=int(consecutive_fetch_failures or 0),
        health=health,
        drift_ratio=round(drift_ratio, 4) if drift_ratio is not None else None,
    )


def _serialize_company(row: CompanyCadenceRow) -> dict[str, Any]:
    return {
        "id": row.id,
        "name": row.name,
        "platform": row.platform,
        "tier": row.tier,
        "is_active": row.is_active,
        "target_cadence_hours": row.target_cadence_hours,
        "actual_cadence_hours": row.actual_cadence_hours,
        "hours_since_last_success": row.hours_since_last_success,
        "observed_interval_hours": row.observed_interval_hours,
        "last_successful_fetch_at": (
            row.last_successful_fetch_at.isoformat() if row.last_successful_fetch_at else None
        ),
        "consecutive_failures": row.consecutive_failures,
        "health": row.health,
        "drift_ratio": row.drift_ratio,
    }


def _summary(companies: list[CompanyCadenceRow]) -> dict[str, Any]:
    with_actual = [
        c
        for c in companies
        if c.actual_cadence_hours is not None and c.target_cadence_hours > 0
    ]
    avg_drift_pct = 0.0
    if with_actual:
        avg_drift_pct = sum(
            (float(c.actual_cadence_hours) / c.target_cadence_hours - 1.0) * 100.0
            for c in with_actual
        ) / len(with_actual)
    return {
        "total": len(companies),
        "never_fetched": sum(1 for c in companies if c.health == "never_fetched"),
        "on_target": sum(1 for c in companies if c.health == "on_target"),
        "drifting": sum(1 for c in companies if c.health == "drifting"),
        "behind": sum(1 for c in companies if c.health == "behind"),
        "avg_drift_pct": round(avg_drift_pct, 1),
    }


async def collect_cadence_stats(
    db: AsyncSession,
    *,
    settings: Settings,
    include_inactive: bool = False,
) -> dict[str, Any]:
    now = _utcnow()
    schedule = settings.fetch_schedule()

    company_rows = (
        await db.execute(
            text(
                """
                SELECT
                  id,
                  name,
                  platform,
                  fetch_tier,
                  is_active,
                  consecutive_fetch_failures,
                  last_successful_fetch_at
                FROM companies
                WHERE (:include_inactive OR is_active)
                ORDER BY name ASC
                """
            ),
            {"include_inactive": include_inactive},
        )
    ).all()

    company_id_set = {row.id for row in company_rows}
    success_by_company: dict[Any, list[datetime]] = {cid: [] for cid in company_id_set}

    if company_id_set:
        # Latest successful polls per company (bounded) for observed cadence.
        poll_rows = (
            await db.execute(
                text(
                    """
                    SELECT company_id, completed_at
                    FROM (
                      SELECT
                        company_id,
                        completed_at,
                        ROW_NUMBER() OVER (
                          PARTITION BY company_id
                          ORDER BY completed_at DESC
                        ) AS rn
                      FROM company_run_results
                      WHERE status = 'success'
                        AND completed_at IS NOT NULL
                    ) ranked
                    WHERE rn <= :limit
                    ORDER BY company_id, completed_at DESC
                    """
                ),
                {"limit": _MAX_SUCCESS_SAMPLES},
            )
        ).all()
        for poll in poll_rows:
            if poll.company_id not in company_id_set:
                continue
            success_by_company[poll.company_id].append(poll.completed_at)

    companies = [
        build_company_cadence(
            company_id=row.id,
            name=row.name,
            platform=row.platform,
            fetch_tier=row.fetch_tier,
            is_active=row.is_active,
            consecutive_fetch_failures=row.consecutive_fetch_failures,
            last_successful_fetch_at=row.last_successful_fetch_at,
            success_timestamps=success_by_company.get(row.id, []),
            schedule=schedule,
            now=now,
        )
        for row in company_rows
    ]

    platforms = sorted({c.platform for c in companies})
    schedule_intervals = {
        platform: {
            str(tier): schedule.interval_minutes(platform, tier) / 60.0 for tier in (1, 2, 3)
        }
        for platform in platforms
    }

    return {
        "generated_at": now.isoformat(),
        "tick_minutes": schedule.tick_minutes,
        "batch_cap": schedule.batch_cap,
        "schedule_intervals_hours": schedule_intervals,
        "summary": _summary(companies),
        "companies": [_serialize_company(c) for c in companies],
    }
