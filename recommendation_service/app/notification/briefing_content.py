from __future__ import annotations

from datetime import datetime, timezone

from app.models.shared import NormalizedJob

_EFFORT_MINUTES = {"LOW": 3, "MEDIUM": 5, "HIGH": 8}
_EFFORT_DETAILS = {
    "LOW": "One-click application",
    "MEDIUM": "Resume upload + standard application",
    "HIGH": "Additional screening questions",
}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def format_briefing_date(now: datetime | None = None) -> str:
    now = _ensure_utc(now or _utc_now())
    return now.strftime("%a, %b %d %H:%M").upper()


def format_salary(job: NormalizedJob) -> str | None:
    if job.salary_min and job.salary_max:
        return f"${job.salary_min // 1000}k - ${job.salary_max // 1000}k"
    if job.salary_max:
        return f"Up to ${job.salary_max // 1000}k"
    if job.salary_min:
        return f"From ${job.salary_min // 1000}k"
    return None


def posted_ago(posted_at: datetime | None) -> str:
    if posted_at is None:
        return "Recently"
    posted_at = _ensure_utc(posted_at)
    hours = int((_utc_now() - posted_at).total_seconds() / 3600)
    if hours < 1:
        minutes = max(int((_utc_now() - posted_at).total_seconds() / 60), 1)
        return f"{minutes}m ago"
    if hours < 24:
        return f"{hours}h ago"
    days = hours // 24
    return f"{days}d ago"


def detected_after(job: NormalizedJob) -> str:
    if job.posted_at is None:
        return "Recently"
    posted_at = _ensure_utc(job.posted_at)
    created_at = _ensure_utc(job.created_at)
    lag_minutes = max(int((created_at - posted_at).total_seconds() / 60), 1)
    return f"{lag_minutes}m after"


def estimate_time_saved_minutes(total_scanned: int, jobs_sent: int) -> int:
    skipped = max(total_scanned - jobs_sent, 0)
    return skipped * 3


def estimate_total_review_minutes(total_scanned: int) -> int:
    return round(total_scanned * 3.6)


def _velocity_label(job: NormalizedJob) -> str:
    if job.posted_at is None:
        return "Moderate activity"
    hours = (_utc_now() - _ensure_utc(job.posted_at)).total_seconds() / 3600
    opp = job.opportunity_score or 0.0
    if hours <= 6 and opp >= 0.45:
        return "High velocity"
    if hours <= 24 and opp >= 0.45:
        return "Low competition window"
    return "Moderate activity"


def _competition_label(job: NormalizedJob) -> str:
    title_lower = job.title.lower()
    if any(token in title_lower for token in ("software engineer", "swe", "full stack", "fullstack")):
        return "High"
    opp = job.opportunity_score or 0.0
    if opp >= 0.5:
        return "Medium-Low"
    if opp >= 0.35:
        return "Medium"
    return "High"


def _visa_signal_label(job: NormalizedJob) -> str:
    status = (job.sponsorship_status or "").lower()
    if status == "yes":
        return "Low"
    if status == "no":
        return "High"
    return "Medium"


def _market_signals(job: NormalizedJob) -> list[str]:
    signals: list[str] = []
    location = (job.location or "").lower()
    title_lower = job.title.lower()

    if any(token in location for token in ("new york", "nyc", "manhattan", "brooklyn", "queens")):
        signals.append("NYC market")
    elif location:
        signals.append("Regional hiring market")

    if job.salary_max and job.salary_max >= 180_000:
        signals.append("Attractive compensation range")
    if any(token in title_lower for token in ("software engineer", "data scientist", "ml engineer")):
        signals.append("Popular role title")
    if job.application_effort == "LOW":
        signals.append("Quick application process")
    if len(job.job_capabilities) >= 4:
        signals.append("Broad technical scope")
    elif job.job_capabilities:
        signals.append(f"Specialized {job.job_capabilities[0].lower()} domain")

    deduped: list[str] = []
    for signal in signals:
        if signal not in deduped:
            deduped.append(signal)
    return deduped[:3]


def _summary_blurb(job: NormalizedJob, explanations: list[str], rank: int, score: float) -> str:
    if rank >= 4:
        return "Good engineering fit, but lower upside than the opportunities above."

    parts: list[str] = []
    if explanations:
        parts.append(f"Strong {explanations[0].lower()} alignment")
    elif score >= 0.5:
        parts.append("Excellent profile match")
    else:
        parts.append("Solid profile match")

    if job.salary_max and job.salary_max >= 180_000:
        parts.append("high compensation")
    elif _velocity_label(job) == "Low competition window":
        parts.append("favorable competition dynamics")
    else:
        parts.append("recent posting")

    if len(parts) == 1:
        return parts[0].capitalize() + "."
    return parts[0].capitalize() + " + " + " + ".join(parts[1:]) + "."


def _visa_color(label: str) -> str:
    if label == "Low":
        return "#67bb6b"
    if label == "High":
        return "#de6900"
    return "#de6900"


def _cta_style(rank: int, total_jobs: int) -> dict[str, str]:
    if rank == total_jobs and total_jobs > 1:
        return {
            "cta": "APPLY SOON",
            "cta_color": "#de6900",
            "cta_bg": "#2a1f14",
            "cta_border": "#de6900",
        }
    return {
        "cta": "APPLY NOW",
        "cta_color": "#67bb6b",
        "cta_bg": "#152218",
        "cta_border": "#67bb6b",
    }


def build_job_card(
    job: NormalizedJob,
    explanations: list[str],
    score: float,
    *,
    rank: int,
    total_jobs: int,
) -> dict:
    effort = job.application_effort or "MEDIUM"
    cta_style = _cta_style(rank, total_jobs)
    visa = _visa_signal_label(job)
    return {
        "rank": rank,
        "rank_label": f"{rank:02d}",
        "cta": cta_style["cta"],
        "cta_color": cta_style["cta_color"],
        "cta_bg": cta_style["cta_bg"],
        "cta_border": cta_style["cta_border"],
        "title": job.title,
        "company_name": job.company_name,
        "posting_url": job.posting_url or "#",
        "salary": format_salary(job),
        "location": job.location or "Location not specified",
        "posted_ago": posted_ago(job.posted_at),
        "detected_after": detected_after(job),
        "summary": _summary_blurb(job, explanations, rank, score),
        "velocity": _velocity_label(job),
        "velocity_color": "#67bb6b",
        "competition": _competition_label(job),
        "competition_color": "#eeeeee",
        "visa_signal": visa,
        "visa_color": _visa_color(visa),
        "market_signals": _market_signals(job),
        "profile_match_tags": explanations,
        "effort_minutes": _EFFORT_MINUTES.get(effort, 5),
        "effort_detail": _EFFORT_DETAILS.get(effort, "Standard application"),
        "score": round(score, 3),
    }
