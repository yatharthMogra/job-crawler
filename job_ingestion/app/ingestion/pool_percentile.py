from __future__ import annotations

from datetime import UTC, datetime

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.pool_embedding_cache import (
    cosine_similarity_distribution,
    get_pool_embedding_matrix,
    percentile_values,
)
from app.models.normalized_job import NormalizedJob

log = structlog.get_logger(__name__)


async def compute_pool_percentile_cutoffs_for_embedding(
    db: AsyncSession,
    embedding: list[float],
    retrieval_pools: list[str],
) -> dict[str, dict[str, float | str]]:
    if not embedding:
        return {}

    cutoffs: dict[str, dict[str, float | str]] = {}
    for pool_name in retrieval_pools:
        _, matrix = await get_pool_embedding_matrix(db, pool_name)
        if matrix is None or matrix.size == 0:
            continue
        scores = cosine_similarity_distribution(embedding, matrix)
        pool_cutoffs = percentile_values(scores)
        if pool_cutoffs is not None:
            cutoffs[pool_name] = pool_cutoffs
    return cutoffs


async def compute_pool_percentile_cutoffs(
    db: AsyncSession,
    job: NormalizedJob,
) -> dict[str, dict[str, float | str]]:
    if not job.content_embedding:
        return {}
    return await compute_pool_percentile_cutoffs_for_embedding(
        db,
        job.content_embedding,
        job.retrieval_pools or [],
    )


async def refresh_cutoffs_for_active_jobs(db: AsyncSession, *, batch_size: int = 100) -> dict[str, int]:
    updated = 0
    scanned = 0
    offset = 0
    while True:
        jobs = (
            await db.scalars(
                select(NormalizedJob)
                .where(
                    NormalizedJob.is_active.is_(True),
                    NormalizedJob.processing_state == "success",
                    NormalizedJob.content_embedding.is_not(None),
                )
                .order_by(NormalizedJob.id)
                .offset(offset)
                .limit(batch_size)
            )
        ).all()
        if not jobs:
            break
        scanned += len(jobs)
        for job in jobs:
            cutoffs = await compute_pool_percentile_cutoffs(db, job)
            if cutoffs:
                job.pool_percentile_cutoffs = cutoffs
                updated += 1
        await db.commit()
        offset += batch_size
    log.info("pool_percentile_cutoffs_refreshed", scanned=scanned, updated=updated)
    return {"scanned": scanned, "updated": updated}
