from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.ingestion.connectors.tesla_careers import (
    TESLA_BOARD_TOKEN,
    TESLA_COMPANY_ID,
    build_tesla_jobs_from_push,
    iter_site_listings,
    pending_tesla_detail_ids,
    resolve_tesla_careers_config,
)
from app.ingestion.pipeline import (
    CompanyRunOutcome,
    _latest_raw_by_external_id,
    process_company_raw_jobs,
)
from app.models.company import Company
from app.models.normalized_job import NormalizedJob
from app.models.pipeline_run import CompanyRunResult, PipelineRun


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


async def get_tesla_company(db: AsyncSession) -> Company | None:
    company = await db.get(Company, UUID(TESLA_COMPANY_ID))
    if company is not None:
        return company
    return await db.scalar(select(Company).where(Company.board_token == TESLA_BOARD_TOKEN))


async def get_known_external_ids(db: AsyncSession, company_id: UUID) -> list[str]:
    rows = (
        await db.scalars(
            select(NormalizedJob.external_job_id)
            .where(NormalizedJob.company_id == company_id)
            .order_by(NormalizedJob.external_job_id.asc())
        )
    ).all()
    return list(rows)


async def plan_tesla_push(
    db: AsyncSession,
    company: Company,
    state_data: dict[str, Any],
) -> dict[str, Any]:
    config = resolve_tesla_careers_config(company)
    sites = config["sites"]
    known_ids = set(await get_known_external_ids(db, company.id))
    pending_ids = pending_tesla_detail_ids(state_data, sites, known_ids)
    listing_count = len(iter_site_listings(state_data, sites))
    return {
        "sites": sites,
        "listing_count": listing_count,
        "known_count": len(known_ids),
        "pending_detail_ids": pending_ids,
    }


async def run_tesla_manual_push(
    db: AsyncSession,
    company: Company,
    state_data: dict[str, Any],
    details: list[dict[str, Any]],
    *,
    settings: Settings,
) -> tuple[CompanyRunOutcome, str]:
    config = resolve_tesla_careers_config(company)
    details_by_id: dict[str, dict[str, Any]] = {}
    for detail in details:
        if not isinstance(detail, dict):
            continue
        job_id = detail.get("id")
        if job_id is not None:
            details_by_id[str(job_id)] = detail

    previous_raw_by_id = await _latest_raw_by_external_id(db, company.id)
    raw_jobs = build_tesla_jobs_from_push(
        state_data,
        details_by_id,
        sites=config["sites"],
        previous_raw_by_id=previous_raw_by_id,
    )

    run = PipelineRun(
        run_type="manual_push",
        status="running",
        total_companies=1,
        schedule_metadata={"source": "tesla_browser_bridge", "company_id": str(company.id)},
    )
    db.add(run)
    await db.flush()

    company_started = _utcnow()
    outcome = CompanyRunOutcome(company_id=company.id, status="success")
    try:
        processed = await process_company_raw_jobs(
            db,
            company,
            raw_jobs,
            pipeline_run_id=run.id,
            settings=settings,
            enrichment_source="manual_push",
        )
        outcome.jobs_fetched = processed.jobs_fetched
        outcome.jobs_new = processed.jobs_new
        outcome.jobs_updated = processed.jobs_updated
        outcome.jobs_unchanged = processed.jobs_unchanged
        outcome.jobs_removed = processed.jobs_removed
        outcome.jobs_deduped = processed.jobs_deduped
        outcome.jobs_rejected_stale_pipeline = processed.jobs_rejected_stale_pipeline
        run.status = "completed"
        run.successful_companies = 1
        run.failed_companies = 0
    except Exception as exc:  # noqa: BLE001
        outcome.status = "failed"
        outcome.error_message = str(exc)
        run.status = "failed"
        run.successful_companies = 0
        run.failed_companies = 1
        completed_at = _utcnow()
        run.completed_at = completed_at
        db.add(
            CompanyRunResult(
                pipeline_run_id=run.id,
                company_id=company.id,
                status=outcome.status,
                jobs_fetched=outcome.jobs_fetched,
                jobs_new=outcome.jobs_new,
                jobs_updated=outcome.jobs_updated,
                jobs_unchanged=outcome.jobs_unchanged,
                jobs_removed=outcome.jobs_removed,
                error_message=outcome.error_message,
                started_at=company_started,
                completed_at=completed_at,
            )
        )
        await db.commit()
        raise exc

    completed_at = _utcnow()
    run.jobs_fetched = outcome.jobs_fetched
    run.jobs_new = outcome.jobs_new
    run.jobs_updated = outcome.jobs_updated
    run.jobs_unchanged = outcome.jobs_unchanged
    run.jobs_removed = outcome.jobs_removed
    run.completed_at = completed_at
    db.add(
        CompanyRunResult(
            pipeline_run_id=run.id,
            company_id=company.id,
            status=outcome.status,
            jobs_fetched=outcome.jobs_fetched,
            jobs_new=outcome.jobs_new,
            jobs_updated=outcome.jobs_updated,
            jobs_unchanged=outcome.jobs_unchanged,
            jobs_removed=outcome.jobs_removed,
            error_message=outcome.error_message,
            started_at=company_started,
            completed_at=completed_at,
        )
    )
    await db.commit()
    return outcome, str(run.id)
