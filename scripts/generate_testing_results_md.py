#!/usr/bin/env python3
"""Generate testing_results.md from exports/user_recommendations.json."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "exports" / "user_recommendations.json"
OUT_PATH = ROOT / "testing_results.md"


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
    out.append(f"| Capabilities | {', '.join(u['capabilities'])} |")
    prefs = u["preferences"]
    out.append(
        f"| Preferred locations | {', '.join(prefs.get('preferred_locations') or []) or '—'} |"
    )
    out.append(f"| Primary roles | {', '.join(prefs.get('primary_roles') or []) or '—'} |")
    constraints = u["constraints"]
    out.append(
        f"| Hard constraints | sponsorship={constraints.get('sponsorship_required')}, "
        f"min_salary={constraints.get('minimum_salary')} |"
    )
    out.append("")
    out.append("### Match summary")
    out.append("")
    out.append(f"- **Total jobs matching subscribed pools (after filters):** {u['total_matching_jobs']}")
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


def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    yatharth, ram = data[0], data[1]
    y_scores = [j["personal_score"] for j in yatharth["personalized_ranked_all"] if j["personal_score"]]
    r_scores = [j["personal_score"] for j in ram["personalized_ranked_all"] if j["personal_score"]]
    y_ashby = sum(
        1 for j in yatharth["personalized_ranked_all"] if j["company"] in ("Ramp", "Notion", "Linear")
    )
    r_ashby = sum(
        1 for j in ram["personalized_ranked_all"] if j["company"] in ("Ramp", "Notion", "Linear")
    )

    lines = [
        "# User Recommendation Results",
        "",
        f"Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} after location scoring "
        "fix + notification dedup (889/889 enriched jobs).",
        "",
        "Pools synced via `PATCH /subscriptions`. Same subscription buckets as prior run.",
        "",
        "**Ranking modes:**",
        "- **Dashboard** — sorted by global `opportunity_score` (freshness + comp + effort)",
        "- **Personalized / Email** — sorted by profile match score "
        "(capabilities 40%, skills 25%, location 20%, comp 15%)",
        "",
        "Full machine-readable export: [`exports/user_recommendations.json`](exports/user_recommendations.json)",
        "",
        "## Changes vs prior run (pre-Ashby fix)",
        "",
        "| Metric | Yatharth (before → now) | Ram (before → now) |",
        "|--------|--------------------------|---------------------|",
        f"| Matching jobs | 260 → **{yatharth['total_matching_jobs']}** | "
        f"263 → **{ram['total_matching_jobs']}** |",
        f"| Unique personal scores | ~6 flat tiers → **{len(set(y_scores))}** | "
        f"~5 flat tiers → **{len(set(r_scores))}** |",
        f"| Personal score range | 0.075–0.3417 → **{min(y_scores):.4f}–{max(y_scores):.4f}** | "
        f"0.075–0.375 → **{min(r_scores):.4f}–{max(r_scores):.4f}** |",
        "| Skills in top-4 | empty on most | **populated** |",
        "| Ashby jobs in pool | 0 | **281 enriched** |",
        f"| Ramp/Notion/Linear visible | 0 → **{y_ashby}** | 0 → **{r_ashby}** |",
        "",
        "**Observations:**",
        "- Segment-aware location matcher now boosts NY-listed jobs when prefs are `NY, USA` / `New York, USA`.",
        "- Notification top-4 dedupes same company+title across cities (keeps highest personal score).",
        "- Yatharth top-4 is NY/SF-multi-city heavy (ScaleAI, Figma, Ramp) — no Doha/London/Mexico outliers.",
        "- Ram top-4 includes Figma data science (#1) and Ramp data platform (#2).",
        f"- Personal score spread: Yatharth {len(set(y_scores))} unique tiers, Ram {len(set(r_scores))} unique tiers.",
        "",
        "---",
        "",
    ]
    for user in data:
        lines.extend(fmt_user(user))

    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT_PATH} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
