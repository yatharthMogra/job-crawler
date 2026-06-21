from __future__ import annotations

from uuid import uuid4

import pytest

from app.config import Settings
from app.ingestion.fetch_backpressure import (
    apply_backpressure_to_companies,
    apply_fetch_backpressure,
    backpressure_metadata,
    evaluate_backpressure,
)
from app.models.company import Company


def _settings(**overrides: object) -> Settings:
    return Settings(**overrides)


def _company(*, fetch_tier: int = 2, platform: str = "greenhouse") -> Company:
    return Company(
        id=uuid4(),
        name="example-co",
        platform=platform,
        board_token="example-co",
        fetch_tier=fetch_tier,
        is_active=True,
    )


def test_evaluate_backpressure_below_threshold() -> None:
    decision = evaluate_backpressure(1999, settings=_settings())
    assert decision.active is False
    assert decision.depth == 1999


def test_evaluate_backpressure_at_threshold_skip_tiers() -> None:
    decision = evaluate_backpressure(2000, settings=_settings(fetch_backpressure_mode="skip_tiers"))
    assert decision.active is True
    assert decision.mode == "skip_tiers"
    assert decision.skip_tiers == frozenset({3})


def test_evaluate_backpressure_disabled() -> None:
    decision = evaluate_backpressure(5000, settings=_settings(fetch_backpressure_enabled=False))
    assert decision.active is False


def test_apply_backpressure_skip_tiers_removes_configured_tiers() -> None:
    decision = evaluate_backpressure(2500, settings=_settings(fetch_backpressure_mode="skip_tiers"))
    companies = [_company(fetch_tier=1), _company(fetch_tier=3), _company(fetch_tier=2)]
    filtered = apply_backpressure_to_companies(companies, decision)
    assert [company.fetch_tier for company in filtered] == [1, 2]


def test_apply_backpressure_halt_all() -> None:
    decision = evaluate_backpressure(
        2500,
        settings=_settings(fetch_backpressure_mode="halt_all", fetch_backpressure_allow_waas=False),
    )
    companies = [_company(fetch_tier=1), _company(fetch_tier=2, platform="workatastartup")]
    filtered = apply_backpressure_to_companies(companies, decision)
    assert filtered == []


def test_apply_backpressure_halt_all_allows_waas() -> None:
    decision = evaluate_backpressure(
        2500,
        settings=_settings(fetch_backpressure_mode="halt_all", fetch_backpressure_allow_waas=True),
    )
    waas = _company(fetch_tier=1, platform="workatastartup")
    gh = _company(fetch_tier=1)
    filtered = apply_backpressure_to_companies([gh, waas], decision)
    assert filtered == [waas]


def test_backpressure_metadata_includes_counts() -> None:
    decision = evaluate_backpressure(2100, settings=_settings()).with_company_counts(before=5, after=2)
    metadata = backpressure_metadata(decision)
    assert metadata["active"] is True
    assert metadata["companies_before"] == 5
    assert metadata["companies_after"] == 2


class _ScalarResult:
    def __init__(self, value: int) -> None:
        self._value = value

    def __iter__(self):
        return iter([self._value])


class _FakeDb:
    def __init__(self, depth: int) -> None:
        self.depth = depth

    async def scalar(self, stmt):  # noqa: ANN001, ARG002
        return self.depth


@pytest.mark.asyncio
async def test_apply_fetch_backpressure_when_disabled() -> None:
    companies = [_company(fetch_tier=3)]
    filtered, decision = await apply_fetch_backpressure(
        _FakeDb(depth=5000),
        companies,
        settings=_settings(fetch_backpressure_enabled=False),
    )
    assert filtered == companies
    assert decision.active is False


@pytest.mark.asyncio
async def test_apply_fetch_backpressure_filters_when_active() -> None:
    companies = [_company(fetch_tier=1), _company(fetch_tier=3)]
    filtered, decision = await apply_fetch_backpressure(
        _FakeDb(depth=2500),
        companies,
        settings=_settings(),
    )
    assert len(filtered) == 1
    assert filtered[0].fetch_tier == 1
    assert decision.companies_before == 2
    assert decision.companies_after == 1
