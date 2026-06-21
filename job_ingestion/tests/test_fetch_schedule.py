from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from app.ingestion.fetch_schedule import (
    company_shard,
    current_tick,
    select_due_companies_from_rows,
)
from app.ingestion.fetch_schedule_config import (
    DEFAULT_FETCH_SCHEDULE,
    FetchScheduleConfig,
    parse_fetch_schedule_json,
)
from app.models.company import Company


def test_parse_fetch_schedule_json_uses_defaults_when_empty() -> None:
    schedule = parse_fetch_schedule_json("")
    assert schedule.tick_minutes == DEFAULT_FETCH_SCHEDULE["tick_minutes"]
    assert schedule.batch_cap == DEFAULT_FETCH_SCHEDULE["batch_cap"]
    assert schedule.waas.dedicated_job is True


def test_parse_fetch_schedule_json_merges_partial_override() -> None:
    raw = json.dumps({"tick_minutes": 15, "intervals": {"greenhouse": {"1": 30}}})
    schedule = parse_fetch_schedule_json(raw)
    assert schedule.tick_minutes == 15
    assert schedule.interval_minutes("greenhouse", 1) == 30
    assert schedule.interval_minutes("greenhouse", 2) == 180


def test_parse_fetch_schedule_json_rejects_invalid_json() -> None:
    with pytest.raises(ValueError, match="not valid JSON"):
        parse_fetch_schedule_json("{not-json")


def test_interval_minutes_falls_back_for_unknown_platform() -> None:
    schedule = FetchScheduleConfig()
    assert schedule.interval_minutes("unknown_platform", 2) == 720


def test_num_shards_derived_from_interval_and_tick() -> None:
    schedule = parse_fetch_schedule_json("")
    assert schedule.num_shards("greenhouse", 1) == 5


def test_fetch_schedule_config_default_tier_validation() -> None:
    with pytest.raises(ValueError):
        FetchScheduleConfig(default_fetch_tier=4)


def test_current_tick() -> None:
    assert current_tick(10, now=6000) == 10
    assert current_tick(10, now=5999) == 9


def test_company_shard_is_stable() -> None:
    assert company_shard("notion", 6) == company_shard("notion", 6)
    assert 0 <= company_shard("notion", 6) < 6


def _company(
    *,
    board_token: str,
    platform: str = "greenhouse",
    fetch_tier: int = 1,
    last_successful_fetch_at: datetime | None = None,
) -> Company:
    return Company(
        id=uuid4(),
        name=board_token,
        platform=platform,
        board_token=board_token,
        fetch_tier=fetch_tier,
        is_active=True,
        last_successful_fetch_at=last_successful_fetch_at,
    )


def test_select_due_companies_respects_last_successful_fetch_at() -> None:
    schedule = FetchScheduleConfig(tick_minutes=10, batch_cap=50)
    now = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    recent = now - timedelta(minutes=10)
    company = _company(board_token="fresh-co", last_successful_fetch_at=recent)
    tick = current_tick(schedule.tick_minutes, now=now.timestamp())

    result = select_due_companies_from_rows(
        [company],
        schedule,
        now=now,
        tick=tick,
    )
    assert result.company_ids == []


def test_select_due_companies_includes_never_fetched_on_matching_shard() -> None:
    schedule = FetchScheduleConfig(tick_minutes=10, batch_cap=50)
    company = _company(board_token="alpha")
    num_shards = schedule.num_shards(company.platform, company.fetch_tier)
    shard = company_shard(company.board_token, num_shards)
    now = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    tick = shard

    result = select_due_companies_from_rows(
        [company],
        schedule,
        now=now,
        tick=tick,
    )
    assert result.company_ids == [company.id]
    assert result.schedule_metadata["companies_selected"] == 1


def test_select_due_companies_excludes_workatastartup_when_configured() -> None:
    schedule = FetchScheduleConfig(tick_minutes=10, batch_cap=50)
    company = _company(board_token="yc-global", platform="workatastartup")
    now = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)

    result = select_due_companies_from_rows(
        [company],
        schedule,
        now=now,
        tick=0,
        exclude_platforms={"workatastartup"},
    )
    assert result.company_ids == []


def test_select_due_companies_excludes_manual_push_companies() -> None:
    schedule = FetchScheduleConfig(tick_minutes=10, batch_cap=50)
    company = _company(board_token="tesla")
    company.platform = "tesla_careers"
    company.platform_config = {"ingestion_mode": "manual_push", "sites": ["US"]}
    now = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)

    result = select_due_companies_from_rows(
        [company],
        schedule,
        now=now,
        tick=0,
    )
    assert result.company_ids == []


def test_select_due_companies_orders_oldest_fetch_first_and_caps_batch() -> None:
    schedule = FetchScheduleConfig(tick_minutes=1, batch_cap=1, intervals={"greenhouse": {"1": 1}})
    now = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    older = _company(board_token="older-co", last_successful_fetch_at=now - timedelta(hours=2))
    newer = _company(board_token="newer-co", last_successful_fetch_at=now - timedelta(hours=1))
    tick = current_tick(schedule.tick_minutes, now=now.timestamp())

    for company in (older, newer):
        num_shards = schedule.num_shards(company.platform, company.fetch_tier)
        assert company_shard(company.board_token, num_shards) == tick % num_shards

    result = select_due_companies_from_rows(
        [newer, older],
        schedule,
        now=now,
        tick=tick,
    )
    assert result.company_ids == [older.id]
    assert result.schedule_metadata["companies_due"] == 2
    assert result.schedule_metadata["companies_selected"] == 1
