from __future__ import annotations

import asyncio

import pytest

from app.ingestion.rate_limiter import HostTokenBucket, parse_retry_after, reset_ashby_bucket_for_tests


@pytest.fixture(autouse=True)
def _reset_bucket() -> None:
    reset_ashby_bucket_for_tests()
    yield
    reset_ashby_bucket_for_tests()


def test_parse_retry_after_parses_integer_seconds() -> None:
    assert parse_retry_after("5") == 5.0
    assert parse_retry_after(" 2.5 ") == 2.5


def test_parse_retry_after_returns_none_for_invalid_values() -> None:
    assert parse_retry_after(None) is None
    assert parse_retry_after("") is None
    assert parse_retry_after("not-a-number") is None
    assert parse_retry_after("-1") is None


@pytest.mark.asyncio
async def test_host_token_bucket_enforces_spacing_after_burst(monkeypatch) -> None:
    monotonic_values = [0.0, 0.0, 0.0, 0.0, 1.0]
    index = {"i": 0}

    def _monotonic() -> float:
        value = monotonic_values[min(index["i"], len(monotonic_values) - 1)]
        index["i"] += 1
        return value

    sleeps: list[float] = []

    async def _record_sleep(seconds: float) -> None:
        sleeps.append(seconds)

    monkeypatch.setattr("app.ingestion.rate_limiter.time.monotonic", _monotonic)
    monkeypatch.setattr("app.ingestion.rate_limiter.asyncio.sleep", _record_sleep)

    bucket = HostTokenBucket(rate_per_second=1.0, burst=2)
    await bucket.acquire()
    await bucket.acquire()
    await bucket.acquire()

    assert len(sleeps) == 1
    assert sleeps[0] == pytest.approx(1.0)


@pytest.mark.asyncio
async def test_host_token_bucket_allows_burst_without_sleep(monkeypatch) -> None:
    monkeypatch.setattr("app.ingestion.rate_limiter.time.monotonic", lambda: 0.0)
    sleeps: list[float] = []

    async def _record_sleep(seconds: float) -> None:
        sleeps.append(seconds)

    monkeypatch.setattr("app.ingestion.rate_limiter.asyncio.sleep", _record_sleep)

    bucket = HostTokenBucket(rate_per_second=1.0, burst=3)
    await bucket.acquire()
    await bucket.acquire()
    await bucket.acquire()

    assert sleeps == []
