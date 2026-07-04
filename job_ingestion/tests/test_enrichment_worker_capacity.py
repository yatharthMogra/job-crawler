from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock
from zoneinfo import ZoneInfo

import pytest

from app.config import Settings
from app.ingestion.enrichment_worker_capacity import (
    WorkerCapacityTracker,
    compute_backoff_seconds,
    current_window_start,
    next_window_start,
)
from app.models.enrichment_worker_state import EnrichmentWorkerState


def _dt(year: int, month: int, day: int, hour: int, minute: int = 0, tz: str = "UTC") -> datetime:
    return datetime(year, month, day, hour, minute, tzinfo=ZoneInfo(tz))


def test_current_window_start_midnight_pacific() -> None:
    settings_reset_time = "00:00"
    tz = "America/Los_Angeles"
    # 2026-07-03 10:00 UTC = 2026-07-03 03:00 PDT — same RPD window as midnight PT Jul 3
    now = _dt(2026, 7, 3, 10, 0, "UTC")
    start = current_window_start(now, reset_time=settings_reset_time, timezone_name=tz)
    expected = _dt(2026, 7, 3, 0, 0, "America/Los_Angeles").astimezone(timezone.utc)
    assert start == expected


def test_current_window_start_before_boundary_uses_previous_day() -> None:
    tz = "America/Los_Angeles"
    # 2026-07-03 06:00 UTC = 2026-07-02 23:00 PDT — still prior window
    now = _dt(2026, 7, 3, 6, 0, "UTC")
    start = current_window_start(now, reset_time="00:00", timezone_name=tz)
    expected = _dt(2026, 7, 2, 0, 0, "America/Los_Angeles").astimezone(timezone.utc)
    assert start == expected


def test_next_window_start_is_one_day_after_current() -> None:
    tz = "America/Los_Angeles"
    now = _dt(2026, 7, 3, 10, 0, "UTC")
    current = current_window_start(now, reset_time="00:00", timezone_name=tz)
    nxt = next_window_start(now, reset_time="00:00", timezone_name=tz)
    assert nxt == current + timedelta(days=1)


def test_compute_backoff_seconds_exponential_with_cap() -> None:
    settings = Settings(
        enrichment_worker_rate_limit_initial_backoff_seconds=60,
        enrichment_worker_rate_limit_backoff_multiplier=2,
        enrichment_worker_rate_limit_max_backoff_seconds=600,
    )
    assert compute_backoff_seconds(0, settings) == 60.0
    assert compute_backoff_seconds(1, settings) == 120.0
    assert compute_backoff_seconds(2, settings) == 240.0
    assert compute_backoff_seconds(10, settings) == 600.0


def test_enrichment_worker_backoff_seconds_property() -> None:
    settings = Settings(
        enrichment_worker_rate_limit_initial_backoff_seconds=60,
        enrichment_worker_rate_limit_backoff_multiplier=2,
        enrichment_worker_rate_limit_max_backoff_seconds=600,
    )
    assert settings.enrichment_worker_backoff_seconds(0) == 60.0
    assert settings.enrichment_worker_backoff_seconds(1) == 120.0


def test_effective_max_batches_probe_mode() -> None:
    settings = Settings(
        gemini_api_keys="k1",
        enrichment_llm_max_rpm=12,
        enrichment_max_batches_per_window=12,
    )
    tracker = WorkerCapacityTracker(worker_id=0, settings=settings)
    tracker._mode = "probe"
    assert tracker.effective_max_batches() == 1


def test_effective_max_batches_daily_exhausted() -> None:
    settings = Settings(gemini_api_keys="k1")
    tracker = WorkerCapacityTracker(worker_id=0, settings=settings)
    tracker._mode = "daily_exhausted"
    assert tracker.effective_max_batches() == 0


def test_can_process_false_during_backoff() -> None:
    settings = Settings(gemini_api_keys="k1")
    tracker = WorkerCapacityTracker(worker_id=0, settings=settings)
    now = datetime.now(timezone.utc)
    tracker._mode = "backoff"
    tracker._rate_limited_until = now + timedelta(seconds=30)
    assert tracker.can_process(now) is False


def test_tick_transitions_backoff_to_probe() -> None:
    settings = Settings(gemini_api_keys="k1")
    tracker = WorkerCapacityTracker(worker_id=0, settings=settings)
    now = datetime.now(timezone.utc)
    tracker._mode = "backoff"
    tracker._rate_limited_until = now - timedelta(seconds=1)
    tracker.tick(now)
    assert tracker.mode == "probe"


@pytest.mark.asyncio
async def test_record_api_call_flushes_at_interval() -> None:
    settings = Settings(
        gemini_api_keys="k1",
        enrichment_worker_daily_api_call_limit=500,
        enrichment_worker_daily_flush_interval=50,
    )
    tracker = WorkerCapacityTracker(worker_id=0, settings=settings)
    row = EnrichmentWorkerState(
        worker_id=0,
        window_start=datetime.now(timezone.utc),
        api_calls=0,
        capacity_mode="normal",
        rate_limit_backoff_attempt=0,
    )
    tracker._apply_row(row)
    db = AsyncMock()
    db.flush = AsyncMock()

    for _ in range(50):
        await tracker.record_api_call(db)

    assert tracker._pending_calls == 0
    assert tracker._committed_calls == 50
    assert row.api_calls == 50
    assert db.flush.await_count >= 1


@pytest.mark.asyncio
async def test_record_api_call_enters_daily_exhausted_at_limit() -> None:
    settings = Settings(
        gemini_api_keys="k1",
        enrichment_worker_daily_api_call_limit=5,
        enrichment_worker_daily_flush_interval=50,
    )
    tracker = WorkerCapacityTracker(worker_id=0, settings=settings)
    row = EnrichmentWorkerState(
        worker_id=0,
        window_start=datetime.now(timezone.utc),
        api_calls=0,
        capacity_mode="normal",
        rate_limit_backoff_attempt=0,
    )
    tracker._apply_row(row)
    db = AsyncMock()
    db.flush = AsyncMock()

    for _ in range(5):
        await tracker.record_api_call(db)

    assert tracker.mode == "daily_exhausted"
    assert tracker.can_process() is False


@pytest.mark.asyncio
async def test_enter_backoff_sets_until_and_mode() -> None:
    settings = Settings(
        gemini_api_keys="k1",
        enrichment_worker_rate_limit_initial_backoff_seconds=60,
        enrichment_worker_rate_limit_backoff_multiplier=2,
        enrichment_worker_rate_limit_max_backoff_seconds=600,
    )
    tracker = WorkerCapacityTracker(worker_id=0, settings=settings)
    row = EnrichmentWorkerState(
        worker_id=0,
        window_start=datetime.now(timezone.utc),
        api_calls=0,
        capacity_mode="normal",
        rate_limit_backoff_attempt=0,
    )
    tracker._apply_row(row)
    db = AsyncMock()
    db.flush = AsyncMock()

    before = datetime.now(timezone.utc)
    await tracker.enter_backoff(db)
    after = datetime.now(timezone.utc)

    assert tracker.mode == "backoff"
    assert tracker._rate_limited_until is not None
    assert tracker._backoff_attempt == 1
    assert before + timedelta(seconds=59) <= tracker._rate_limited_until <= after + timedelta(seconds=61)


@pytest.mark.asyncio
async def test_dispatch_api_success_from_probe_enters_normal() -> None:
    settings = Settings(gemini_api_keys="k1")
    tracker = WorkerCapacityTracker(worker_id=0, settings=settings)
    row = EnrichmentWorkerState(
        worker_id=0,
        window_start=datetime.now(timezone.utc),
        api_calls=0,
        capacity_mode="probe",
        rate_limit_backoff_attempt=2,
    )
    tracker._apply_row(row)
    tracker._mode = "probe"
    tracker._backoff_attempt = 2
    db = AsyncMock()
    db.flush = AsyncMock()

    await tracker.dispatch_api_success(db)

    assert tracker.mode == "normal"
    assert tracker._backoff_attempt == 0


@pytest.mark.asyncio
async def test_load_or_create_resets_stale_window() -> None:
    settings = Settings(
        gemini_api_keys="k1",
        enrichment_worker_daily_reset_time="00:00",
        enrichment_worker_daily_reset_timezone="America/Los_Angeles",
    )
    now = _dt(2026, 7, 3, 10, 0, "UTC")
    current_start = current_window_start(
        now,
        reset_time=settings.enrichment_worker_daily_reset_time,
        timezone_name=settings.enrichment_worker_daily_reset_timezone,
    )
    stale_start = current_start - timedelta(days=1)
    row = EnrichmentWorkerState(
        worker_id=0,
        window_start=stale_start,
        api_calls=400,
        capacity_mode="daily_exhausted",
        rate_limit_backoff_attempt=3,
    )
    db = MagicMock()
    db.get = AsyncMock(return_value=row)
    db.flush = AsyncMock()
    db.add = MagicMock()

    tracker = WorkerCapacityTracker(worker_id=0, settings=settings)
    await tracker.load_or_create(db)

    assert row.api_calls == 0
    assert row.capacity_mode == "normal"
    assert tracker.mode == "normal"
    assert tracker.total_calls() == 0
