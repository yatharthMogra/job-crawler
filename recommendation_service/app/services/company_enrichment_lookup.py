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
        from app.models.shared import Company, CompanyEnrichment
    except ImportError:
        return {}

    try:
        companies = await db.scalars(select(Company).where(Company.id.in_(company_ids)))
        companies_by_id = {row.id: row for row in companies.all()}

        enrichments = await db.scalars(
            select(CompanyEnrichment).where(CompanyEnrichment.company_id.in_(company_ids))
        )
        enrichments_by_id = {row.company_id: row for row in enrichments.all()}
    except ProgrammingError as exc:
        if _is_missing_company_enrichment_table(exc):
            return {}
        raise

    lookup: dict[uuid.UUID, CompanyEnrichmentOut] = {}
    for company_id in company_ids:
        company = companies_by_id.get(company_id)
        enrichment = enrichments_by_id.get(company_id)
        if company is None and enrichment is None:
            continue
        lookup[company_id] = CompanyEnrichmentOut(
            founded_year=enrichment.founded_year if enrichment else None,
            headquarters=enrichment.headquarters if enrichment else None,
            employee_count_range=enrichment.employee_count_range if enrichment else None,
            one_line_description=enrichment.one_line_description if enrichment else None,
            website=enrichment.website if enrichment else None,
            linkedin_url=enrichment.linkedin_url if enrichment else None,
            glassdoor_rating=float(enrichment.glassdoor_rating)
            if enrichment and enrichment.glassdoor_rating is not None
            else None,
            logo_url=company.logo_url if company else None,
        )
    return lookup


def _is_missing_company_enrichment_table(exc: ProgrammingError) -> bool:
    orig = getattr(exc, "orig", None)
    if orig is not None and orig.__class__.__name__ == "UndefinedTableError":
        return True
    message = str(exc).lower()
    return "company_enrichments" in message and "does not exist" in message
