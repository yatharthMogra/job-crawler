import uuid
from datetime import datetime, timedelta, timezone

from app.config import Settings
from app.notification.digest import (
    clamp_cadence_hours,
    clamp_top_k,
    compute_next_digest_due_at,
    digest_window_start,
    should_send_digest,
    should_send_notification,
)
from app.models.notification_preferences import NotificationPreferences


def test_should_send_digest_meets_minimum() -> None:
    settings = Settings(notification_min_jobs_to_send=1)
    assert should_send_digest(1, settings) is True
    assert should_send_digest(4, settings) is True


def test_should_send_digest_below_minimum() -> None:
    settings = Settings(notification_min_jobs_to_send=3)
    assert should_send_digest(2, settings) is False
    assert should_send_digest(0, settings) is False


def test_should_send_notification_alias() -> None:
    settings = Settings(notification_min_jobs_to_send=1)
    assert should_send_notification(1, settings) is True


def test_clamp_cadence_hours() -> None:
    assert clamp_cadence_hours(1) == 3
    assert clamp_cadence_hours(24) == 24
    assert clamp_cadence_hours(200) == 168


def test_clamp_top_k() -> None:
    assert clamp_top_k(0) == 1
    assert clamp_top_k(4) == 4
    assert clamp_top_k(50) == 20


def test_compute_next_digest_due_at_from_last_send() -> None:
    last = datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc)
    due = compute_next_digest_due_at(last_sent_at=last, cadence_hours=24)
    assert due == last + timedelta(hours=24)


def test_digest_window_start_uses_last_sent() -> None:
    candidate_id = uuid.uuid4()
    last = datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc)
    prefs = NotificationPreferences(
        candidate_id=candidate_id,
        cadence_hours=24,
        last_digest_sent_at=last,
    )
    assert digest_window_start(prefs) == last


def test_digest_window_start_fallback_to_cadence() -> None:
    candidate_id = uuid.uuid4()
    now = datetime(2026, 6, 2, 12, 0, tzinfo=timezone.utc)
    prefs = NotificationPreferences(
        candidate_id=candidate_id,
        cadence_hours=6,
        last_digest_sent_at=None,
    )
    start = digest_window_start(prefs, now=now)
    assert start == now - timedelta(hours=6)
