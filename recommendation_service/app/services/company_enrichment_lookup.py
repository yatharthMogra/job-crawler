from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.dashboard import CompanyEnrichmentOut


async def load_company_enrichment_lookup(
    db: AsyncSession,
    company_ids: set[uuid.UUID],
) -> dict[uuid.UUID, CompanyEnrichmentOut]:
    if not company_ids:
        return {}

    try:
        from app.models.shared import CompanyEnrichment
    except ImportError:
        return {}

    try:
        rows = await db.scalars(
            select(CompanyEnrichment).where(CompanyEnrichment.company_id.in_(company_ids))
        )
    except ProgrammingError as exc:
        if _is_missing_company_enrichment_table(exc):
            return {}
        raise

    lookup: dict[uuid.UUID, CompanyEnrichmentOut] = {}
    for row in rows.all():
        lookup[row.company_id] = CompanyEnrichmentOut(
            founded_year=row.founded_year,
            headquarters=row.headquarters,
            employee_count_range=row.employee_count_range,
            one_line_description=row.one_line_description,
            website=row.website,
            linkedin_url=row.linkedin_url,
            glassdoor_rating=float(row.glassdoor_rating) if row.glassdoor_rating is not None else None,
        )
    return lookup


def _is_missing_company_enrichment_table(exc: ProgrammingError) -> bool:
    orig = getattr(exc, "orig", None)
    if orig is not None and orig.__class__.__name__ == "UndefinedTableError":
        return True
    message = str(exc).lower()
    return "company_enrichments" in message and "does not exist" in message
