from __future__ import annotations

from app.services.entitlements import (
    FREE_CADENCE_OPTIONS_MINUTES,
    PLUS_CADENCE_OPTIONS_MINUTES,
    PRO_CADENCE_OPTIONS_MINUTES,
    clamp_company_watch_cadence_minutes,
    clamp_max_emails_per_day,
    get_tier_limits,
    normalize_plan_tier,
    resolve_effective_plan_tier,
    tier_allows_ats_fit,
)


def test_normalize_plan_tier() -> None:
    assert normalize_plan_tier("pro") == "pro"
    assert normalize_plan_tier("plus") == "plus"
    assert normalize_plan_tier("free") == "free"
    assert normalize_plan_tier(None) == "free"
    assert normalize_plan_tier("unknown") == "free"


def test_free_tier_limits() -> None:
    limits = get_tier_limits("free")
    assert limits.max_companies == 0
    assert limits.ats_fit is False
    assert limits.hiring_manager is False
    assert limits.apply_agent is False


def test_plus_tier_limits() -> None:
    limits = get_tier_limits("plus")
    assert limits.max_companies == 25
    assert limits.cadence_min_minutes == 30
    assert limits.cadence_max_minutes == 180
    assert limits.delivery == "batched"
    assert limits.default_max_emails_per_day == 10
    assert limits.max_emails_per_day_cap == 20
    assert limits.ats_fit is True
    assert limits.hiring_manager is False


def test_pro_tier_limits() -> None:
    limits = get_tier_limits("pro")
    assert limits.max_companies == 100
    assert limits.cadence_min_minutes == 15
    assert limits.cadence_max_minutes == 60
    assert limits.ats_fit is True
    assert limits.hiring_manager is True
    assert limits.apply_agent is True


def test_clamp_company_watch_cadence_minutes_plus() -> None:
    assert clamp_company_watch_cadence_minutes(10, "plus") == 30
    assert clamp_company_watch_cadence_minutes(60, "plus") == 60
    assert clamp_company_watch_cadence_minutes(240, "plus") == 180


def test_clamp_company_watch_cadence_minutes_pro() -> None:
    assert clamp_company_watch_cadence_minutes(5, "pro") == 15
    assert clamp_company_watch_cadence_minutes(45, "pro") == 45
    assert clamp_company_watch_cadence_minutes(120, "pro") == 60


def test_clamp_max_emails_per_day() -> None:
    assert clamp_max_emails_per_day(15, "plus") == 15
    assert clamp_max_emails_per_day(100, "plus") == 20
    assert clamp_max_emails_per_day(100, "pro") == 50


def test_tier_allows_ats_fit() -> None:
    assert tier_allows_ats_fit("free") is False
    assert tier_allows_ats_fit("plus") is True
    assert tier_allows_ats_fit("pro") is True


def test_resolve_effective_plan_tier_expired() -> None:
    from datetime import datetime, timedelta, timezone

    past = datetime.now(timezone.utc) - timedelta(days=1)
    assert resolve_effective_plan_tier("plus", "active", past) == "free"


def test_resolve_effective_plan_tier_past_due_grace() -> None:
    from datetime import datetime, timedelta, timezone

    past = datetime.now(timezone.utc) - timedelta(days=1)
    assert resolve_effective_plan_tier("plus", "past_due", past) == "plus"
    expired = datetime.now(timezone.utc) - timedelta(days=5)
    assert resolve_effective_plan_tier("plus", "past_due", expired) == "free"


def test_cadence_option_lists() -> None:
    assert FREE_CADENCE_OPTIONS_MINUTES[0] == 360
    assert PLUS_CADENCE_OPTIONS_MINUTES[0] == 30
    assert PRO_CADENCE_OPTIONS_MINUTES[0] == 15
