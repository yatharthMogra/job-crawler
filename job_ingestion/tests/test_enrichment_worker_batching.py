from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from app.config import Settings
from app.ingestion.enrichment_worker import (
    _allocate_tokens,
    _batch_is_ready,
    _is_daily_quota_exhausted,
    _is_provider_capacity_error,
    _is_retryable_error,
    _is_transient_rate_limit,
    _pack_batches,
    _partition_ready_batches,
)

GEMINI_RESOURCE_EXHAUSTED = (
    "Gemini completion failed: 429 RESOURCE_EXHAUSTED. "
    "{'error': {'code': 429, 'message': 'Resource has been exhausted (e.g. check quota).', "
    "'status': 'RESOURCE_EXHAUSTED'}}"
)
GEMINI_DAILY_QUOTA = (
    "Gemini completion failed: 429 RESOURCE_EXHAUSTED. "
    "{'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan.', "
    "'status': 'RESOURCE_EXHAUSTED'}}"
)


def _item(tokens: int):
    return SimpleNamespace(estimated_tokens=tokens)


def test_is_daily_quota_exhausted() -> None:
    assert _is_daily_quota_exhausted(
        "429 Quota exceeded for metric generativelanguage.googleapis.com/generate_requests_per_day"
    )
    assert _is_daily_quota_exhausted(GEMINI_DAILY_QUOTA)
    assert not _is_daily_quota_exhausted("429 Too Many Requests")
    assert not _is_daily_quota_exhausted(GEMINI_RESOURCE_EXHAUSTED)


def test_is_transient_rate_limit() -> None:
    assert _is_transient_rate_limit("429 Too Many Requests")
    assert _is_transient_rate_limit("503 UNAVAILABLE")
    assert _is_transient_rate_limit(GEMINI_RESOURCE_EXHAUSTED)
    assert not _is_transient_rate_limit("429 Quota exceeded for metric generate_requests_per_day")
    assert not _is_transient_rate_limit(GEMINI_DAILY_QUOTA)


def test_is_provider_capacity_error() -> None:
    assert _is_provider_capacity_error(GEMINI_RESOURCE_EXHAUSTED)
    assert _is_provider_capacity_error(GEMINI_DAILY_QUOTA)
    assert not _is_provider_capacity_error("validation error for JobEnrichment")


def test_is_retryable_error_matches_transient_failures_only() -> None:
    assert _is_retryable_error("429 Too Many Requests")
    assert _is_retryable_error("503 UNAVAILABLE")
    assert _is_retryable_error(GEMINI_RESOURCE_EXHAUSTED)
    assert not _is_retryable_error("429 Quota exceeded for metric generate_requests_per_day")
    assert not _is_retryable_error(GEMINI_DAILY_QUOTA)
    assert not _is_retryable_error("schema mismatch")


def test_allocate_tokens_distributes_total() -> None:
    result = _allocate_tokens(total_tokens=100, estimates=[50, 25, 25])
    assert sum(result) == 100
    assert result[0] >= result[1]


def test_pack_batches_applies_batch_and_budget_limits() -> None:
    settings = Settings(
        enrichment_micro_batch_size=2,
        enrichment_max_input_tokens_per_batch=70,
        enrichment_window_token_budget=100,
    )
    batches, deferred = _pack_batches(
        settings=settings,
        items=[_item(50), _item(30), _item(20), _item(10)],
    )

    assert len(batches) >= 1
    assert all(len(batch) <= 2 for batch in batches)
    assert all(sum(item.estimated_tokens for item in batch) <= 70 for batch in batches)
    packed_total = sum(item.estimated_tokens for batch in batches for item in batch)
    assert packed_total <= 100
    assert packed_total + sum(item.estimated_tokens for item in deferred) == 110


def test_batch_interval_respects_rpm_cap() -> None:
    settings = Settings(
        enrichment_window_seconds=60,
        enrichment_max_batches_per_window=12,
        enrichment_llm_max_rpm=12,
    )
    assert settings.enrichment_batch_interval_seconds == 5.0


def _work_item(*, minutes_ago: float, attempt_count: int = 0):
    now = datetime.now(timezone.utc)
    ts = now - timedelta(minutes=minutes_ago)
    return SimpleNamespace(
        estimated_tokens=100,
        queue_row=SimpleNamespace(
            created_at=ts,
            updated_at=ts,
            attempt_count=attempt_count,
        ),
    )


def test_batch_is_ready_when_min_size_met() -> None:
    settings = Settings(enrichment_min_batch_enabled=True, enrichment_min_batch_size=6)
    now = datetime.now(timezone.utc)
    batch = [_work_item(minutes_ago=5) for _ in range(6)]
    assert _batch_is_ready(batch, settings, now)


def test_batch_is_not_ready_when_undersized_and_fresh() -> None:
    settings = Settings(
        enrichment_min_batch_enabled=True,
        enrichment_min_batch_size=6,
        enrichment_min_batch_bypass_wait_seconds=1800,
    )
    now = datetime.now(timezone.utc)
    batch = [_work_item(minutes_ago=5) for _ in range(4)]
    assert not _batch_is_ready(batch, settings, now)


def test_batch_is_ready_when_undersized_but_stale() -> None:
    settings = Settings(
        enrichment_min_batch_enabled=True,
        enrichment_min_batch_size=6,
        enrichment_min_batch_bypass_wait_seconds=1800,
    )
    now = datetime.now(timezone.utc)
    batch = [_work_item(minutes_ago=5) for _ in range(3)] + [_work_item(minutes_ago=31)]
    assert _batch_is_ready(batch, settings, now)


def test_batch_is_ready_when_min_batch_disabled() -> None:
    settings = Settings(enrichment_min_batch_enabled=False, enrichment_min_batch_size=6)
    now = datetime.now(timezone.utc)
    batch = [_work_item(minutes_ago=1)]
    assert _batch_is_ready(batch, settings, now)


def test_partition_ready_batches_splits_held_and_ready() -> None:
    settings = Settings(
        enrichment_min_batch_enabled=True,
        enrichment_min_batch_size=6,
        enrichment_min_batch_bypass_wait_seconds=1800,
    )
    now = datetime.now(timezone.utc)
    fresh_small = [_work_item(minutes_ago=5) for _ in range(3)]
    ready_large = [_work_item(minutes_ago=5) for _ in range(6)]
    ready, held = _partition_ready_batches([fresh_small, ready_large], settings, now)
    assert len(ready) == 1
    assert len(ready[0]) == 6
    assert len(held) == 3
