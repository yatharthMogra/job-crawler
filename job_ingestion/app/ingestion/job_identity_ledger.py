from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job_identity_ledger import JobIdentityLedger


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


async def load_ledger_hashes(db: AsyncSession, company_id: UUID) -> dict[str, str]:
    rows = (
        await db.execute(
            select(JobIdentityLedger.external_job_id, JobIdentityLedger.content_hash).where(
                JobIdentityLedger.company_id == company_id
            )
        )
    ).all()
    return {external_job_id: content_hash for external_job_id, content_hash in rows}


async def load_ledger_first_seen_map(db: AsyncSession, company_id: UUID) -> dict[str, datetime]:
    rows = (
        await db.execute(
            select(JobIdentityLedger.external_job_id, JobIdentityLedger.first_seen_at).where(
                JobIdentityLedger.company_id == company_id
            )
        )
    ).all()
    return {external_job_id: first_seen_at for external_job_id, first_seen_at in rows}


async def upsert_ledger_entry(
    db: AsyncSession,
    company_id: UUID,
    external_job_id: str,
    content_hash: str,
    *,
    seen_at: datetime | None = None,
) -> None:
    now = seen_at or _utcnow()
    existing_hash = await db.scalar(
        select(JobIdentityLedger.content_hash).where(
            JobIdentityLedger.company_id == company_id,
            JobIdentityLedger.external_job_id == external_job_id,
        )
    )
    if existing_hash is None:
        stmt = pg_insert(JobIdentityLedger).values(
            company_id=company_id,
            external_job_id=external_job_id,
            content_hash=content_hash,
            first_seen_at=now,
            last_seen_at=now,
            last_changed_at=None,
        )
        await db.execute(stmt)
        return

    values = {
        "content_hash": content_hash,
        "last_seen_at": now,
    }
    if existing_hash != content_hash:
        values["last_changed_at"] = now
    await db.execute(
        update(JobIdentityLedger)
        .where(
            JobIdentityLedger.company_id == company_id,
            JobIdentityLedger.external_job_id == external_job_id,
        )
        .values(**values)
    )


async def touch_ledger_seen(
    db: AsyncSession,
    company_id: UUID,
    external_job_ids: list[str],
    *,
    seen_at: datetime | None = None,
) -> None:
    if not external_job_ids:
        return
    now = seen_at or _utcnow()
    await db.execute(
        update(JobIdentityLedger)
        .where(
            JobIdentityLedger.company_id == company_id,
            JobIdentityLedger.external_job_id.in_(external_job_ids),
        )
        .values(last_seen_at=now)
    )
