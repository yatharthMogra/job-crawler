from __future__ import annotations

from decimal import Decimal

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.h1b.fiscal_year import current_fiscal_year
from app.models.h1b import H1bCompanyPoolSummary, H1bLcaStats, H1bUscisStats

_TOP_SPONSOR_LIMIT = 500
_LOOKBACK_YEARS = 3


async def rebuild_company_pool_summary(
    db: AsyncSession,
    *,
    company_ids: list | None = None,
) -> int:
    """Truncate and rebuild h1b_company_pool_summary."""
    if company_ids:
        for company_id in company_ids:
            await db.execute(
                delete(H1bCompanyPoolSummary).where(
                    H1bCompanyPoolSummary.company_id == company_id
                )
            )
    else:
        await db.execute(delete(H1bCompanyPoolSummary))

    latest_fy = current_fiscal_year() - 1
    window_years = list(range(latest_fy - _LOOKBACK_YEARS + 1, latest_fy + 1))

    lca_rows = await db.execute(
        select(
            H1bLcaStats.company_id,
            H1bLcaStats.pool_family,
            H1bLcaStats.fiscal_year,
            H1bLcaStats.lca_certified,
        ).where(
            H1bLcaStats.company_id.isnot(None),
            H1bLcaStats.pool_family.isnot(None),
            H1bLcaStats.fiscal_year.in_(window_years),
            *( [H1bLcaStats.company_id.in_(company_ids)] if company_ids else [] ),
        )
    )

    lca_buckets: dict[tuple, dict] = {}
    for company_id, pool_family, fy, certified in lca_rows.all():
        key = (company_id, pool_family)
        bucket = lca_buckets.setdefault(key, {"years": set(), "total_lca": 0})
        bucket["years"].add(fy)
        bucket["total_lca"] += int(certified or 0)

    uscis_rows = await db.execute(
        select(
            H1bUscisStats.company_id,
            H1bUscisStats.fiscal_year,
            H1bUscisStats.initial_approvals,
            H1bUscisStats.approval_rate,
        ).where(
            H1bUscisStats.company_id.isnot(None),
            H1bUscisStats.fiscal_year.in_(window_years),
            *( [H1bUscisStats.company_id.in_(company_ids)] if company_ids else [] ),
        )
    )

    uscis_by_company: dict = {}
    for company_id, fy, init_app, rate in uscis_rows.all():
        bucket = uscis_by_company.setdefault(company_id, {"years": set(), "total_h1b": 0, "rates": []})
        bucket["years"].add(fy)
        bucket["total_h1b"] += int(init_app or 0)
        if rate is not None:
            bucket["rates"].append(float(rate))

    summaries: list[H1bCompanyPoolSummary] = []
    for (company_id, pool_family), lca_data in lca_buckets.items():
        uscis = uscis_by_company.get(company_id, {"years": set(), "total_h1b": 0, "rates": []})
        years = sorted(lca_data["years"] | uscis["years"])
        years_available = len(years)
        lookback = min(_LOOKBACK_YEARS, years_available) if years_available else 0
        approval_rate_3yr = (
            Decimal(str(round(sum(uscis["rates"]) / len(uscis["rates"]), 4)))
            if uscis["rates"]
            else None
        )
        summaries.append(
            H1bCompanyPoolSummary(
                company_id=company_id,
                pool_family=pool_family,
                years_covered=years,
                latest_year=max(years) if years else None,
                total_lca_3yr=lca_data["total_lca"],
                total_h1b_3yr=uscis["total_h1b"],
                approval_rate_3yr=approval_rate_3yr,
                is_top_sponsor=False,
            )
        )

    by_pool: dict[str, list[H1bCompanyPoolSummary]] = {}
    for summary in summaries:
        by_pool.setdefault(summary.pool_family, []).append(summary)

    for pool_family, pool_summaries in by_pool.items():
        ranked = sorted(pool_summaries, key=lambda s: s.total_lca_3yr or 0, reverse=True)
        for summary in ranked[:_TOP_SPONSOR_LIMIT]:
            summary.is_top_sponsor = True

    for summary in summaries:
        db.add(summary)

    await db.commit()
    return len(summaries)


async def rebuild_summary_for_company(db: AsyncSession, company_id) -> int:
    return await rebuild_company_pool_summary(db, company_ids=[company_id])
