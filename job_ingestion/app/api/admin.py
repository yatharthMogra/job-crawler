from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.admin import (
    NO_POOL_THRESHOLD_PCT,
    TOP_TITLES_LIMIT,
    DomainTaxonomyHealthOut,
    NoPoolTitleOut,
    TaxonomyHealthOut,
)

router = APIRouter(prefix="/admin", tags=["admin"])

_DOMAIN_STATS_SQL = text(
    """
    SELECT
        COALESCE(job_domain, '(none)') AS domain,
        COUNT(*)                        AS total,
        COUNT(*) FILTER (
            WHERE cardinality(retrieval_pools) = 0
        )                               AS no_pool
    FROM normalized_jobs
    WHERE is_active = TRUE
      AND processing_state IN ('success', 'partial_success')
    GROUP BY job_domain
    ORDER BY no_pool DESC
    """
)

_TOP_TITLES_SQL = text(
    """
    SELECT
        COALESCE(job_domain, '(none)') AS domain,
        title,
        COUNT(*)                        AS cnt
    FROM normalized_jobs
    WHERE is_active = TRUE
      AND processing_state IN ('success', 'partial_success')
      AND cardinality(retrieval_pools) = 0
      AND title IS NOT NULL
    GROUP BY job_domain, title
    ORDER BY job_domain, cnt DESC
    """
)


@router.get("/taxonomy-health", response_model=TaxonomyHealthOut)
async def get_taxonomy_health(db: AsyncSession = Depends(get_db)) -> TaxonomyHealthOut:
    domain_result = await db.execute(_DOMAIN_STATS_SQL)
    domain_stats = domain_result.fetchall()

    titles_result = await db.execute(_TOP_TITLES_SQL)
    all_titles = titles_result.fetchall()

    titles_by_domain: dict[str, list[NoPoolTitleOut]] = {}
    for row in all_titles:
        bucket = titles_by_domain.setdefault(row.domain, [])
        if len(bucket) < TOP_TITLES_LIMIT:
            bucket.append(NoPoolTitleOut(title=row.title, count=row.cnt))

    total_enriched = sum(row.total for row in domain_stats)
    total_no_pool = sum(row.no_pool for row in domain_stats)

    domains: list[DomainTaxonomyHealthOut] = []
    for row in domain_stats:
        no_pool_pct = round(100.0 * row.no_pool / row.total, 1) if row.total else 0.0
        domains.append(
            DomainTaxonomyHealthOut(
                domain=row.domain,
                total=row.total,
                no_pool=row.no_pool,
                no_pool_pct=no_pool_pct,
                flagged=no_pool_pct >= NO_POOL_THRESHOLD_PCT,
                top_no_pool_titles=titles_by_domain.get(row.domain, []),
            )
        )

    global_no_pool_pct = (
        round(100.0 * total_no_pool / total_enriched, 1) if total_enriched else 0.0
    )

    return TaxonomyHealthOut(
        generated_at=datetime.now(timezone.utc),
        total_active_enriched=total_enriched,
        global_no_pool_count=total_no_pool,
        global_no_pool_pct=global_no_pool_pct,
        domains=domains,
    )
