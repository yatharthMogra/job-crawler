from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.ingestion.alerts import write_push_staleness_alert
from app.models.company import Company

DEFAULT_ALERT_AFTER_MISSED_INTERVALS = 2


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _is_manual_push_company(company: Company) -> bool:
    config = company.platform_config if isinstance(company.platform_config, dict) else {}
    return config.get("ingestion_mode") == "manual_push"


def _expected_push_interval_hours(company: Company) -> int:
    config = company.platform_config if isinstance(company.platform_config, dict) else {}
    raw = config.get("expected_push_interval_hours", 4)
    try:
        return max(1, int(raw))
    except (TypeError, ValueError):
        return 4


async def check_push_staleness(db: AsyncSession, settings: Settings) -> list[dict]:
    companies = (
        await db.scalars(select(Company).where(Company.is_active.is_(True)).order_by(Company.name.asc()))
    ).all()
    alerts: list[dict] = []
    now = _utcnow()

    for company in companies:
        if not _is_manual_push_company(company):
            continue
        last_push = company.last_successful_fetch_at
        if last_push is None:
            continue

        interval_hours = _expected_push_interval_hours(company)
        threshold = timedelta(hours=interval_hours * DEFAULT_ALERT_AFTER_MISSED_INTERVALS)
        age = now - last_push
        if age <= threshold:
            continue

        hours_since = age.total_seconds() / 3600
        record = write_push_staleness_alert(
            alerts_path=settings.alerts_path,
            company=company,
            hours_since_last_push=hours_since,
            expected_interval_hours=interval_hours,
        )
        alerts.append(record)
    return alerts
