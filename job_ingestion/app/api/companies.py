import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.ingestion.constants import EventCategory, EventSeverity, EventType
from app.ingestion.events import write_event
from app.ingestion.company_enrichment.worker import enrich_company_by_id
from app.models.company import Company
from app.models.normalized_job import NormalizedJob
from app.schemas.company import CompanyFlagIn, CompanyOut, CompanyPatchIn, CompanySyncOut
from app.utils.seed import seed_companies

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("", response_model=list[CompanyOut])
async def list_companies(
    include_job_counts: bool = Query(default=False),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> list[CompanyOut]:
    rows = (
        await db.scalars(select(Company).order_by(Company.name.asc()).offset(offset).limit(limit))
    ).all()
    job_counts: dict[uuid.UUID, int] = {}
    if include_job_counts and rows:
        company_ids = [row.id for row in rows]
        counts = (
            await db.execute(
                select(NormalizedJob.company_id, func.count(NormalizedJob.id))
                .where(NormalizedJob.company_id.in_(company_ids), NormalizedJob.is_active.is_(True))
                .group_by(NormalizedJob.company_id)
            )
        ).all()
        job_counts = {company_id: int(count) for company_id, count in counts}
    return [_serialize_company(row, active_jobs_count=job_counts.get(row.id)) for row in rows]


@router.get("/{company_id}", response_model=CompanyOut)
async def get_company(company_id: str, db: AsyncSession = Depends(get_db)) -> CompanyOut:
    try:
        company_uuid = uuid.UUID(company_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid company id") from exc

    row = await db.get(Company, company_uuid)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return _serialize_company(row)


@router.post("/seed", response_model=CompanySyncOut)
async def seed_companies_endpoint(db: AsyncSession = Depends(get_db)) -> CompanySyncOut:
    return await seed_companies(db)


@router.patch("/{company_id}", response_model=CompanyOut)
async def patch_company(
    company_id: str, payload: CompanyPatchIn, db: AsyncSession = Depends(get_db)
) -> CompanyOut:
    try:
        company_uuid = uuid.UUID(company_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid company id") from exc

    row = await db.get(Company, company_uuid)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    data = payload.model_dump(exclude_none=True)
    for key, value in data.items():
        setattr(row, key, value)
    await db.commit()
    await db.refresh(row)

    return _serialize_company(row)


@router.post("/{company_id}/flag", response_model=CompanyOut)
async def flag_company_for_review(
    company_id: str,
    payload: CompanyFlagIn,
    db: AsyncSession = Depends(get_db),
) -> CompanyOut:
    try:
        company_uuid = uuid.UUID(company_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid company id") from exc

    row = await db.get(Company, company_uuid)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    row.requires_review = True
    row.flagged_for_review_at = datetime.now(timezone.utc)
    await write_event(
        db=db,
        event_type=EventType.JOB_MARKED_REQUIRES_REVIEW,
        category=EventCategory.REVIEW,
        severity=EventSeverity.WARNING,
        platform=row.platform,
        company_id=row.id,
        metadata={"entity": "company", "comment": payload.comment or ""},
    )
    await db.commit()
    await db.refresh(row)
    return _serialize_company(row)


@router.post("/{company_id}/enrich")
async def enrich_company_endpoint(company_id: str, db: AsyncSession = Depends(get_db)) -> dict:
    try:
        company_uuid = uuid.UUID(company_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid company id") from exc

    row = await db.get(Company, company_uuid)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    result = await enrich_company_by_id(db, company_uuid)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Could not enrich company (missing website or about page content)",
        )
    return {
        "company_id": company_id,
        "founded_year": result.founded_year,
        "headquarters": result.headquarters,
        "employee_count_range": result.employee_count_range,
        "one_line_description": result.one_line_description,
        "website": result.website,
        "linkedin_url": result.linkedin_url,
        "glassdoor_rating": result.glassdoor_rating,
    }


def _serialize_company(row: Company, active_jobs_count: int | None = None) -> CompanyOut:
    return CompanyOut(
        id=str(row.id),
        name=row.name,
        platform=row.platform,
        board_token=row.board_token,
        platform_config=row.platform_config,
        is_active=row.is_active,
        fetch_tier=row.fetch_tier,
        requires_review=row.requires_review,
        active_jobs_count=active_jobs_count,
        consecutive_fetch_failures=row.consecutive_fetch_failures,
        last_failure_at=row.last_failure_at,
        flagged_for_review_at=row.flagged_for_review_at,
        last_successful_fetch_at=row.last_successful_fetch_at,
    )
