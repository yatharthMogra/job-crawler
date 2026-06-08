#!/usr/bin/env python3
"""Render a local HTML preview of the daily briefing email for a candidate."""

from __future__ import annotations

import argparse
import asyncio
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "recommendation_service"))

from app.config import get_settings
from app.database import AsyncSessionLocal
from app.notification.ranker import deduplicate_ranked_jobs, rank_jobs
from app.notification.renderer import render_daily_briefing
from app.notification.retrieval import build_constraint_filters, query_jobs_in_pools
from app.scoring.explainability import generate_explanations
from app.services.profile_loader import load_user_profile
from app.services.subscriptions import get_active_pools

DEFAULT_CANDIDATE_ID = "6230dd88-b346-4e96-94fd-4a51c4500f34"
OUT_PATH = ROOT / "exports" / "preview_daily_briefing.html"


async def render_preview(candidate_id: uuid.UUID, *, app_base_url: str | None) -> str:
    settings = get_settings()
    async with AsyncSessionLocal() as db:
        profile = await load_user_profile(db, candidate_id)
        if profile is None:
            raise RuntimeError(f"No profile for candidate {candidate_id}")

        pools = await get_active_pools(db, candidate_id)
        filters = build_constraint_filters(profile)

        all_jobs: list = []
        offset = 0
        while True:
            chunk = await query_jobs_in_pools(
                db, pools=pools, filters=filters, limit=200, offset=offset
            )
            if not chunk:
                break
            all_jobs.extend(chunk)
            offset += len(chunk)
            if len(chunk) < 200:
                break

        ranked = deduplicate_ranked_jobs(rank_jobs(all_jobs, profile, settings))
        top = ranked[: settings.notification_jobs_per_email]
        jobs_with_explanations = [
            (job, generate_explanations(job, profile), score) for job, score in top
        ]

        return render_daily_briefing(
            jobs_with_explanations=jobs_with_explanations,
            user_profile=profile,
            total_scanned=len(all_jobs),
            app_base_url=app_base_url,
        )


async def main() -> None:
    parser = argparse.ArgumentParser(description="Preview daily briefing HTML email")
    parser.add_argument("--candidate-id", default=DEFAULT_CANDIDATE_ID)
    parser.add_argument("--output", default=str(OUT_PATH))
    parser.add_argument("--app-base-url", default="http://localhost:3000")
    args = parser.parse_args()

    html = await render_preview(uuid.UUID(args.candidate_id), app_base_url=args.app_base_url)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    asyncio.run(main())
