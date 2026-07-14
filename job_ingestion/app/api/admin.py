from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.ingestion.h1b.pipeline import run_h1b_ingestion
from app.schemas.admin import (
    NO_POOL_THRESHOLD_PCT,
    TOP_TITLES_LIMIT,
    DomainTaxonomyHealthOut,
    H1bCoverageOut,
    H1bCoverageItemOut,
    H1bEmployerLinkIn,
    H1bEmployerOut,
    H1bIngestResultOut,
    H1bLcaYearOut,
    H1bReviewQueueItemOut,
    H1bReviewQueueOut,
    H1bStatsOut,
    NoPoolTitleOut,
    TaxonomyHealthAckIn,
    TaxonomyHealthOut,
)
from app.services.h1b_admin import (
    get_h1b_coverage,
    get_h1b_review_queue,
    get_h1b_stats,
    link_h1b_employer,
)
from app.services.taxonomy_health_ack import (
    list_acknowledgements,
    set_domain_acknowledged,
    set_group_acknowledged,
)

router = APIRouter(prefix="/admin", tags=["admin"])

GroupBy = Literal["domain", "role"]

_JOB_LEVEL_GLOBALS_SQL = text(
    """
    SELECT
        COUNT(*) AS total,
        COUNT(*) FILTER (WHERE cardinality(retrieval_pools) = 0) AS no_pool
    FROM normalized_jobs
    WHERE is_active = TRUE
      AND processing_state IN ('success', 'partial_success')
    """
)

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

_DOMAIN_TOP_TITLES_SQL = text(
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

# One job can contribute to multiple role rows when it has multiple normalized_roles.
_ROLE_STATS_SQL = text(
    """
    SELECT
        roles.role AS domain,
        COUNT(*)   AS total,
        COUNT(*) FILTER (
            WHERE cardinality(nj.retrieval_pools) = 0
        )          AS no_pool
    FROM normalized_jobs nj
    CROSS JOIN LATERAL (
        SELECT COALESCE(r, '(none)') AS role
        FROM unnest(
            CASE
                WHEN nj.normalized_roles IS NULL OR cardinality(nj.normalized_roles) = 0
                THEN ARRAY[NULL]::text[]
                ELSE nj.normalized_roles::text[]
            END
        ) AS r
    ) roles
    WHERE nj.is_active = TRUE
      AND nj.processing_state IN ('success', 'partial_success')
    GROUP BY roles.role
    ORDER BY no_pool DESC
    """
)

_ROLE_TOP_TITLES_SQL = text(
    """
    SELECT
        roles.role AS domain,
        nj.title,
        COUNT(*)   AS cnt
    FROM normalized_jobs nj
    CROSS JOIN LATERAL (
        SELECT COALESCE(r, '(none)') AS role
        FROM unnest(
            CASE
                WHEN nj.normalized_roles IS NULL OR cardinality(nj.normalized_roles) = 0
                THEN ARRAY[NULL]::text[]
                ELSE nj.normalized_roles::text[]
            END
        ) AS r
    ) roles
    WHERE nj.is_active = TRUE
      AND nj.processing_state IN ('success', 'partial_success')
      AND cardinality(nj.retrieval_pools) = 0
      AND nj.title IS NOT NULL
    GROUP BY roles.role, nj.title
    ORDER BY roles.role, cnt DESC
    """
)


def _parse_ack_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def _build_taxonomy_health(
    group_stats,
    titles_by_group: dict[str, list[NoPoolTitleOut]],
    acknowledgements: dict[str, str],
    *,
    group_by: GroupBy,
    total_active_enriched: int,
    global_no_pool_count: int,
) -> TaxonomyHealthOut:
    domains: list[DomainTaxonomyHealthOut] = []
    for row in group_stats:
        no_pool_pct = round(100.0 * row.no_pool / row.total, 1) if row.total else 0.0
        flagged = no_pool_pct >= NO_POOL_THRESHOLD_PCT
        ack_raw = acknowledgements.get(row.domain)
        acknowledged = ack_raw is not None
        acknowledged_at = _parse_ack_timestamp(ack_raw)
        needs_review = flagged and not acknowledged
        domains.append(
            DomainTaxonomyHealthOut(
                domain=row.domain,
                total=row.total,
                no_pool=row.no_pool,
                no_pool_pct=no_pool_pct,
                flagged=flagged,
                acknowledged=acknowledged,
                acknowledged_at=acknowledged_at,
                needs_review=needs_review,
                top_no_pool_titles=titles_by_group.get(row.domain, []),
            )
        )

    global_no_pool_pct = (
        round(100.0 * global_no_pool_count / total_active_enriched, 1) if total_active_enriched else 0.0
    )

    return TaxonomyHealthOut(
        generated_at=datetime.now(timezone.utc),
        group_by=group_by,
        total_active_enriched=total_active_enriched,
        global_no_pool_count=global_no_pool_count,
        global_no_pool_pct=global_no_pool_pct,
        domains_flagged=sum(1 for d in domains if d.flagged),
        domains_needing_review=sum(1 for d in domains if d.needs_review),
        domains=domains,
    )


async def _fetch_taxonomy_stats(db: AsyncSession, group_by: GroupBy):
    globals_row = (await db.execute(_JOB_LEVEL_GLOBALS_SQL)).one()
    total_active_enriched = int(globals_row.total or 0)
    global_no_pool_count = int(globals_row.no_pool or 0)

    stats_sql = _ROLE_STATS_SQL if group_by == "role" else _DOMAIN_STATS_SQL
    titles_sql = _ROLE_TOP_TITLES_SQL if group_by == "role" else _DOMAIN_TOP_TITLES_SQL

    group_stats = (await db.execute(stats_sql)).fetchall()
    all_titles = (await db.execute(titles_sql)).fetchall()

    titles_by_group: dict[str, list[NoPoolTitleOut]] = {}
    for row in all_titles:
        bucket = titles_by_group.setdefault(row.domain, [])
        if len(bucket) < TOP_TITLES_LIMIT:
            bucket.append(NoPoolTitleOut(title=row.title, count=row.cnt))
    return group_stats, titles_by_group, total_active_enriched, global_no_pool_count


@router.get("/taxonomy-health", response_model=TaxonomyHealthOut)
async def get_taxonomy_health(
    group_by: GroupBy = Query(default="domain"),
    db: AsyncSession = Depends(get_db),
) -> TaxonomyHealthOut:
    group_stats, titles_by_group, total_active, global_no_pool = await _fetch_taxonomy_stats(
        db, group_by
    )
    return _build_taxonomy_health(
        group_stats,
        titles_by_group,
        list_acknowledgements(group_by),
        group_by=group_by,
        total_active_enriched=total_active,
        global_no_pool_count=global_no_pool,
    )


@router.patch("/taxonomy-health/domains/{domain}/acknowledge", response_model=TaxonomyHealthOut)
async def acknowledge_taxonomy_domain(
    domain: str,
    body: TaxonomyHealthAckIn,
    group_by: GroupBy = Query(default="domain"),
    db: AsyncSession = Depends(get_db),
) -> TaxonomyHealthOut:
    if group_by == "role":
        acknowledgements = set_group_acknowledged("role", domain, acknowledged=body.acknowledged)
    else:
        acknowledgements = set_domain_acknowledged(domain, acknowledged=body.acknowledged)
    group_stats, titles_by_group, total_active, global_no_pool = await _fetch_taxonomy_stats(
        db, group_by
    )
    return _build_taxonomy_health(
        group_stats,
        titles_by_group,
        acknowledgements,
        group_by=group_by,
        total_active_enriched=total_active,
        global_no_pool_count=global_no_pool,
    )


@router.get("/h1b-stats", response_model=H1bStatsOut)
async def h1b_stats(db: AsyncSession = Depends(get_db)) -> H1bStatsOut:
    stats = await get_h1b_stats(db)
    return H1bStatsOut(
        generated_at=stats["generated_at"],
        total_employers=stats["total_employers"],
        matched_employers=stats["matched_employers"],
        unmatched_employers=stats["unmatched_employers"],
        match_rate_pct=stats["match_rate_pct"],
        lca_rows_by_year=[H1bLcaYearOut(**row) for row in stats["lca_rows_by_year"]],
        total_lca_rows=stats["total_lca_rows"],
    )


@router.get("/h1b-review-queue", response_model=H1bReviewQueueOut)
async def h1b_review_queue(db: AsyncSession = Depends(get_db)) -> H1bReviewQueueOut:
    items = await get_h1b_review_queue(db)
    return H1bReviewQueueOut(
        items=[H1bReviewQueueItemOut(**item) for item in items],
    )


@router.get("/h1b-coverage", response_model=H1bCoverageOut)
async def h1b_coverage(db: AsyncSession = Depends(get_db)) -> H1bCoverageOut:
    items = await get_h1b_coverage(db)
    return H1bCoverageOut(items=[H1bCoverageItemOut(**item) for item in items])


@router.patch("/h1b-employer/{employer_id}", response_model=H1bEmployerOut)
async def patch_h1b_employer(
    employer_id: int,
    body: H1bEmployerLinkIn,
    db: AsyncSession = Depends(get_db),
) -> H1bEmployerOut:
    try:
        employer = await link_h1b_employer(db, employer_id, body.company_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return H1bEmployerOut.model_validate(employer)


@router.post("/h1b-ingest", response_model=H1bIngestResultOut)
async def trigger_h1b_ingest(db: AsyncSession = Depends(get_db)) -> H1bIngestResultOut:
    """Re-run normalization, aggregation, and summary rebuild (skip raw load)."""
    results = await run_h1b_ingestion(db, skip_load=True)
    return H1bIngestResultOut(status="completed", results=results)
