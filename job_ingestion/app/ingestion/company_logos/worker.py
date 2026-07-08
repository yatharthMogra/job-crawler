from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Optional

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.company_logos.domain import logo_source_urls, resolve_logo_domain
from app.ingestion.company_logos.normalize import normalize_logo_image
from app.models.company import Company
from app.models.company_enrichment import CompanyEnrichment
from app.storage import get_company_logo_storage


async def fetch_logo_bytes(client: httpx.AsyncClient, domain: str) -> bytes | None:
    for url in logo_source_urls(domain):
        try:
            response = await client.get(url, follow_redirects=True, timeout=15.0)
            if response.status_code != 200:
                continue
            normalized = normalize_logo_image(response.content)
            if normalized:
                return normalized
        except Exception:
            continue
    return None


async def fetch_and_store_company_logo(
    db: AsyncSession,
    company: Company,
    *,
    enrichment_website: str | None = None,
    client: httpx.AsyncClient | None = None,
) -> str:
    """Fetch, normalize, and store a company logo. Returns logo_status."""
    domain = resolve_logo_domain(company, enrichment_website=enrichment_website)
    storage = get_company_logo_storage()
    owns_client = client is None
    http = client or httpx.AsyncClient(headers={"User-Agent": "JobCrawler/1.0"})

    try:
        content = await fetch_logo_bytes(http, domain)
        now = datetime.now(timezone.utc)
        company.logo_domain = domain
        company.logo_fetched_at = now

        if content is None:
            company.logo_status = "missing"
            company.logo_url = None
            return "missing"

        company.logo_url = storage.save(company.board_token, content)
        company.logo_status = "found"
        return "found"
    except Exception:
        company.logo_status = "failed"
        company.logo_fetched_at = datetime.now(timezone.utc)
        return "failed"
    finally:
        if owns_client:
            await http.aclose()


async def load_enrichment_websites(
    db: AsyncSession,
    company_ids: list,
) -> dict:
    if not company_ids:
        return {}
    rows = await db.scalars(
        select(CompanyEnrichment).where(CompanyEnrichment.company_id.in_(company_ids))
    )
    return {row.company_id: row.website for row in rows.all() if row.website}


async def run_company_logo_batch(
    db: AsyncSession,
    *,
    limit: int = 100,
    pending_only: bool = True,
    board_token: str | None = None,
) -> dict[str, int]:
    stmt = select(Company).order_by(Company.name)
    if board_token:
        stmt = stmt.where(Company.board_token == board_token)
    elif pending_only:
        stmt = stmt.where(Company.logo_status.in_(("pending", "failed")))
    stmt = stmt.limit(limit)

    companies = (await db.scalars(stmt)).all()
    if not companies:
        return {"processed": 0, "found": 0, "missing": 0, "failed": 0}

    websites = await load_enrichment_websites(db, [c.id for c in companies])
    counts = {"processed": 0, "found": 0, "missing": 0, "failed": 0}

    async with httpx.AsyncClient(headers={"User-Agent": "JobCrawler/1.0"}) as client:
        for company in companies:
            status = await fetch_and_store_company_logo(
                db,
                company,
                enrichment_website=websites.get(company.id),
                client=client,
            )
            counts["processed"] += 1
            counts[status] += 1
            await asyncio.sleep(0.2)

    await db.commit()
    return counts
