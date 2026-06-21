from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.ingestion.company_enrichment.fetcher import fetch_company_about_text
from app.ingestion.company_enrichment.llm import (
    COMPANY_ENRICHMENT_SYSTEM_PROMPT,
    CompanyEnrichmentResult,
)
from app.ingestion.company_enrichment.resolver import resolve_company_website
from app.llm.factory import get_llm_provider
from app.models.company import Company
from app.models.company_enrichment import CompanyEnrichment
from app.models.normalized_job import NormalizedJob

COMPANY_ENRICHMENT_VERSION = "v1"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


async def enrich_company(
    db: AsyncSession,
    company: Company,
    *,
    settings: Settings | None = None,
    posting_url: str | None = None,
) -> CompanyEnrichmentResult | None:
    settings = settings or get_settings()
    website = resolve_company_website(company, posting_url=posting_url)
    if website is None:
        return None

    about_text = await fetch_company_about_text(website)
    if not about_text:
        return None

    provider = get_llm_provider(settings)
    user_prompt = (
        f"Company name: {company.name}\n"
        f"Known website: {website}\n\n"
        f"About page text:\n{about_text}"
    )
    result = await provider.complete(
        COMPANY_ENRICHMENT_SYSTEM_PROMPT,
        user_prompt,
        CompanyEnrichmentResult,
    )
    enrichment = result.output
    if enrichment.website is None:
        enrichment = enrichment.model_copy(update={"website": website})

    now = _utcnow()
    values = {
        "company_id": company.id,
        "founded_year": enrichment.founded_year,
        "headquarters": enrichment.headquarters,
        "employee_count_range": enrichment.employee_count_range,
        "one_line_description": enrichment.one_line_description,
        "website": enrichment.website,
        "linkedin_url": enrichment.linkedin_url,
        "glassdoor_rating": enrichment.glassdoor_rating,
        "llm_provider": settings.llm_provider,
        "llm_model": settings.gemini_model if settings.llm_provider == "gemini" else None,
        "extraction_version": COMPANY_ENRICHMENT_VERSION,
        "last_enriched_at": now,
        "updated_at": now,
    }
    stmt = (
        pg_insert(CompanyEnrichment)
        .values(**values)
        .on_conflict_do_update(index_elements=["company_id"], set_=values)
    )
    await db.execute(stmt)
    return enrichment


async def select_companies_for_enrichment(
    db: AsyncSession,
    *,
    refresh_days: int,
    batch_size: int,
) -> list[tuple[Company, Optional[str]]]:
    cutoff = _utcnow() - timedelta(days=max(1, refresh_days))
    stmt = (
        select(Company, func.max(NormalizedJob.posting_url))
        .outerjoin(CompanyEnrichment, CompanyEnrichment.company_id == Company.id)
        .outerjoin(
            NormalizedJob,
            (NormalizedJob.company_id == Company.id) & NormalizedJob.is_active.is_(True),
        )
        .where(
            Company.is_active.is_(True),
            (CompanyEnrichment.last_enriched_at.is_(None) | (CompanyEnrichment.last_enriched_at < cutoff)),
        )
        .group_by(Company.id)
        .order_by(func.count(NormalizedJob.id).desc().nullslast())
        .limit(batch_size)
    )
    rows = (await db.execute(stmt)).all()
    return [(company, posting_url) for company, posting_url in rows]


async def run_company_enrichment_batch(
    db: AsyncSession,
    *,
    settings: Settings | None = None,
    batch_size: int | None = None,
) -> dict[str, int]:
    settings = settings or get_settings()
    batch_size = batch_size or settings.company_enrichment_batch_size
    companies = await select_companies_for_enrichment(
        db,
        refresh_days=settings.company_enrichment_refresh_days,
        batch_size=batch_size,
    )
    enriched = 0
    skipped = 0
    for company, posting_url in companies:
        result = await enrich_company(db, company, settings=settings, posting_url=posting_url)
        if result is None:
            skipped += 1
        else:
            enriched += 1
    await db.commit()
    return {"selected": len(companies), "enriched": enriched, "skipped": skipped}


async def enrich_company_by_id(
    db: AsyncSession,
    company_id: uuid.UUID,
    *,
    settings: Settings | None = None,
) -> CompanyEnrichmentResult | None:
    settings = settings or get_settings()
    company = await db.get(Company, company_id)
    if company is None:
        return None
    posting_url = await db.scalar(
        select(NormalizedJob.posting_url)
        .where(NormalizedJob.company_id == company_id, NormalizedJob.is_active.is_(True))
        .order_by(NormalizedJob.last_seen_at.desc())
        .limit(1)
    )
    result = await enrich_company(db, company, settings=settings, posting_url=posting_url)
    await db.commit()
    return result
