from __future__ import annotations

import uuid
from dataclasses import dataclass

import structlog
from sqlalchemy import select
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shared import H1bCompanyPoolSummary

log = structlog.get_logger(__name__)


@dataclass(frozen=True)
class H1bSummaryRow:
    pool_family: str
    total_lca_3yr: int
    approval_rate_3yr: float | None
    is_top_sponsor: bool
    years_covered: list[int]


H1bLookup = dict[tuple[uuid.UUID, str], H1bSummaryRow]


async def load_h1b_summary_lookup(
    db: AsyncSession,
    company_ids: set[uuid.UUID],
) -> H1bLookup:
    if not company_ids:
        return {}

    try:
        rows = await db.scalars(
            select(H1bCompanyPoolSummary).where(
                H1bCompanyPoolSummary.company_id.in_(company_ids)
            )
        )
    except ProgrammingError as exc:
        if _is_missing_h1b_table(exc):
            log.warning(
                "h1b_summary_table_missing",
                detail="h1b_company_pool_summary not found; skipping sponsorship lookup",
            )
            return {}
        raise

    lookup: H1bLookup = {}
    for row in rows.all():
        lookup[(row.company_id, row.pool_family)] = H1bSummaryRow(
            pool_family=row.pool_family,
            total_lca_3yr=row.total_lca_3yr or 0,
            approval_rate_3yr=float(row.approval_rate_3yr) if row.approval_rate_3yr is not None else None,
            is_top_sponsor=bool(row.is_top_sponsor),
            years_covered=list(row.years_covered or []),
        )
    return lookup


def _is_missing_h1b_table(exc: ProgrammingError) -> bool:
    orig = getattr(exc, "orig", None)
    if orig is not None and orig.__class__.__name__ == "UndefinedTableError":
        return True
    message = str(exc).lower()
    return "h1b_company_pool_summary" in message and "does not exist" in message
