from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.archival.active_cleanup import run_active_cleanup
from app.archival.archive_cleanup import run_archive_cleanup


async def run_all_cleanup(db: AsyncSession) -> dict:
    active_stats = await run_active_cleanup(db)
    archive_stats = await run_archive_cleanup(db)
    return {"active_cleanup": active_stats, "archive_cleanup": archive_stats}
