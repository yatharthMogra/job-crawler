from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.config import Settings
from app.notification.retrieval import build_notification_age_filter


def test_build_notification_age_filter_disabled_when_zero() -> None:
    assert build_notification_age_filter(Settings(notification_max_job_age_days=0)) == []


def test_build_notification_age_filter_includes_cutoff_clause() -> None:
    filters = build_notification_age_filter(Settings(notification_max_job_age_days=60))
    assert len(filters) == 1
    cutoff = datetime.now(timezone.utc) - timedelta(days=60)
    clause = str(filters[0].compile(compile_kwargs={"literal_binds": True}))
    assert "posted_at" in clause
    assert cutoff.strftime("%Y-%m-%d") in clause or "posted_at" in clause
