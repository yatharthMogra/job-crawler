from app.config import Settings, notification_interval_kwargs


def test_notification_interval_kwargs_uses_minutes_when_set() -> None:
    settings = Settings(notification_cadence_minutes=720, notification_cadence_hours=24)
    assert notification_interval_kwargs(settings) == {"minutes": 720}


def test_notification_interval_kwargs_falls_back_to_hours() -> None:
    settings = Settings(notification_cadence_minutes=None, notification_cadence_hours=12)
    assert notification_interval_kwargs(settings) == {"hours": 12}
