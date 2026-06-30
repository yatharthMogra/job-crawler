from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.database import get_db
from app.models.company_watch import CompanyWatchSubscription
from app.models.notification_preferences import NotificationPreferences
from app.models.shared import Company
from app.notification.digest import (
    clamp_cadence_hours,
    clamp_top_k,
    compute_next_digest_due_at,
    get_or_create_preferences,
)
from app.schemas.notifications import (
    CompanySearchOut,
    CompanyWatchItemOut,
    CompanyWatchListOut,
    CompanyWatchUpdateIn,
    NotificationPreferencesOut,
    NotificationPreferencesUpdateIn,
)

router = APIRouter(tags=["notifications"])


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _serialize_preferences(prefs: NotificationPreferences) -> NotificationPreferencesOut:
    return NotificationPreferencesOut(
        candidate_id=prefs.candidate_id,
        digest_enabled=prefs.digest_enabled,
        company_watch_enabled=prefs.company_watch_enabled,
        cadence_hours=prefs.cadence_hours,
        top_k=prefs.top_k,
        digest_filters=prefs.digest_filters,
        last_digest_sent_at=prefs.last_digest_sent_at,
        next_digest_due_at=prefs.next_digest_due_at,
    )


@router.get("/notification-preferences/{candidate_id}", response_model=NotificationPreferencesOut)
async def get_notification_preferences(
    candidate_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> NotificationPreferencesOut:
    prefs = await get_or_create_preferences(db, candidate_id, settings)
    await db.commit()
    return _serialize_preferences(prefs)


@router.put("/notification-preferences/{candidate_id}", response_model=NotificationPreferencesOut)
async def update_notification_preferences(
    candidate_id: uuid.UUID,
    payload: NotificationPreferencesUpdateIn,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> NotificationPreferencesOut:
    prefs = await get_or_create_preferences(db, candidate_id, settings)

    if payload.digest_enabled is not None:
        prefs.digest_enabled = payload.digest_enabled
    if payload.company_watch_enabled is not None:
        prefs.company_watch_enabled = payload.company_watch_enabled
    if payload.cadence_hours is not None:
        prefs.cadence_hours = clamp_cadence_hours(payload.cadence_hours)
        prefs.next_digest_due_at = compute_next_digest_due_at(
            last_sent_at=prefs.last_digest_sent_at,
            cadence_hours=prefs.cadence_hours,
            now=_utcnow(),
        )
    if payload.top_k is not None:
        prefs.top_k = clamp_top_k(payload.top_k)
    if payload.digest_filters is not None:
        prefs.digest_filters = payload.digest_filters.model_dump(exclude_none=True)

    if prefs.next_digest_due_at is None:
        prefs.next_digest_due_at = compute_next_digest_due_at(
            last_sent_at=prefs.last_digest_sent_at,
            cadence_hours=prefs.cadence_hours,
            now=_utcnow(),
        )

    await db.commit()
    await db.refresh(prefs)
    return _serialize_preferences(prefs)


@router.get("/company-watch/{candidate_id}", response_model=CompanyWatchListOut)
async def get_company_watch(
    candidate_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> CompanyWatchListOut:
    rows = (
        await db.execute(
            select(CompanyWatchSubscription, Company)
            .join(Company, Company.id == CompanyWatchSubscription.company_id)
            .where(
                CompanyWatchSubscription.candidate_id == candidate_id,
                CompanyWatchSubscription.is_active.is_(True),
            )
            .order_by(Company.name.asc())
        )
    ).all()

    companies = [
        CompanyWatchItemOut(
            company_id=company.id,
            company_name=company.name,
            platform=company.platform,
            is_active=company.is_active,
        )
        for _sub, company in rows
    ]
    return CompanyWatchListOut(candidate_id=candidate_id, companies=companies)


@router.put("/company-watch/{candidate_id}", response_model=CompanyWatchListOut)
async def update_company_watch(
    candidate_id: uuid.UUID,
    payload: CompanyWatchUpdateIn,
    db: AsyncSession = Depends(get_db),
) -> CompanyWatchListOut:
    requested_ids = list(dict.fromkeys(payload.company_ids))

    if requested_ids:
        valid_companies = (
            await db.scalars(
                select(Company.id).where(
                    Company.id.in_(requested_ids),
                    Company.is_active.is_(True),
                )
            )
        ).all()
        valid_set = set(valid_companies)
        invalid = [cid for cid in requested_ids if cid not in valid_set]
        if invalid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more company IDs are invalid or inactive",
            )

    existing = (
        await db.scalars(
            select(CompanyWatchSubscription).where(
                CompanyWatchSubscription.candidate_id == candidate_id,
            )
        )
    ).all()
    existing_by_company = {row.company_id: row for row in existing}
    requested_set = set(requested_ids)

    for company_id, row in existing_by_company.items():
        row.is_active = company_id in requested_set

    for company_id in requested_set:
        if company_id not in existing_by_company:
            db.add(
                CompanyWatchSubscription(
                    candidate_id=candidate_id,
                    company_id=company_id,
                    is_active=True,
                )
            )

    await db.commit()
    return await get_company_watch(candidate_id, db)


@router.get("/companies/search", response_model=list[CompanySearchOut])
async def search_companies(
    q: str = Query(default="", max_length=128),
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> list[CompanySearchOut]:
    stmt = select(Company).where(Company.is_active.is_(True))
    if q.strip():
        pattern = f"%{q.strip()}%"
        stmt = stmt.where(or_(Company.name.ilike(pattern), Company.board_token.ilike(pattern)))
    stmt = stmt.order_by(Company.name.asc()).limit(limit)
    rows = (await db.scalars(stmt)).all()
    return [
        CompanySearchOut(
            id=row.id,
            name=row.name,
            platform=row.platform,
            is_active=row.is_active,
        )
        for row in rows
    ]
