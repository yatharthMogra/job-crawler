from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.database import get_db
from app.exceptions import ParseError
from app.ingestion.tesla_push import (
    get_known_external_ids,
    get_tesla_company,
    plan_tesla_push,
    run_tesla_manual_push,
)
from app.schemas.manual_ingest import (
    TeslaPlanResponse,
    TeslaPushPayload,
    TeslaPushResponse,
    TeslaStatePayload,
)

router = APIRouter(prefix="/ingest", tags=["manual-ingest"])


def _verify_ingest_token(
    settings: Settings,
    x_ingest_token: str | None,
) -> None:
    expected = settings.tesla_ingest_token.strip()
    if not expected:
        return
    if x_ingest_token != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid ingest token")


async def _require_tesla_company(db: AsyncSession):
    company = await get_tesla_company(db)
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tesla company not found")
    if not company.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tesla company is not active")
    return company


@router.get("/tesla/known-ids", response_model=list[str])
async def tesla_known_ids(
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
    x_ingest_token: str | None = Header(default=None, alias="X-Ingest-Token"),
) -> list[str]:
    _verify_ingest_token(settings, x_ingest_token)
    company = await _require_tesla_company(db)
    return await get_known_external_ids(db, company.id)


@router.post("/tesla/plan", response_model=TeslaPlanResponse)
async def tesla_plan(
    payload: TeslaStatePayload,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
    x_ingest_token: str | None = Header(default=None, alias="X-Ingest-Token"),
) -> TeslaPlanResponse:
    _verify_ingest_token(settings, x_ingest_token)
    company = await _require_tesla_company(db)
    try:
        plan = await plan_tesla_push(db, company, payload.state)
    except ParseError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return TeslaPlanResponse(**plan)


@router.post("/tesla/push", response_model=TeslaPushResponse)
async def tesla_push(
    payload: TeslaPushPayload,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
    x_ingest_token: str | None = Header(default=None, alias="X-Ingest-Token"),
) -> TeslaPushResponse:
    _verify_ingest_token(settings, x_ingest_token)
    company = await _require_tesla_company(db)
    if not payload.state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty state payload")
    try:
        outcome, run_id = await run_tesla_manual_push(
            db,
            company,
            payload.state,
            payload.details,
            settings=settings,
        )
    except ParseError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    from app.ingestion.connectors.tesla_careers import iter_site_listings, resolve_tesla_careers_config

    config = resolve_tesla_careers_config(company)
    listing_count = len(iter_site_listings(payload.state, config["sites"]))
    return TeslaPushResponse(
        status="accepted",
        run_id=run_id,
        listing_count=listing_count,
        new_details_received=len(payload.details),
        jobs_fetched=outcome.jobs_fetched,
        jobs_new=outcome.jobs_new,
        jobs_updated=outcome.jobs_updated,
        jobs_unchanged=outcome.jobs_unchanged,
        jobs_removed=outcome.jobs_removed,
    )
