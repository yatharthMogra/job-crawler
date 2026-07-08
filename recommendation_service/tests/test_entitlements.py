from app.services.entitlements import (
    clamp_company_watch_cadence_minutes,
    clamp_max_emails_per_day,
    get_tier_limits,
    normalize_plan_tier,
)


def test_normalize_plan_tier() -> None:
    assert normalize_plan_tier("plus") == "plus"
    assert normalize_plan_tier("free") == "free"
    assert normalize_plan_tier(None) == "free"
    assert normalize_plan_tier("unknown") == "free"


def test_free_tier_limits() -> None:
    limits = get_tier_limits("free")
    assert limits.max_companies == 5
    assert limits.delivery == "batched"
    assert limits.cadence_min_minutes == 360
    assert limits.cadence_max_minutes == 720


def test_plus_tier_limits() -> None:
    limits = get_tier_limits("plus")
    assert limits.max_companies == 25
    assert limits.delivery == "batched"
    assert limits.cadence_min_minutes == 30
    assert limits.cadence_max_minutes == 180


def test_clamp_company_watch_cadence_minutes_free() -> None:
    assert clamp_company_watch_cadence_minutes(100, "free") == 360
    assert clamp_company_watch_cadence_minutes(500, "free") == 500
    assert clamp_company_watch_cadence_minutes(900, "free") == 720


def test_clamp_company_watch_cadence_minutes_plus() -> None:
    assert clamp_company_watch_cadence_minutes(10, "plus") == 30
    assert clamp_company_watch_cadence_minutes(60, "plus") == 60
    assert clamp_company_watch_cadence_minutes(240, "plus") == 180


def test_clamp_max_emails_per_day() -> None:
    assert clamp_max_emails_per_day(0, "free") == 1
    assert clamp_max_emails_per_day(5, "free") == 5
    assert clamp_max_emails_per_day(100, "free") == 10
    assert clamp_max_emails_per_day(15, "plus") == 15
    assert clamp_max_emails_per_day(100, "plus") == 20
