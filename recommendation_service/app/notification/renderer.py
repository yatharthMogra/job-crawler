from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.constants import EFFORT_LABELS
from app.models.shared import NormalizedJob
from app.services.profile_loader import UserProfile

_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATE_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)


def _format_salary(job: NormalizedJob) -> str | None:
    if job.salary_min and job.salary_max:
        return f"${job.salary_min:,} - ${job.salary_max:,}"
    if job.salary_max:
        return f"Up to ${job.salary_max:,}"
    if job.salary_min:
        return f"From ${job.salary_min:,}"
    return None


def _posted_ago(posted_at: datetime | None) -> str:
    if posted_at is None:
        return "Recently"
    now = datetime.now(timezone.utc)
    if posted_at.tzinfo is None:
        posted_at = posted_at.replace(tzinfo=timezone.utc)
    hours = int((now - posted_at).total_seconds() / 3600)
    if hours < 1:
        return "Just posted"
    if hours < 24:
        return f"{hours}h ago"
    days = hours // 24
    return f"{days}d ago"


def render_daily_briefing(
    *,
    jobs_with_explanations: list[tuple[NormalizedJob, list[str], float]],
    user_profile: UserProfile,
    total_scanned: int,
) -> str:
    template = _env.get_template("daily_briefing.html")
    jobs_payload = []
    for job, explanations, score in jobs_with_explanations:
        jobs_payload.append(
            {
                "title": job.title,
                "company_name": job.company_name,
                "posting_url": job.posting_url or "#",
                "salary": _format_salary(job),
                "location": job.location or "Location not specified",
                "remote_type": job.remote_type,
                "posted_ago": _posted_ago(job.posted_at),
                "effort_label": EFFORT_LABELS.get(job.application_effort or "MEDIUM", "Standard"),
                "explanations": explanations,
                "score": round(score, 3),
            }
        )
    return template.render(
        user_name=user_profile.name,
        jobs=jobs_payload,
        jobs_sent=len(jobs_payload),
        total_scanned=total_scanned,
    )
