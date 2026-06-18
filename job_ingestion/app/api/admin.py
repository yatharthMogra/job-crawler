from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
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
from app.services.taxonomy_health_ack import list_acknowledged_domains, set_domain_acknowledged

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
    domain_stats,
    titles_by_domain: dict[str, list[NoPoolTitleOut]],
    acknowledgements: dict[str, str],
) -> TaxonomyHealthOut:
    total_enriched = sum(row.total for row in domain_stats)
    total_no_pool = sum(row.no_pool for row in domain_stats)

    domains: list[DomainTaxonomyHealthOut] = []
    for row in domain_stats:
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
        domains_flagged=sum(1 for d in domains if d.flagged),
        domains_needing_review=sum(1 for d in domains if d.needs_review),
        domains=domains,
    )


async def _fetch_taxonomy_stats(db: AsyncSession):
    domain_result = await db.execute(_DOMAIN_STATS_SQL)
    domain_stats = domain_result.fetchall()

    titles_result = await db.execute(_TOP_TITLES_SQL)
    all_titles = titles_result.fetchall()

    titles_by_domain: dict[str, list[NoPoolTitleOut]] = {}
    for row in all_titles:
        bucket = titles_by_domain.setdefault(row.domain, [])
        if len(bucket) < TOP_TITLES_LIMIT:
            bucket.append(NoPoolTitleOut(title=row.title, count=row.cnt))
    return domain_stats, titles_by_domain


@router.get("/taxonomy-health", response_model=TaxonomyHealthOut)
async def get_taxonomy_health(db: AsyncSession = Depends(get_db)) -> TaxonomyHealthOut:
    domain_stats, titles_by_domain = await _fetch_taxonomy_stats(db)
    return _build_taxonomy_health(domain_stats, titles_by_domain, list_acknowledged_domains())


@router.patch("/taxonomy-health/domains/{domain}/acknowledge", response_model=TaxonomyHealthOut)
async def acknowledge_taxonomy_domain(
    domain: str,
    body: TaxonomyHealthAckIn,
    db: AsyncSession = Depends(get_db),
) -> TaxonomyHealthOut:
    acknowledgements = set_domain_acknowledged(domain, acknowledged=body.acknowledged)
    domain_stats, titles_by_domain = await _fetch_taxonomy_stats(db)
    return _build_taxonomy_health(domain_stats, titles_by_domain, acknowledgements)


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
