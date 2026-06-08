#!/usr/bin/env python3
"""Generate stage-by-stage E2E pipeline visibility report."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "job_ingestion"))
sys.path.insert(0, str(ROOT / "recommendation_service"))

from sqlalchemy import text

from app.database import AsyncSessionLocal

TARGET_TOKENS = ["slate", "basis", "achievers", "greenhouse", "linear"]
RUN_ID = "73c45d70-e198-4af8-8081-d5025dc8f2a4"
CANDIDATE_ID = "6230dd88-b346-4e96-94fd-4a51c4500f34"


async def main() -> None:
    tokens_sql = ", ".join(f"'{t}'" for t in TARGET_TOKENS)
    report: dict = {"target_companies": TARGET_TOKENS, "pipeline_run_id": RUN_ID}

    async with AsyncSessionLocal() as db:
        report["stage_0_setup"] = {
            "active_companies": [
                dict(r._mapping)
                for r in (
                    await db.execute(
                        text(
                            "SELECT name, board_token, platform, is_active FROM companies ORDER BY name"
                        )
                    )
                ).all()
            ]
        }

        run = await db.execute(
            text("SELECT * FROM pipeline_runs WHERE id = :id"),
            {"id": RUN_ID},
        )
        run_row = run.mappings().first()
        report["stage_1_fetch"] = dict(run_row) if run_row else None

        company_results = await db.execute(
            text(
                """
                SELECT c.name, c.board_token, crr.jobs_fetched, crr.jobs_new,
                       crr.jobs_updated, crr.jobs_unchanged, crr.jobs_removed, crr.status
                FROM company_run_results crr
                JOIN companies c ON c.id = crr.company_id
                WHERE crr.pipeline_run_id = :run_id
                ORDER BY c.name
                """
            ),
            {"run_id": RUN_ID},
        )
        report["stage_1_fetch"]["company_breakdown"] = [dict(r) for r in company_results.mappings()]

        raw_stats = await db.execute(
            text(
                f"""
                SELECT c.board_token, COUNT(rj.id) AS raw_jobs
                FROM companies c
                LEFT JOIN raw_jobs rj ON rj.company_id = c.id
                WHERE c.board_token IN ({tokens_sql})
                GROUP BY c.board_token ORDER BY c.board_token
                """
            )
        )
        report["stage_2_raw_jobs"] = [dict(r) for r in raw_stats.mappings()]

        norm_sample = await db.execute(
            text(
                f"""
                SELECT c.board_token, nj.title, nj.location, nj.employment_type,
                       nj.processing_state, LEFT(nj.description_preview, 120) AS preview
                FROM normalized_jobs nj
                JOIN companies c ON c.id = nj.company_id
                WHERE c.board_token IN ({tokens_sql})
                ORDER BY c.board_token, nj.title
                LIMIT 8
                """
            )
        )
        report["stage_3_normalized_sample"] = [dict(r) for r in norm_sample.mappings()]

        norm_counts = await db.execute(
            text(
                f"""
                SELECT c.board_token, nj.processing_state, COUNT(*)
                FROM normalized_jobs nj
                JOIN companies c ON c.id = nj.company_id
                WHERE c.board_token IN ({tokens_sql})
                GROUP BY c.board_token, nj.processing_state
                ORDER BY c.board_token
                """
            )
        )
        report["stage_3_normalized_counts"] = [dict(r._mapping) for r in norm_counts]

        queue_stats = await db.execute(
            text(
                f"""
                SELECT eq.status, COUNT(*)
                FROM enrichment_queue eq
                JOIN normalized_jobs nj ON nj.id = eq.normalized_job_id
                JOIN companies c ON c.id = nj.company_id
                WHERE c.board_token IN ({tokens_sql})
                GROUP BY eq.status
                """
            )
        )
        report["stage_4_enrichment_queue"] = dict(queue_stats.all())

        batch_stats = await db.execute(
            text(
                """
                SELECT status, COUNT(*) AS batches, SUM(jobs_total) AS jobs,
                       SUM(actual_input_tokens) AS input_tokens,
                       SUM(actual_output_tokens) AS output_tokens
                FROM enrichment_batches
                WHERE started_at > NOW() - INTERVAL '2 hours'
                GROUP BY status
                """
            )
        )
        report["stage_4_enrichment_batches"] = [dict(r) for r in batch_stats.mappings()]

        enriched_sample = await db.execute(
            text(
                f"""
                SELECT c.board_token, nj.title, nj.seniority, nj.is_internship,
                       nj.remote_type, nj.normalized_roles, nj.job_capabilities,
                       nj.application_effort, nj.retrieval_pools, nj.opportunity_score,
                       nj.salary_min, nj.salary_max
                FROM normalized_jobs nj
                JOIN companies c ON c.id = nj.company_id
                WHERE c.board_token IN ({tokens_sql})
                  AND nj.opportunity_score IS NOT NULL
                ORDER BY nj.opportunity_score DESC
                LIMIT 6
                """
            )
        )
        report["stage_5_enriched_sample_top_scores"] = [dict(r) for r in enriched_sample.mappings()]

        pools = await db.execute(
            text(
                f"""
                SELECT pool, COUNT(*) AS jobs
                FROM (
                    SELECT unnest(nj.retrieval_pools) AS pool
                    FROM normalized_jobs nj
                    JOIN companies c ON c.id = nj.company_id
                    WHERE c.board_token IN ({tokens_sql})
                ) sub
                GROUP BY pool ORDER BY jobs DESC
                """
            )
        )
        report["stage_5_retrieval_pools"] = [dict(r) for r in pools.mappings()]

        effort = await db.execute(
            text(
                f"""
                SELECT application_effort, COUNT(*)
                FROM normalized_jobs nj
                JOIN companies c ON c.id = nj.company_id
                WHERE c.board_token IN ({tokens_sql})
                GROUP BY application_effort
                """
            )
        )
        report["stage_5_application_effort"] = dict(effort.all())

    # Recommendation stage
    for key in list(sys.modules):
        if key == "app" or key.startswith("app."):
            del sys.modules[key]
    sys.path.insert(0, str(ROOT / "recommendation_service"))

    from app.database import AsyncSessionLocal as RecoSession
    from app.models.subscription import UserPoolSubscription
    from app.notification.retrieval import query_jobs_in_pools
    from app.services.subscriptions import get_active_pools
    from sqlalchemy import select

    import uuid

    candidate_id = uuid.UUID(CANDIDATE_ID)
    top_pools = [p["pool"] for p in report["stage_5_retrieval_pools"][:3]]

    async with RecoSession() as db:
        for pool in top_pools:
            existing = await db.scalar(
                select(UserPoolSubscription).where(
                    UserPoolSubscription.candidate_id == candidate_id,
                    UserPoolSubscription.pool_name == pool,
                )
            )
            if not existing:
                db.add(
                    UserPoolSubscription(
                        candidate_id=candidate_id,
                        pool_name=pool,
                        is_active=True,
                    )
                )
        await db.commit()

        pools = await get_active_pools(db, candidate_id)
        jobs = await query_jobs_in_pools(db, pools=pools, filters=[], limit=5, offset=0)
        report["stage_6_recommendation"] = {
            "candidate_id": CANDIDATE_ID,
            "subscribed_pools": pools,
            "dashboard_top_5": [
                {
                    "title": j.title,
                    "company": j.company_name,
                    "pools": j.retrieval_pools,
                    "opportunity_score": j.opportunity_score,
                    "application_effort": j.application_effort,
                }
                for j in jobs
            ],
        }

    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
