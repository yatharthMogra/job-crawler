from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.config import Settings
from app.ingestion import pipeline
from app.ingestion.change_detector import ClassifiedJobs, classify_jobs
from app.ingestion.job_identity_ledger import load_ledger_hashes, touch_ledger_seen, upsert_ledger_entry
from app.models.company import Company
from app.utils.hashing import compute_content_hash


def test_classify_uses_ledger_hashes_after_purge() -> None:
    job = {"id": "42", "title": "Software Engineer"}
    ledger_hashes = {"42": compute_content_hash(job)}

    result = classify_jobs(
        fetched_jobs=[job],
        previous_hashes=ledger_hashes,
        previously_active_job_ids=set(),
    )

    assert len(result.new) == 0
    assert len(result.updated) == 0
    assert len(result.unchanged) == 1


@pytest.mark.asyncio
async def test_ledger_upsert_insert() -> None:
    company_id = uuid4()
    db = AsyncMock()
    db.scalar = AsyncMock(return_value=None)
    db.execute = AsyncMock()

    await upsert_ledger_entry(db, company_id, "ext-1", "hash-a")

    assert db.execute.await_count == 1


@pytest.mark.asyncio
async def test_ledger_upsert_updates_hash_and_last_changed_at() -> None:
    company_id = uuid4()
    db = AsyncMock()
    db.scalar = AsyncMock(return_value="hash-a")
    db.execute = AsyncMock()

    await upsert_ledger_entry(db, company_id, "ext-1", "hash-b")

    assert db.execute.await_count == 1


@pytest.mark.asyncio
async def test_load_ledger_hashes() -> None:
    db = AsyncMock()
    db.execute = AsyncMock(
        return_value=MagicMock(
            all=lambda: [("ext-1", "hash-a"), ("ext-2", "hash-b")]
        )
    )

    result = await load_ledger_hashes(db, uuid4())

    assert result == {"ext-1": "hash-a", "ext-2": "hash-b"}


@pytest.mark.asyncio
async def test_touch_ledger_seen_noop_on_empty() -> None:
    db = AsyncMock()
    await touch_ledger_seen(db, uuid4(), [])
    db.execute.assert_not_awaited()


def _company(**overrides) -> Company:
    defaults = {
        "id": uuid4(),
        "name": "Acme",
        "platform": "greenhouse",
        "board_token": "acme",
        "is_active": True,
        "consecutive_fetch_failures": 0,
    }
    defaults.update(overrides)
    return Company(**defaults)


@pytest.mark.asyncio
async def test_process_company_raw_jobs_unchanged_when_ledger_hash_matches(monkeypatch) -> None:
    company = _company()
    job = {"id": "job-1", "title": "Engineer", "content": "<p>Build things</p>"}
    content_hash = compute_content_hash(job)

    monkeypatch.setattr(pipeline, "load_ledger_hashes", AsyncMock(return_value={"job-1": content_hash}))
    monkeypatch.setattr(pipeline, "_latest_hashes_for_company", AsyncMock(return_value={}))
    monkeypatch.setattr(pipeline, "_normalized_map_for_company", AsyncMock(return_value={}))
    monkeypatch.setattr(pipeline, "fingerprint_exists", AsyncMock(return_value=False))
    monkeypatch.setattr(
        pipeline,
        "upsert_job_archive_from_deterministic",
        AsyncMock(return_value=uuid4()),
    )
    normalized = SimpleNamespace(id=uuid4(), job_archive_id=uuid4(), is_active=True)
    monkeypatch.setattr(
        pipeline,
        "_upsert_normalized_core",
        AsyncMock(return_value=normalized),
    )
    monkeypatch.setattr(pipeline, "queue_job_for_enrichment", AsyncMock())
    upsert_mock = AsyncMock()
    monkeypatch.setattr(pipeline, "upsert_ledger_entry", upsert_mock)

    db = MagicMock()
    db.flush = AsyncMock()
    outcome = await pipeline.process_company_raw_jobs(
        db,
        company,
        [job],
        pipeline_run_id=uuid4(),
        settings=Settings(),
    )

    assert outcome.jobs_new == 0
    assert outcome.jobs_unchanged == 1
    assert outcome.jobs_ledger_skipped == 0
    db.add.assert_called_once()
    assert upsert_mock.await_count >= 2


@pytest.mark.asyncio
async def test_process_company_raw_jobs_guard_skips_changed_job(monkeypatch) -> None:
    company = _company()
    job = {"id": "job-1", "title": "Engineer", "content": "<p>Build things</p>"}
    content_hash = compute_content_hash(job)
    classified = ClassifiedJobs()
    classified.new = [job]

    monkeypatch.setattr(pipeline, "load_ledger_hashes", AsyncMock(return_value={"job-1": content_hash}))
    monkeypatch.setattr(pipeline, "_latest_hashes_for_company", AsyncMock(return_value={"job-1": "stale-hash"}))
    monkeypatch.setattr(
        pipeline,
        "_normalized_map_for_company",
        AsyncMock(
            return_value={
                "job-1": SimpleNamespace(id=uuid4(), is_active=True, job_archive_id=uuid4())
            }
        ),
    )
    monkeypatch.setattr(pipeline, "classify_jobs", lambda *args, **kwargs: classified)
    monkeypatch.setattr(pipeline, "fingerprint_exists", AsyncMock(return_value=False))
    upsert_mock = AsyncMock()
    monkeypatch.setattr(pipeline, "upsert_ledger_entry", upsert_mock)

    db = MagicMock()
    outcome = await pipeline.process_company_raw_jobs(
        db,
        company,
        [job],
        pipeline_run_id=uuid4(),
        settings=Settings(),
    )

    assert outcome.jobs_new == 0
    assert outcome.jobs_ledger_skipped == 1
    db.add.assert_not_called()
    upsert_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_company_raw_jobs_reingests_on_hash_mismatch(monkeypatch) -> None:
    company = _company()
    job = {"id": "job-1", "title": "Senior Engineer", "content": "<p>Build things</p>"}
    old_job = {"id": "job-1", "title": "Engineer", "content": "<p>Build things</p>"}

    monkeypatch.setattr(
        pipeline,
        "load_ledger_hashes",
        AsyncMock(return_value={"job-1": compute_content_hash(old_job)}),
    )
    monkeypatch.setattr(pipeline, "_latest_hashes_for_company", AsyncMock(return_value={}))
    monkeypatch.setattr(pipeline, "_normalized_map_for_company", AsyncMock(return_value={}))
    monkeypatch.setattr(pipeline, "fingerprint_exists", AsyncMock(return_value=False))
    monkeypatch.setattr(
        pipeline,
        "upsert_job_archive_from_deterministic",
        AsyncMock(return_value=uuid4()),
    )
    monkeypatch.setattr(
        pipeline,
        "_upsert_normalized_core",
        AsyncMock(return_value=SimpleNamespace(id=uuid4())),
    )
    monkeypatch.setattr(pipeline, "queue_job_for_enrichment", AsyncMock())
    upsert_mock = AsyncMock()
    monkeypatch.setattr(pipeline, "upsert_ledger_entry", upsert_mock)

    db = MagicMock()
    db.flush = AsyncMock()

    outcome = await pipeline.process_company_raw_jobs(
        db,
        company,
        [job],
        pipeline_run_id=uuid4(),
        settings=Settings(),
    )

    assert outcome.jobs_updated == 1
    assert outcome.jobs_ledger_skipped == 0
    db.add.assert_called_once()
    upsert_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_company_raw_jobs_baseline_ledgers_unknown_posted_at(monkeypatch) -> None:
    company = _company()
    job = {"id": "job-new", "title": "Engineer", "content": "<p>New role</p>"}

    monkeypatch.setattr(pipeline, "load_ledger_hashes", AsyncMock(return_value={}))
    monkeypatch.setattr(pipeline, "_latest_hashes_for_company", AsyncMock(return_value={}))
    monkeypatch.setattr(pipeline, "_normalized_map_for_company", AsyncMock(return_value={}))
    monkeypatch.setattr(pipeline, "fingerprint_exists", AsyncMock(return_value=False))
    monkeypatch.setattr(
        pipeline,
        "upsert_job_archive_from_deterministic",
        AsyncMock(return_value=uuid4()),
    )
    monkeypatch.setattr(
        pipeline,
        "_upsert_normalized_core",
        AsyncMock(return_value=SimpleNamespace(id=uuid4())),
    )
    monkeypatch.setattr(pipeline, "queue_job_for_enrichment", AsyncMock())
    upsert_mock = AsyncMock()
    monkeypatch.setattr(pipeline, "upsert_ledger_entry", upsert_mock)

    db = MagicMock()
    db.flush = AsyncMock()

    outcome = await pipeline.process_company_raw_jobs(
        db,
        company,
        [job],
        pipeline_run_id=uuid4(),
        settings=Settings(),
    )

    assert outcome.jobs_new == 0
    assert outcome.jobs_ledger_baselined == 1
    assert outcome.jobs_ledger_skipped == 0
    db.add.assert_not_called()
    upsert_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_company_raw_jobs_baseline_ingests_fresh_jobs(monkeypatch) -> None:
    company = _company()
    reference = datetime.now(timezone.utc)
    job = {
        "id": "job-fresh",
        "title": "Engineer",
        "content": "<p>Fresh role</p>",
        "created_at": (reference - timedelta(days=2)).isoformat().replace("+00:00", "Z"),
    }

    monkeypatch.setattr(pipeline, "load_ledger_hashes", AsyncMock(return_value={}))
    monkeypatch.setattr(pipeline, "_latest_hashes_for_company", AsyncMock(return_value={}))
    monkeypatch.setattr(pipeline, "_normalized_map_for_company", AsyncMock(return_value={}))
    monkeypatch.setattr(pipeline, "fingerprint_exists", AsyncMock(return_value=False))
    monkeypatch.setattr(
        pipeline,
        "upsert_job_archive_from_deterministic",
        AsyncMock(return_value=uuid4()),
    )
    monkeypatch.setattr(
        pipeline,
        "_upsert_normalized_core",
        AsyncMock(return_value=SimpleNamespace(id=uuid4())),
    )
    monkeypatch.setattr(pipeline, "queue_job_for_enrichment", AsyncMock())
    upsert_mock = AsyncMock()
    monkeypatch.setattr(pipeline, "upsert_ledger_entry", upsert_mock)

    db = MagicMock()
    db.flush = AsyncMock()

    outcome = await pipeline.process_company_raw_jobs(
        db,
        company,
        [job],
        pipeline_run_id=uuid4(),
        settings=Settings(),
    )

    assert outcome.jobs_new == 1
    assert outcome.jobs_ledger_baselined == 0
    db.add.assert_called_once()
    upsert_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_company_raw_jobs_baseline_ledgers_stale_jobs(monkeypatch) -> None:
    company = _company()
    reference = datetime.now(timezone.utc)
    job = {
        "id": "job-stale",
        "title": "Engineer",
        "content": "<p>Old role</p>",
        "created_at": (reference - timedelta(days=30)).isoformat().replace("+00:00", "Z"),
    }

    monkeypatch.setattr(pipeline, "load_ledger_hashes", AsyncMock(return_value={}))
    monkeypatch.setattr(pipeline, "_latest_hashes_for_company", AsyncMock(return_value={}))
    monkeypatch.setattr(pipeline, "_normalized_map_for_company", AsyncMock(return_value={}))
    monkeypatch.setattr(pipeline, "fingerprint_exists", AsyncMock(return_value=False))
    upsert_mock = AsyncMock()
    monkeypatch.setattr(pipeline, "upsert_ledger_entry", upsert_mock)

    db = MagicMock()

    outcome = await pipeline.process_company_raw_jobs(
        db,
        company,
        [job],
        pipeline_run_id=uuid4(),
        settings=Settings(),
    )

    assert outcome.jobs_new == 0
    assert outcome.jobs_ledger_baselined == 1
    assert outcome.jobs_rejected_stale_pipeline == 0
    db.add.assert_not_called()
    upsert_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_company_raw_jobs_second_run_ingests_new_jobs(monkeypatch) -> None:
    company = _company()
    job = {"id": "job-new", "title": "Engineer", "content": "<p>New role</p>"}

    monkeypatch.setattr(pipeline, "load_ledger_hashes", AsyncMock(return_value={"job-old": "existing-hash"}))
    monkeypatch.setattr(pipeline, "_latest_hashes_for_company", AsyncMock(return_value={}))
    monkeypatch.setattr(pipeline, "_normalized_map_for_company", AsyncMock(return_value={}))
    monkeypatch.setattr(pipeline, "fingerprint_exists", AsyncMock(return_value=False))
    monkeypatch.setattr(
        pipeline,
        "upsert_job_archive_from_deterministic",
        AsyncMock(return_value=uuid4()),
    )
    monkeypatch.setattr(
        pipeline,
        "_upsert_normalized_core",
        AsyncMock(return_value=SimpleNamespace(id=uuid4())),
    )
    monkeypatch.setattr(pipeline, "queue_job_for_enrichment", AsyncMock())
    upsert_mock = AsyncMock()
    monkeypatch.setattr(pipeline, "upsert_ledger_entry", upsert_mock)

    db = MagicMock()
    db.flush = AsyncMock()

    outcome = await pipeline.process_company_raw_jobs(
        db,
        company,
        [job],
        pipeline_run_id=uuid4(),
        settings=Settings(),
    )

    assert outcome.jobs_new == 1
    assert outcome.jobs_ledger_baselined == 0
    db.add.assert_called_once()
    upsert_mock.assert_awaited_once()
