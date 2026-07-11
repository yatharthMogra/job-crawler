from __future__ import annotations

import uuid

import structlog
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.embeddings.service import embed_text, embedding_model_name
from app.ingestion.pool_percentile import compute_pool_percentile_cutoffs_for_embedding
from app.models.normalized_job import NormalizedJob
from app.scoring.text_corpus import IdfJobText, job_content_text

log = structlog.get_logger(__name__)

DEFAULT_BACKFILL_BATCH_SIZE = 500

_EMBEDDING_JOB_COLUMNS = (
    NormalizedJob.id,
    NormalizedJob.description_text,
    NormalizedJob.description_preview,
    NormalizedJob.responsibilities,
    NormalizedJob.required_qualifications,
    NormalizedJob.preferred_qualifications,
    NormalizedJob.tech_stack,
    NormalizedJob.skills,
    NormalizedJob.retrieval_pools,
)


def _row_to_job_text(row: tuple) -> IdfJobText:
    return IdfJobText(
        description_text=row[1],
        description_preview=row[2],
        responsibilities=list(row[3] or []),
        required_qualifications=list(row[4] or []),
        preferred_qualifications=list(row[5] or []),
        tech_stack=list(row[6] or []),
        skills=list(row[7] or []),
    )


async def apply_job_ats_enrichment(db: AsyncSession, job: NormalizedJob) -> None:
    text = job_content_text(job)
    embedding = embed_text(text)
    if embedding is None:
        return
    job.content_embedding = embedding
    job.content_embedding_model = embedding_model_name()
    try:
        job.pool_percentile_cutoffs = await compute_pool_percentile_cutoffs_for_embedding(
            db,
            embedding,
            job.retrieval_pools or [],
        )
    except Exception as exc:
        log.warning("pool_percentile_cutoff_failed", job_id=str(job.id), error=str(exc))


async def _persist_job_ats_enrichment(
    db: AsyncSession,
    *,
    job_id: uuid.UUID,
    embedding: list[float],
    retrieval_pools: list[str],
) -> None:
    cutoffs: dict[str, dict[str, float | str]] = {}
    try:
        cutoffs = await compute_pool_percentile_cutoffs_for_embedding(db, embedding, retrieval_pools)
    except Exception as exc:
        log.warning("pool_percentile_cutoff_failed", job_id=str(job_id), error=str(exc))

    await db.execute(
        update(NormalizedJob)
        .where(NormalizedJob.id == job_id)
        .values(
            content_embedding=embedding,
            content_embedding_model=embedding_model_name(),
            pool_percentile_cutoffs=cutoffs,
        )
    )


async def backfill_missing_job_embeddings(
    db: AsyncSession,
    *,
    batch_size: int = DEFAULT_BACKFILL_BATCH_SIZE,
    max_batches: int | None = None,
) -> dict[str, int]:
    last_id: uuid.UUID | None = None
    total_updated = 0
    total_skipped = 0
    batches = 0

    while True:
        if max_batches is not None and batches >= max_batches:
            break

        stmt = (
            select(*_EMBEDDING_JOB_COLUMNS)
            .where(
                NormalizedJob.is_active.is_(True),
                NormalizedJob.processing_state == "success",
                NormalizedJob.content_embedding.is_(None),
            )
            .order_by(NormalizedJob.id)
            .limit(batch_size)
        )
        if last_id is not None:
            stmt = stmt.where(NormalizedJob.id > last_id)

        rows = (await db.execute(stmt)).all()
        if not rows:
            break

        batch_updated = 0
        batch_skipped = 0
        for row in rows:
            job_id = row[0]
            job_text = _row_to_job_text(row)
            retrieval_pools = list(row[8] or [])
            embedding = embed_text(job_content_text(job_text))
            if embedding is None:
                batch_skipped += 1
                continue
            await _persist_job_ats_enrichment(
                db,
                job_id=job_id,
                embedding=embedding,
                retrieval_pools=retrieval_pools,
            )
            batch_updated += 1

        await db.commit()
        batches += 1
        total_updated += batch_updated
        total_skipped += batch_skipped
        last_id = rows[-1][0]
        log.info(
            "job_embedding_backfill_batch",
            batch_jobs=len(rows),
            batch_updated=batch_updated,
            batch_skipped=batch_skipped,
            total_updated=total_updated,
            last_id=str(last_id),
        )

    return {
        "updated": total_updated,
        "skipped": total_skipped,
        "batches": batches,
    }
