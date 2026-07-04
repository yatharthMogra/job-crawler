from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Literal
from zoneinfo import ZoneInfo

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.models.enrichment_worker_state import EnrichmentWorkerState

CapacityMode = Literal["normal", "backoff", "probe", "daily_exhausted"]


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _parse_reset_time(reset_time: str) -> tuple[int, int]:
    parts = reset_time.strip().split(":")
    if len(parts) != 2:
        raise ValueError(f"Invalid reset time {reset_time!r}; expected HH:MM")
    hour, minute = int(parts[0]), int(parts[1])
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(f"Invalid reset time {reset_time!r}")
    return hour, minute


def current_window_start(
    now: datetime,
    *,
    reset_time: str,
    timezone_name: str,
) -> datetime:
    tz = ZoneInfo(timezone_name)
    hour, minute = _parse_reset_time(reset_time)
    local_now = now.astimezone(tz)
    boundary = local_now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if local_now < boundary:
        boundary -= timedelta(days=1)
    return boundary.astimezone(timezone.utc)


def next_window_start(
    now: datetime,
    *,
    reset_time: str,
    timezone_name: str,
) -> datetime:
    current = current_window_start(now, reset_time=reset_time, timezone_name=timezone_name)
    tz = ZoneInfo(timezone_name)
    hour, minute = _parse_reset_time(reset_time)
    local_current = current.astimezone(tz)
    next_boundary = (local_current + timedelta(days=1)).replace(
        hour=hour, minute=minute, second=0, microsecond=0
    )
    return next_boundary.astimezone(timezone.utc)


def compute_backoff_seconds(attempt: int, settings: Settings) -> float:
    return settings.enrichment_worker_backoff_seconds(attempt)


class WorkerCapacityTracker:
    def __init__(self, worker_id: int, settings: Settings) -> None:
        self._worker_id = worker_id
        self._settings = settings
        self._committed_calls = 0
        self._pending_calls = 0
        self._mode: CapacityMode = "normal"
        self._backoff_attempt = 0
        self._rate_limited_until: datetime | None = None
        self._window_start: datetime | None = None
        self._row: EnrichmentWorkerState | None = None
        self._window_error_fired = False

    @property
    def mode(self) -> CapacityMode:
        return self._mode

    @property
    def worker_id(self) -> int:
        return self._worker_id

    def total_calls(self) -> int:
        return self._committed_calls + self._pending_calls

    def window_error_fired(self) -> bool:
        return self._window_error_fired

    def clear_window_error_flag(self) -> None:
        self._window_error_fired = False

    async def load_or_create(self, db: AsyncSession) -> None:
        now = _utcnow()
        settings = self._settings
        window_start = current_window_start(
            now,
            reset_time=settings.enrichment_worker_daily_reset_time,
            timezone_name=settings.enrichment_worker_daily_reset_timezone,
        )
        row = await db.get(EnrichmentWorkerState, self._worker_id)
        if row is None:
            row = EnrichmentWorkerState(
                worker_id=self._worker_id,
                window_start=window_start,
                api_calls=0,
                capacity_mode="normal",
                rate_limit_backoff_attempt=0,
                rate_limited_until=None,
            )
            db.add(row)
            await db.flush()
        elif row.window_start < window_start:
            row.window_start = window_start
            row.api_calls = 0
            row.capacity_mode = "normal"
            row.rate_limit_backoff_attempt = 0
            row.rate_limited_until = None
            row.updated_at = now
            await db.flush()

        self._apply_row(row)

    def _apply_row(self, row: EnrichmentWorkerState) -> None:
        self._row = row
        self._committed_calls = row.api_calls
        self._pending_calls = 0
        self._mode = row.capacity_mode  # type: ignore[assignment]
        self._backoff_attempt = row.rate_limit_backoff_attempt
        self._rate_limited_until = row.rate_limited_until
        self._window_start = row.window_start

    def tick(self, now: datetime | None = None) -> None:
        now = now or _utcnow()
        settings = self._settings
        window_start = current_window_start(
            now,
            reset_time=settings.enrichment_worker_daily_reset_time,
            timezone_name=settings.enrichment_worker_daily_reset_timezone,
        )
        if self._window_start is not None and self._window_start < window_start:
            self._reset_for_new_window(window_start)

        if self._mode == "backoff" and self._rate_limited_until is not None and now >= self._rate_limited_until:
            self._mode = "probe"
            if self._row is not None:
                self._row.capacity_mode = "probe"

        if self._mode == "daily_exhausted":
            if self._window_start is not None and self._window_start < window_start:
                self._reset_for_new_window(window_start)

    def _reset_for_new_window(self, window_start: datetime) -> None:
        self._committed_calls = 0
        self._pending_calls = 0
        self._mode = "normal"
        self._backoff_attempt = 0
        self._rate_limited_until = None
        self._window_start = window_start
        if self._row is not None:
            self._row.window_start = window_start
            self._row.api_calls = 0
            self._row.capacity_mode = "normal"
            self._row.rate_limit_backoff_attempt = 0
            self._row.rate_limited_until = None

    def can_process(self, now: datetime | None = None) -> bool:
        now = now or _utcnow()
        if self._mode == "daily_exhausted":
            return False
        if self._mode == "backoff":
            if self._rate_limited_until is not None and now < self._rate_limited_until:
                return False
        return self.total_calls() < self._settings.enrichment_worker_daily_api_call_limit

    def sleep_seconds(self, now: datetime | None = None) -> float:
        now = now or _utcnow()
        if self._mode == "backoff" and self._rate_limited_until is not None:
            remaining = (self._rate_limited_until - now).total_seconds()
            return max(1.0, min(remaining, 30.0))
        return 30.0

    def effective_max_batches(self, now: datetime | None = None) -> int:
        if not self.can_process(now):
            return 0
        if self._mode == "probe":
            return 1
        settings = self._settings
        rpm_cap = max(settings.enrichment_llm_max_rpm, 1)
        return min(settings.enrichment_max_batches_per_window, rpm_cap)

    async def record_api_call(self, db: AsyncSession) -> None:
        self._pending_calls += 1
        if self._pending_calls >= self._settings.enrichment_worker_daily_flush_interval:
            await self.flush_pending(db)
        if self.total_calls() >= self._settings.enrichment_worker_daily_api_call_limit:
            await self.enter_daily_exhausted(db)

    async def enter_backoff(self, db: AsyncSession) -> None:
        now = _utcnow()
        delay = compute_backoff_seconds(self._backoff_attempt, self._settings)
        self._backoff_attempt += 1
        self._rate_limited_until = now + timedelta(seconds=delay)
        self._mode = "backoff"
        await self._persist(db)

    async def enter_normal(self, db: AsyncSession) -> None:
        self._mode = "normal"
        self._backoff_attempt = 0
        self._rate_limited_until = None
        await self._persist(db)

    async def enter_daily_exhausted(self, db: AsyncSession) -> None:
        await self.flush_pending(db)
        self._mode = "daily_exhausted"
        self._rate_limited_until = None
        await self._persist(db)

    async def flush_pending(self, db: AsyncSession) -> None:
        if self._pending_calls <= 0 or self._row is None:
            return
        self._committed_calls += self._pending_calls
        self._row.api_calls = self._committed_calls
        self._row.updated_at = _utcnow()
        self._pending_calls = 0
        await db.flush()

    def mark_window_error(self) -> None:
        self._window_error_fired = True

    async def dispatch_before_api_call(self, db: AsyncSession) -> None:
        await self.record_api_call(db)

    async def dispatch_transient_rate_limit(self, db: AsyncSession) -> None:
        self.mark_window_error()
        await self.enter_backoff(db)

    async def dispatch_daily_quota(self, db: AsyncSession) -> None:
        self.mark_window_error()
        await self.enter_daily_exhausted(db)

    async def dispatch_api_success(self, db: AsyncSession) -> None:
        if self._mode == "probe":
            await self.enter_normal(db)

    async def _persist(self, db: AsyncSession) -> None:
        if self._row is None:
            return
        self._row.capacity_mode = self._mode
        self._row.rate_limit_backoff_attempt = self._backoff_attempt
        self._row.rate_limited_until = self._rate_limited_until
        self._row.updated_at = _utcnow()
        await db.flush()

    def snapshot(self) -> dict[str, object]:
        return {
            "worker_id": self._worker_id,
            "capacity_mode": self._mode,
            "api_calls": self.total_calls(),
            "committed_calls": self._committed_calls,
            "pending_calls": self._pending_calls,
            "rate_limit_backoff_attempt": self._backoff_attempt,
            "rate_limited_until": (
                self._rate_limited_until.isoformat() if self._rate_limited_until else None
            ),
            "window_start": self._window_start.isoformat() if self._window_start else None,
        }
