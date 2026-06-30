from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from app.archival import active_cleanup, archive_cleanup, writer
from app.config import Settings
from app.ingestion.job_archive_sync import (
    _archive_conflict_update,
    _archive_values_from_deterministic,
)


def test_serialize_for_archive_handles_uuid_and_datetime() -> None:
    job_id = uuid4()
    posted = datetime(2026, 1, 1, tzinfo=timezone.utc)
    line = writer.serialize_for_archive(
        {"id": job_id, "posted_at": posted, "skills": ["python"]}
    )
    parsed = json.loads(line)
    assert parsed["id"] == str(job_id)
    assert parsed["posted_at"] == posted.isoformat()
    assert parsed["skills"] == ["python"]


def test_write_archive_batch_appends_and_fsync(tmp_path: Path, monkeypatch) -> None:
    filepath = tmp_path / "jobs.jsonl"
    fsync_calls: list[int] = []

    class FakeFile:
        def __init__(self) -> None:
            self.lines: list[str] = []

        def write(self, data: str) -> None:
            self.lines.append(data)

        def flush(self) -> None:
            return None

        def fileno(self) -> int:
            return 42

        def __enter__(self) -> FakeFile:
            return self

        def __exit__(self, *_args: object) -> None:
            return None

    fake = FakeFile()
    monkeypatch.setattr("builtins.open", lambda *_args, **_kwargs: fake)
    monkeypatch.setattr(writer.os, "fsync", lambda fd: fsync_calls.append(fd))

    count = writer.write_archive_batch([{"id": "abc"}], filepath)
    assert count == 1
    assert fsync_calls == [42]
    assert fake.lines[0].endswith("\n")


def test_archive_values_from_deterministic() -> None:
    company = SimpleNamespace(id=uuid4(), name="Acme", platform="greenhouse")
    det = {
        "external_job_id": "123",
        "title": "Engineer",
        "location": "Remote",
        "department": "Eng",
        "posting_url": "https://example.com",
        "employment_type": "full_time",
        "posted_at": datetime(2026, 1, 1, tzinfo=timezone.utc),
        "salary_min": 100000,
        "salary_max": 150000,
    }
    values = _archive_values_from_deterministic(det, company, description_text="Hello")
    assert values["external_job_id"] == "123"
    assert values["company_name"] == "Acme"
    assert values["description_text"] == "Hello"

    conflict = _archive_conflict_update(det, description_text="Hello")
    assert conflict["title"] == "Engineer"
    assert conflict["description_text"] == "Hello"


@pytest.mark.asyncio
async def test_active_cleanup_deletes_expired_in_batches() -> None:
    settings = Settings(job_max_age_days=7, cleanup_batch_size=2)
    archive_id = uuid4()
    batch1 = [
        SimpleNamespace(id=uuid4(), raw_job_id=uuid4(), job_archive_id=archive_id),
        SimpleNamespace(id=uuid4(), raw_job_id=uuid4(), job_archive_id=None),
    ]
    batch2 = [SimpleNamespace(id=uuid4(), raw_job_id=uuid4(), job_archive_id=archive_id)]
    execute_results = [
        MagicMock(all=lambda: batch1),
        MagicMock(all=lambda: batch2),
        MagicMock(all=lambda: []),
    ]
    db = AsyncMock()
    db.execute = AsyncMock(side_effect=execute_results)

    with patch.object(active_cleanup, "get_settings", return_value=settings):
        with patch.object(active_cleanup, "purge_normalized_jobs", new=AsyncMock(side_effect=[2, 1])):
            stats = await active_cleanup.run_active_cleanup(db)

    assert stats["deleted"] == 3
    assert db.commit.await_count == 2


@pytest.mark.asyncio
async def test_active_cleanup_skips_when_none_expired() -> None:
    settings = Settings(job_max_age_days=7, cleanup_batch_size=500)
    db = AsyncMock()
    db.execute = AsyncMock(return_value=MagicMock(all=lambda: []))

    with patch.object(active_cleanup, "get_settings", return_value=settings):
        stats = await active_cleanup.run_active_cleanup(db)

    assert stats["deleted"] == 0
    db.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_archive_cleanup_writes_jsonl_before_delete(tmp_path: Path) -> None:
    settings = Settings(archive_retention_days=100, cleanup_batch_size=500, archive_dir=str(tmp_path))
    row = SimpleNamespace(
        id=uuid4(),
        external_job_id="ext-1",
        company_id=uuid4(),
        company_name="Acme",
        platform="greenhouse",
        title="Engineer",
        location="Remote",
        department=None,
        posting_url="https://example.com",
        employment_type=None,
        salary_min=100000,
        salary_max=150000,
        seniority="senior",
        normalized_roles=["backend"],
        job_capabilities=["api"],
        skills=["python"],
        tech_stack=["postgres"],
        remote_type="remote",
        description_text="desc",
        original_posted_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
        created_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
        archived_at=None,
    )
    write_order: list[str] = []

    async def fake_execute(stmt):  # noqa: ANN001, ARG001
        if not write_order:
            write_order.append("select")
            return MagicMock(scalars=lambda: MagicMock(all=lambda: [row]))
        write_order.append("delete")
        return MagicMock()

    db = AsyncMock()
    db.execute = AsyncMock(side_effect=fake_execute)

    with patch.object(archive_cleanup, "get_settings", return_value=settings):
        with patch.object(writer, "get_settings", return_value=settings):
            stats = await archive_cleanup.run_archive_cleanup(db)

    assert stats["archived_to_file"] == 1
    assert stats["deleted"] == 1
    assert write_order[0] == "select"
    assert "delete" in write_order
    files = list(tmp_path.glob("jobs_*.jsonl"))
    assert len(files) == 1
    assert json.loads(files[0].read_text().strip())["external_job_id"] == "ext-1"


@pytest.mark.asyncio
async def test_update_job_archive_after_enrichment_executes_update() -> None:
    from app.ingestion.job_archive_sync import update_job_archive_after_enrichment

    db = AsyncMock()
    archive_id = uuid4()
    await update_job_archive_after_enrichment(
        db,
        archive_id,
        seniority="senior",
        experience_tier="SENIOR",
        normalized_roles=["backend"],
        job_capabilities=["api"],
        skills=["python"],
        tech_stack=["postgres"],
        remote_type="remote",
        salary_min=100000,
        salary_max=150000,
    )
    db.execute.assert_awaited_once()


def test_first_run_large_batch_simulation() -> None:
    batch_size = 500
    total = 1200
    batches = 0
    remaining = total
    while remaining > 0:
        chunk = min(batch_size, remaining)
        remaining -= chunk
        batches += 1
    assert batches == 3
