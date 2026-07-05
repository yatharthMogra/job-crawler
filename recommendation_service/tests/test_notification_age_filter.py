from datetime import datetime, timedelta, timezone

from app.config import Settings
from app.notification.retrieval import build_notification_age_filter


def test_build_notification_age_filter_disabled_when_zero() -> None:
    assert build_notification_age_filter(Settings(job_max_age_days=0)) == []


def test_build_notification_age_filter_applies_cutoff() -> None:
    filters = build_notification_age_filter(Settings(job_max_age_days=7))
    assert len(filters) == 1
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    clause = str(filters[0])
    assert "reference_at" in clause
