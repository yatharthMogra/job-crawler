from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.models.shared import NormalizedJob
from app.notification.briefing_content import (
    build_job_card,
    estimate_time_saved_minutes,
    estimate_total_review_minutes,
    format_briefing_date,
)
from app.services.profile_loader import UserProfile

_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATE_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)

_DEFAULT_APP_BASE_URL = "http://localhost:3000"


def render_daily_briefing(
    *,
    jobs_with_explanations: list[tuple[NormalizedJob, list[str], float]],
    user_profile: UserProfile,
    total_scanned: int,
    briefing_date: datetime | None = None,
    app_base_url: str | None = None,
) -> str:
    template = _env.get_template("daily_briefing.html")
    jobs_sent = len(jobs_with_explanations)
    base_url = (app_base_url or _DEFAULT_APP_BASE_URL).rstrip("/")
    candidate_id = str(user_profile.candidate_id)

    jobs_payload = [
        build_job_card(job, explanations, score, rank=idx, total_jobs=jobs_sent)
        for idx, (job, explanations, score) in enumerate(jobs_with_explanations, start=1)
    ]

    return template.render(
        user_name=user_profile.name,
        briefing_date=format_briefing_date(briefing_date),
        jobs=jobs_payload,
        jobs_sent=jobs_sent,
        total_scanned=total_scanned,
        time_saved_minutes=estimate_time_saved_minutes(total_scanned, jobs_sent),
        total_review_minutes=estimate_total_review_minutes(total_scanned),
        manage_prefs_url=f"{base_url}/filters?candidate_id={candidate_id}",
        dashboard_url=f"{base_url}/jobs/recommended?candidate_id={candidate_id}",
        unsubscribe_url=f"{base_url}/unsubscribe?candidate_id={candidate_id}",
    )
