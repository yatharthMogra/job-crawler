from __future__ import annotations

from types import SimpleNamespace

from app.config import Settings
from app.ingestion.enrichment_worker import _allocate_tokens, _is_retryable_error, _pack_batches


def _item(tokens: int):
    return SimpleNamespace(estimated_tokens=tokens)


def test_is_retryable_error_matches_rate_and_quota_failures() -> None:
    assert _is_retryable_error("429 RESOURCE_EXHAUSTED")
    assert _is_retryable_error("503 UNAVAILABLE")
    assert _is_retryable_error("quota exceeded")
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
