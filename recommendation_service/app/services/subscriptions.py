from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.subscription import UserPoolSubscription


async def get_active_pools(db: AsyncSession, candidate_id: uuid.UUID) -> list[str]:
    rows = (
        await db.scalars(
            select(UserPoolSubscription.pool_name).where(
                UserPoolSubscription.candidate_id == candidate_id,
                UserPoolSubscription.is_active.is_(True),
            )
        )
    ).all()
    return list(rows)
