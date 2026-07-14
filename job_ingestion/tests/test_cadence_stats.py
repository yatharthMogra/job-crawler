from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.ingestion.cadence_stats import build_company_cadence, compute_health
from app.ingestion.fetch_schedule_config import parse_fetch_schedule_json


def test_compute_health_thresholds() -> None:
    assert compute_health(actual_cadence_hours=None, target_cadence_hours=6) == "never_fetched"
    assert compute_health(actual_cadence_hours=6.0, target_cadence_hours=6) == "on_target"
    assert compute_health(actual_cadence_hours=6.5, target_cadence_hours=6) == "on_target"
    assert compute_health(actual_cadence_hours=7.5, target_cadence_hours=6) == "drifting"
    assert compute_health(actual_cadence_hours=10.0, target_cadence_hours=6) == "behind"


def test_build_company_cadence_uses_observed_interval() -> None:
    now = datetime(2026, 7, 14, 12, 0, tzinfo=timezone.utc)
    schedule = parse_fetch_schedule_json("")
    # greenhouse tier 2 default = 180 minutes = 3h
    stamps = [
        now - timedelta(hours=9),
        now - timedelta(hours=6),
        now - timedelta(hours=3),
    ]
    row = build_company_cadence(
        company_id=uuid4(),
        name="Acme",
        platform="greenhouse",
        fetch_tier=2,
        is_active=True,
        consecutive_fetch_failures=0,
        last_successful_fetch_at=stamps[-1],
        success_timestamps=stamps,
        schedule=schedule,
        now=now,
    )
    assert row.target_cadence_hours == 3.0
    assert row.observed_interval_hours == 3.0
    assert row.actual_cadence_hours == 3.0
    assert row.health == "on_target"
    assert row.drift_ratio == 1.0


def test_build_company_cadence_falls_back_to_staleness() -> None:
    now = datetime(2026, 7, 14, 12, 0, tzinfo=timezone.utc)
    schedule = parse_fetch_schedule_json("")
    last = now - timedelta(hours=12)
    row = build_company_cadence(
        company_id=uuid4(),
        name="Beta",
        platform="greenhouse",
        fetch_tier=2,
        is_active=True,
        consecutive_fetch_failures=2,
        last_successful_fetch_at=last,
        success_timestamps=[last],
        schedule=schedule,
        now=now,
    )
    assert row.observed_interval_hours is None
    assert row.actual_cadence_hours == 12.0
    assert row.health == "behind"
    assert row.consecutive_failures == 2


def test_build_company_cadence_never_fetched() -> None:
    schedule = parse_fetch_schedule_json("")
    row = build_company_cadence(
        company_id=uuid4(),
        name="Gamma",
        platform="ashby",
        fetch_tier=1,
        is_active=True,
        consecutive_fetch_failures=5,
        last_successful_fetch_at=None,
        success_timestamps=[],
        schedule=schedule,
    )
    assert row.actual_cadence_hours is None
    assert row.health == "never_fetched"
    assert row.target_cadence_hours == 2.0  # ashby tier 1 = 120m
