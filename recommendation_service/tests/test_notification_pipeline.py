from __future__ import annotations

from app.config import Settings
from app.notification.digest import should_send_digest


def test_should_send_notification_meets_minimum() -> None:
    settings = Settings(notification_min_jobs_to_send=1)
    assert should_send_digest(1, settings) is True
    assert should_send_digest(4, settings) is True


def test_should_send_notification_below_minimum() -> None:
    settings = Settings(notification_min_jobs_to_send=3)
    assert should_send_digest(2, settings) is False
    assert should_send_digest(1, settings) is False
    assert should_send_digest(0, settings) is False


def test_should_send_notification_disabled_when_zero() -> None:
    settings = Settings(notification_min_jobs_to_send=0)
    assert should_send_digest(1, settings) is True
