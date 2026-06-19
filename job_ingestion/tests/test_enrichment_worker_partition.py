from __future__ import annotations

import pytest

from app.config import Settings
from app.ingestion.enrichment_worker import EnrichmentWorkerPool, _partition_filter


def test_gemini_api_keys_list_from_comma_separated() -> None:
    settings = Settings(gemini_api_keys="key1,key2, key3")
    assert settings.gemini_api_keys_list() == ["key1", "key2", "key3"]


def test_gemini_api_keys_list_falls_back_to_single_key() -> None:
    settings = Settings(gemini_api_keys="", gemini_api_key="solo-key")
    assert settings.gemini_api_keys_list() == ["solo-key"]


def test_gemini_api_keys_list_prefers_comma_list() -> None:
    settings = Settings(gemini_api_keys="a,b", gemini_api_key="solo")
    assert settings.gemini_api_keys_list() == ["a", "b"]


def test_resolved_enrichment_worker_count_defaults_to_key_count() -> None:
    settings = Settings(gemini_api_keys="k1,k2,k3")
    assert settings.resolved_enrichment_worker_count() == 3


def test_resolved_enrichment_worker_count_honors_cap() -> None:
    settings = Settings(gemini_api_keys="k1,k2,k3", enrichment_worker_count=2)
    assert settings.resolved_enrichment_worker_count() == 2


def test_resolved_enrichment_worker_count_rejects_excess_cap() -> None:
    settings = Settings(gemini_api_keys="k1", enrichment_worker_count=3)
    with pytest.raises(ValueError, match="exceeds configured Gemini keys"):
        settings.resolved_enrichment_worker_count()


def test_enrichment_worker_pool_builds_n_workers() -> None:
    settings = Settings(gemini_api_keys="k1,k2,k3")
    pool = EnrichmentWorkerPool(settings=settings)
    assert pool.worker_count == 3
    assert len(pool.workers) == 3
    assert pool.workers[0]._worker_id == 0
    assert pool.workers[2]._worker_count == 3
    assert pool.workers[0]._settings.gemini_api_key == "k1"
    assert pool.workers[0]._settings.enrichment_stop_on_daily_quota is False


def test_partition_filter_compiles() -> None:
    clause = _partition_filter(worker_id=2, worker_count=7)
    compiled = str(clause.compile(compile_kwargs={"literal_binds": True}))
    assert "hashtext" in compiled
    assert "7" in compiled
    assert "2" in compiled
