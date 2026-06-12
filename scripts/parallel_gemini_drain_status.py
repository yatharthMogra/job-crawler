#!/usr/bin/env python3
"""Print enrichment drain status for parallel workers."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JOB_INGESTION = ROOT / "job_ingestion"
sys.path.insert(0, str(JOB_INGESTION))

from sqlalchemy import text

from app.database import AsyncSessionLocal


async def main() -> None:
    async with AsyncSessionLocal() as db:
        jobs = (
            await db.execute(
                text(
                    """
                    SELECT
                      COUNT(*) FILTER (WHERE is_active AND job_domain IS NOT NULL) AS with_domain,
                      COUNT(*) FILTER (WHERE is_active) AS active,
                      COUNT(*) FILTER (WHERE is_active AND extraction_version = 'v5') AS on_v5
                    FROM normalized_jobs
                    """
                )
            )
        ).one()
        queue = (
            await db.execute(
                text(
                    """
                    SELECT status, COALESCE(last_failure_reason, ''), COUNT(*)::int
                    FROM enrichment_queue
                    GROUP BY 1, 2
                    ORDER BY 3 DESC
                    """
                )
            )
        ).all()
        completed_recent = await db.scalar(
            text(
                """
                SELECT COUNT(*)::int FROM enrichment_queue
                WHERE status = 'completed'
                  AND updated_at > NOW() - INTERVAL '5 minutes'
                """
            )
        )
        last_completed = await db.scalar(
            text("SELECT MAX(updated_at) FROM enrichment_queue WHERE status = 'completed'")
        )
        errors = (
            await db.execute(
                text(
                    """
                    SELECT LEFT(COALESCE(last_error, last_failure_reason), 100), COUNT(*)::int
                    FROM enrichment_queue
                    WHERE status IN ('failed', 'quota_blocked')
                    GROUP BY 1 ORDER BY 2 DESC LIMIT 5
                    """
                )
            )
        ).all()

    with_domain, active, on_v5 = jobs
    pct = 100 * with_domain / active if active else 0
    print(f"domain={with_domain}/{active} ({pct:.1f}%) v5={on_v5}")
    print(f"completed_last_5min={completed_recent} last_completion={last_completed}")
    print("queue:")
    for status, reason, count in queue:
        print(f"  {status:16} {reason:32} {count}")
    if errors:
        print("failures:")
        for err, count in errors:
            print(f"  [{count}] {err}")


if __name__ == "__main__":
    asyncio.run(main())
