#!/usr/bin/env python3
"""Generate testing_results.md from exports/user_recommendations.json."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "exports" / "user_recommendations.json"
OUT_PATH = ROOT / "testing_results.md"

RECO_ROOT = ROOT / "recommendation_service"
sys.path.insert(0, str(RECO_ROOT))
os.chdir(RECO_ROOT)

from sqlalchemy import text

from app.database import AsyncSessionLocal, engine


async def fetch_index_stats() -> dict:
    from app.config import get_settings

    settings = get_settings()
    async with AsyncSessionLocal() as db:
        row = (
            await db.execute(
                text(
                    """
                    SELECT
                      (SELECT COUNT(*) FROM normalized_jobs
                        WHERE is_active AND processing_state = 'success'
                          AND opportunity_score IS NOT NULL) AS reco_eligible,
                      (SELECT COUNT(*) FROM normalized_jobs WHERE is_active) AS active_normalized,
                      (SELECT COUNT(*) FROM job_archive) AS archive_total,
                      (SELECT COUNT(*) FROM companies WHERE is_active) AS active_companies
                    """
                )
            )
        ).one()
        stats = dict(row._mapping)
        stats["domain_filter_enabled"] = settings.domain_filter_enabled
        stats["role_intent_filter_enabled"] = settings.role_intent_filter_enabled
        stats["clearance_filter_enabled"] = settings.clearance_filter_enabled
        stats["sponsorship_score_enabled"] = settings.sponsorship_score_enabled
        return stats


def fmt_user(u: dict) -> list[str]:
    out: list[str] = []
    out.append(f"## {u['name']} (`{u['email']}`)")
    out.append("")
    out.append(f"**Candidate ID:** `{u['candidate_id']}`")
    out.append("")
    out.append("### Subscribed pools")
    for pool in u["subscribed_pools"]:
        out.append(f"- `{pool}`")
    out.append("")
    out.append("### Profile snapshot")
    out.append("")
    out.append("| Field | Value |")
    out.append("|-------|-------|")
    out.append(f"| Capabilities | {', '.join(u['capabilities']) or '—'} |")
    prefs = u["preferences"]
    out.append(
        f"| Preferred locations | {', '.join(prefs.get('preferred_locations') or []) or '—'} |"
    )
    out.append(f"| Primary roles | {', '.join(prefs.get('primary_roles') or []) or '—'} |")
    constraints = u["constraints"]
    target_seniority = constraints.get("target_seniority")
    seniority_str = ", ".join(target_seniority) if isinstance(target_seniority, list) else "—"
    out.append(
        f"| Hard constraints | sponsorship={constraints.get('sponsorship_required')}, "
        f"min_salary={constraints.get('minimum_salary')}, target_seniority={seniority_str} |"
    )
    out.append("")
    out.append("### Match summary")
    out.append("")
    out.append(f"- **Total jobs matching subscribed pools (after filters):** {u['total_matching_jobs']}")
    if u.get("notification_eligible_jobs") is not None:
        out.append(
            f"- **Notification-eligible jobs (≤60d, not yet emailed):** {u['notification_eligible_jobs']}"
        )
    out.append(
        f"- **Personal score range:** {u.get('personal_score_min')} – {u.get('personal_score_max')} "
        f"({u.get('personal_score_unique')} unique tiers)"
    )
    out.append("- Pool tag counts (jobs can appear in multiple pools):")
    out.append("")
    out.append("| Pool | Job tag count |")
    out.append("|------|---------------|")
    for row in u["pool_breakdown"]:
        out.append(f"| `{row['pool']}` | {row['jobs']} |")
    out.append("")
    out.append("### Email notification — top 4 (personalized)")
    out.append("")
    for job in u["notification_top_4"]:
        out.append(f"#### #{job['rank']} — {job['title']} @ {job['company']}")
        out.append("")
        out.append(f"- **Location:** {job['location'] or '—'} ({job['remote_type']})")
        out.append(f"- **Posted:** {job['posted_at'] or '—'}")
        out.append(f"- **Salary:** {job.get('salary_min') or '—'} – {job.get('salary_max') or '—'}")
        out.append(f"- **Effort:** {job['application_effort']}")
        out.append(f"- **Opportunity score:** {job['opportunity_score']}")
        out.append(f"- **Personal score:** {job['personal_score']}")
        pools = ", ".join(f"`{p}`" for p in (job.get("retrieval_pools") or [])[:4])
        roles = ", ".join(job.get("normalized_roles") or [])
        caps = ", ".join((job.get("job_capabilities") or [])[:6])
        skills = ", ".join((job.get("skills") or job.get("tech_stack") or [])[:6])
        reasons = ", ".join(job.get("match_reasons") or []) or "—"
        out.append(f"- **Pools:** {pools}")
        out.append(f"- **Roles:** {roles}")
        out.append(f"- **Capabilities:** {caps}")
        out.append(f"- **Skills:** {skills}")
        out.append(f"- **Match reasons:** {reasons}")
        out.append(f"- **URL:** {job['posting_url']}")
        out.append("")
    out.append("### Full personalized ranking (all jobs)")
    out.append("")
    out.append("| Rank | Title | Company | Location | Opp | Personal | Pools | Match reasons |")
    out.append("|------|-------|---------|----------|-----|----------|-------|---------------|")
    for job in u["personalized_ranked_all"]:
        pools = ", ".join((job.get("retrieval_pools") or [])[:2])
        reasons = ", ".join((job.get("match_reasons") or [])[:3]) or "—"
        location = (job.get("location") or "—").replace("|", "/")
        title = (job.get("title") or "").replace("|", "/")
        out.append(
            f"| {job['rank']} | {title} | {job['company']} | {location} | "
            f"{job['opportunity_score']} | {job['personal_score']} | {pools} | {reasons} |"
        )
    out.append("")
    return out


async def generate() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    stats = await fetch_index_stats()
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "# User Recommendation Results",
        "",
        f"Generated {generated} "
        f"({stats['reco_eligible']:,} recommendation-eligible active jobs, "
        f"{stats['active_normalized']:,} active normalized rows, "
        f"{stats['archive_total']:,} archived identities, "
        f"{stats['active_companies']} active companies; "
        f"domain_filter={stats['domain_filter_enabled']}, "
        f"role_intent_filter={stats['role_intent_filter_enabled']}, "
        f"clearance_filter={stats['clearance_filter_enabled']}, "
        f"sponsorship_score={stats['sponsorship_score_enabled']}).",
        "",
        "Active layer (`normalized_jobs`) retains jobs ≤7 days; long-lived history lives in `job_archive`.",
        "",
        "Pools synced via `PATCH /subscriptions` from profile preferences or existing subscriptions.",
        "",
        "**Ranking modes:**",
        "- **Dashboard** — sorted by global `opportunity_score` (freshness + comp + effort)",
        "- **Personalized / Email** — sorted by profile match score "
        "(capabilities 40%, skills 25%, location 20%, comp 15%, seniority soft penalty); "
        "ties broken by `posted_at` then `opportunity_score`",
        "- **Email retrieval** — only jobs posted within 60 days, not previously emailed; "
        "skips send when fewer than 3 eligible jobs (daily cadence default)",
        "",
        "Full machine-readable export: [`exports/user_recommendations.json`](exports/user_recommendations.json)",
        "",
        "## Run summary",
        "",
        "| User | Matching jobs | Personal score range | Unique score tiers | Subscribed pools |",
        "|------|---------------|----------------------|--------------------|------------------|",
    ]
    for u in data:
        pools = ", ".join(f"`{p}`" for p in u["subscribed_pools"][:4])
        if len(u["subscribed_pools"]) > 4:
            pools += f" (+{len(u['subscribed_pools']) - 4})"
        lines.append(
            f"| {u['name']} | {u['total_matching_jobs']} | "
            f"{u.get('personal_score_min')}–{u.get('personal_score_max')} | "
            f"{u.get('personal_score_unique')} | {pools} |"
        )
    lines.extend(["", "---", ""])
    for user in data:
        lines.extend(fmt_user(user))

    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT_PATH} ({len(lines)} lines)")


def main() -> None:
    async def _run() -> None:
        try:
            await generate()
        finally:
            await engine.dispose()

    asyncio.run(_run())


if __name__ == "__main__":
    main()
