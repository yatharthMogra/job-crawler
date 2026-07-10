from __future__ import annotations

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.embeddings.service import embed_text, embedding_model_name
from app.ingestion.pool_percentile import compute_pool_percentile_cutoffs
from app.models.normalized_job import NormalizedJob
from app.scoring.text_corpus import job_content_text

log = structlog.get_logger(__name__)


async def apply_job_ats_enrichment(db: AsyncSession, job: NormalizedJob) -> None:
    text = job_content_text(job)
    embedding = embed_text(text)
    if embedding is None:
        return
    job.content_embedding = embedding
    job.content_embedding_model = embedding_model_name()
    try:
        job.pool_percentile_cutoffs = await compute_pool_percentile_cutoffs(db, job)
    except Exception as exc:
        log.warning("pool_percentile_cutoff_failed", job_id=str(job.id), error=str(exc))
