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
    return render_personalized_digest(
        jobs_with_explanations=jobs_with_explanations,
        user_profile=user_profile,
        total_scanned=total_scanned,
        briefing_date=briefing_date,
        app_base_url=app_base_url,
    )


def render_personalized_digest(
    *,
    jobs_with_explanations: list[tuple[NormalizedJob, list[str], float]],
    user_profile: UserProfile,
    total_scanned: int,
    briefing_date: datetime | None = None,
    app_base_url: str | None = None,
) -> str:
    template = _env.get_template("personalized_digest.html")
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
        manage_prefs_url=f"{base_url}/emails?candidate_id={candidate_id}",
        dashboard_url=f"{base_url}/jobs/recommended?candidate_id={candidate_id}",
        unsubscribe_url=f"{base_url}/unsubscribe?candidate_id={candidate_id}&channel=digest",
    )


def render_company_watch(
    *,
    job: NormalizedJob,
    explanations: list[str],
    user_profile: UserProfile,
    company_name: str,
    app_base_url: str | None = None,
    plan_tier: str = "plus",
) -> str:
    template = _env.get_template("company_watch.html")
    base_url = (app_base_url or _DEFAULT_APP_BASE_URL).rstrip("/")
    candidate_id = str(user_profile.candidate_id)
    job_card = build_job_card(job, explanations, score=0.0, rank=1, total_jobs=1)
    sla_message = (
        "We notify you within 30 minutes of learning about new postings."
        if plan_tier == "plus"
        else "We batch company alerts and send them every 6–12 hours."
    )

    return template.render(
        user_name=user_profile.name,
        company_name=company_name,
        job=job_card,
        sla_message=sla_message,
        manage_prefs_url=f"{base_url}/emails?candidate_id={candidate_id}",
        unsubscribe_url=f"{base_url}/unsubscribe?candidate_id={candidate_id}&channel=company_watch",
    )


def render_company_watch_batch(
    *,
    jobs_with_explanations: list[tuple[NormalizedJob, list[str], str]],
    user_profile: UserProfile,
    app_base_url: str | None = None,
) -> str:
    template = _env.get_template("company_watch_batch.html")
    base_url = (app_base_url or _DEFAULT_APP_BASE_URL).rstrip("/")
    candidate_id = str(user_profile.candidate_id)
    jobs_sent = len(jobs_with_explanations)

    jobs_payload = [
        {
            **build_job_card(job, explanations, score=0.0, rank=idx, total_jobs=jobs_sent),
            "company_name": company_name,
        }
        for idx, (job, explanations, company_name) in enumerate(jobs_with_explanations, start=1)
    ]

    return template.render(
        user_name=user_profile.name,
        jobs=jobs_payload,
        jobs_sent=jobs_sent,
        manage_prefs_url=f"{base_url}/emails?candidate_id={candidate_id}",
        unsubscribe_url=f"{base_url}/unsubscribe?candidate_id={candidate_id}&channel=company_watch",
    )
