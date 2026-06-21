from __future__ import annotations

import asyncio
import time
from typing import Optional

from app.config import Settings, get_settings

_ashby_bucket: Optional["HostTokenBucket"] = None


def parse_retry_after(header_value: str | None) -> float | None:
    if not header_value:
        return None
    try:
        seconds = float(header_value.strip())
    except ValueError:
        return None
    if seconds < 0:
        return None
    return seconds


class HostTokenBucket:
    """Shared across all coroutines touching one host, regardless of company or tick."""

    def __init__(self, rate_per_second: float, burst: int) -> None:
        self.rate = max(rate_per_second, 0.01)
        self.burst = max(burst, 1)
        self.tokens = float(self.burst)
        self.updated_at = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:
            while True:
                now = time.monotonic()
                elapsed = now - self.updated_at
                self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
                self.updated_at = now
                if self.tokens >= 1:
                    self.tokens -= 1
                    return
                wait = (1 - self.tokens) / self.rate
                await asyncio.sleep(wait)


def get_ashby_bucket(settings: Settings | None = None) -> HostTokenBucket:
    global _ashby_bucket
    if _ashby_bucket is None:
        settings = settings or get_settings()
        _ashby_bucket = HostTokenBucket(
            rate_per_second=settings.ashby_host_rate_per_second,
            burst=settings.ashby_host_burst,
        )
    return _ashby_bucket


def reset_ashby_bucket_for_tests() -> None:
    global _ashby_bucket
    _ashby_bucket = None
