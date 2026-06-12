from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import normalize_pool_names
from app.database import get_db
from app.models.subscription import UserPoolSubscription
from app.schemas.subscription import (
    SubscriptionCreateIn,
    SubscriptionListOut,
    SubscriptionOut,
    SubscriptionUpdateIn,
)

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.post("", response_model=list[SubscriptionOut], status_code=status.HTTP_201_CREATED)
async def create_subscriptions(
    payload: SubscriptionCreateIn,
    db: AsyncSession = Depends(get_db),
) -> list[SubscriptionOut]:
    created: list[UserPoolSubscription] = []
    for pool_name in normalize_pool_names(payload.pool_names):
        existing = await db.scalar(
            select(UserPoolSubscription).where(
                UserPoolSubscription.candidate_id == payload.candidate_id,
                UserPoolSubscription.pool_name == pool_name,
            )
        )
        if existing:
            existing.is_active = True
            created.append(existing)
            continue
        row = UserPoolSubscription(
            candidate_id=payload.candidate_id,
            pool_name=pool_name,
            is_active=True,
        )
        db.add(row)
        created.append(row)
    await db.commit()
    for row in created:
        await db.refresh(row)
    return [SubscriptionOut.model_validate(row) for row in created]


@router.get("/{candidate_id}", response_model=SubscriptionListOut)
async def get_subscriptions(
    candidate_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> SubscriptionListOut:
    rows = (
        await db.scalars(
            select(UserPoolSubscription)
            .where(UserPoolSubscription.candidate_id == candidate_id)
            .order_by(UserPoolSubscription.created_at.asc())
        )
    ).all()
    return SubscriptionListOut(
        candidate_id=candidate_id,
        subscriptions=[SubscriptionOut.model_validate(row) for row in rows],
    )


@router.patch("/{candidate_id}", response_model=list[SubscriptionOut])
async def update_subscriptions(
    candidate_id: uuid.UUID,
    payload: SubscriptionUpdateIn,
    db: AsyncSession = Depends(get_db),
) -> list[SubscriptionOut]:
    existing_rows = (
        await db.scalars(select(UserPoolSubscription).where(UserPoolSubscription.candidate_id == candidate_id))
    ).all()
    desired = set(normalize_pool_names(payload.pool_names))
    updated: list[UserPoolSubscription] = []

    for row in existing_rows:
        row.is_active = payload.is_active and row.pool_name in desired
        updated.append(row)

    existing_names = {row.pool_name for row in existing_rows}
    for pool_name in desired - existing_names:
        row = UserPoolSubscription(
            candidate_id=candidate_id,
            pool_name=pool_name,
            is_active=payload.is_active,
        )
        db.add(row)
        updated.append(row)

    await db.commit()
    for row in updated:
        await db.refresh(row)
    return [SubscriptionOut.model_validate(row) for row in updated if row.is_active]
