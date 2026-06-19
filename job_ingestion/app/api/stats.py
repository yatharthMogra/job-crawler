from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.ingestion.ops_stats import collect_ops_stats

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("")
async def get_ops_stats(db: AsyncSession = Depends(get_db)) -> dict:
    settings = get_settings()
    return await collect_ops_stats(db, settings=settings, trigger="api")
