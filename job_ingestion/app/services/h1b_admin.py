from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.h1b.rebuild_summary import rebuild_summary_for_company
from app.models.company import Company
from app.models.h1b import (
    H1bCompanyPoolSummary,
    H1bEmployer,
    H1bEmployerAlias,
    LcaRaw,
)

_REVIEW_LCA_THRESHOLD = 50
_COVERAGE_THRESHOLD_PCT = 50.0


async def get_h1b_stats(db: AsyncSession) -> dict:
    employer_counts = await db.execute(
        select(
            func.count().label("total"),
            func.count().filter(H1bEmployer.company_id.isnot(None)).label("matched"),
        ).select_from(H1bEmployer)
    )
    emp_row = employer_counts.one()

    lca_by_year = await db.execute(
        select(LcaRaw.fiscal_year, func.count())
        .group_by(LcaRaw.fiscal_year)
        .order_by(LcaRaw.fiscal_year.desc())
    )
    lca_rows_by_year = [
        {"fiscal_year": fy, "count": count} for fy, count in lca_by_year.all()
    ]

    total_employers = int(emp_row.total or 0)
    matched_employers = int(emp_row.matched or 0)
    match_rate_pct = round(100.0 * matched_employers / total_employers, 1) if total_employers else 0.0

    return {
        "generated_at": datetime.now(timezone.utc),
        "total_employers": total_employers,
        "matched_employers": matched_employers,
        "unmatched_employers": total_employers - matched_employers,
        "match_rate_pct": match_rate_pct,
        "lca_rows_by_year": lca_rows_by_year,
        "total_lca_rows": sum(row["count"] for row in lca_rows_by_year),
    }


async def get_h1b_review_queue(db: AsyncSession) -> list[dict]:
    volume_subq = (
        select(
            H1bEmployerAlias.employer_name_norm,
            func.count().label("lca_volume"),
        )
        .join(LcaRaw, LcaRaw.employer_name_raw == H1bEmployerAlias.employer_name_raw)
        .where(LcaRaw.case_status.ilike("certified"))
        .group_by(H1bEmployerAlias.employer_name_norm)
        .subquery()
    )

    rows = await db.execute(
        select(
            H1bEmployer.id,
            H1bEmployer.employer_name_norm,
            H1bEmployer.match_method,
            H1bEmployer.match_confidence,
            volume_subq.c.lca_volume,
        )
        .join(volume_subq, volume_subq.c.employer_name_norm == H1bEmployer.employer_name_norm)
        .where(
            H1bEmployer.match_method.in_(("unmatched", "fuzzy_candidate")),
            H1bEmployer.company_id.is_(None),
            volume_subq.c.lca_volume > _REVIEW_LCA_THRESHOLD,
        )
        .order_by(volume_subq.c.lca_volume.desc())
    )

    return [
        {
            "id": row.id,
            "employer_name_norm": row.employer_name_norm,
            "match_method": row.match_method,
            "match_confidence": float(row.match_confidence) if row.match_confidence else None,
            "total_lca": int(row.lca_volume or 0),
        }
        for row in rows.all()
    ]


async def get_h1b_coverage(db: AsyncSession) -> list[dict]:
    tracked = await db.scalar(select(func.count()).select_from(Company).where(Company.is_active.is_(True)))
    tracked = int(tracked or 0)

    pool_rows = await db.execute(
        select(
            H1bCompanyPoolSummary.pool_family,
            func.count(func.distinct(H1bCompanyPoolSummary.company_id)).label("with_data"),
        ).group_by(H1bCompanyPoolSummary.pool_family)
    )

    coverage = []
    for pool_family, with_data in pool_rows.all():
        with_data = int(with_data or 0)
        coverage_pct = round(100.0 * with_data / tracked, 1) if tracked else 0.0
        coverage.append(
            {
                "pool_family": pool_family,
                "tracked_companies": tracked,
                "companies_with_data": with_data,
                "coverage_pct": coverage_pct,
                "flagged": coverage_pct < _COVERAGE_THRESHOLD_PCT,
            }
        )

    coverage.sort(key=lambda row: row["coverage_pct"])
    return coverage


async def link_h1b_employer(
    db: AsyncSession,
    employer_id: int,
    company_id: uuid.UUID,
) -> H1bEmployer:
    employer = await db.get(H1bEmployer, employer_id)
    if employer is None:
        raise ValueError("Employer not found")

    company = await db.get(Company, company_id)
    if company is None:
        raise ValueError("Company not found")

    employer.company_id = company_id
    employer.match_method = "manual"
    employer.match_confidence = 1.0
    employer.reviewed_at = datetime.now(timezone.utc)

    await db.execute(
        text(
            """
            UPDATE h1b_lca_stats SET company_id = :company_id
            WHERE employer_name_norm = :norm
            """
        ),
        {"company_id": company_id, "norm": employer.employer_name_norm},
    )
    await db.execute(
        text(
            """
            UPDATE h1b_uscis_stats SET company_id = :company_id
            WHERE employer_name_norm = :norm
            """
        ),
        {"company_id": company_id, "norm": employer.employer_name_norm},
    )
    await db.commit()

    await rebuild_summary_for_company(db, company_id)
    await db.refresh(employer)
    return employer
