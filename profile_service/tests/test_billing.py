from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.services.stripe_billing import effective_plan_tier


def test_effective_plan_tier_active() -> None:
    future = datetime.now(timezone.utc) + timedelta(days=10)
    assert effective_plan_tier("plus", "active", future) == "plus"
    assert effective_plan_tier("pro", "active", future) == "pro"


def test_effective_plan_tier_expired() -> None:
    past = datetime.now(timezone.utc) - timedelta(days=1)
    assert effective_plan_tier("plus", "active", past) == "free"


def test_effective_plan_tier_past_due_grace() -> None:
    past = datetime.now(timezone.utc) - timedelta(days=1)
    assert effective_plan_tier("plus", "past_due", past) == "plus"
    expired = datetime.now(timezone.utc) - timedelta(days=5)
    assert effective_plan_tier("plus", "past_due", expired) == "free"


def test_effective_plan_tier_canceled_until_period_end() -> None:
    future = datetime.now(timezone.utc) + timedelta(days=5)
    assert effective_plan_tier("pro", "canceled", future) == "pro"
    past = datetime.now(timezone.utc) - timedelta(hours=1)
    assert effective_plan_tier("pro", "canceled", past) == "free"


def test_effective_plan_tier_manual_comp() -> None:
    assert effective_plan_tier("plus", "none", None) == "plus"
