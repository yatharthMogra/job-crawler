from __future__ import annotations

import time
import uuid
from dataclasses import dataclass

import numpy as np
import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate_resume import CandidateResume
from app.models.user_pool_subscription import UserPoolSubscription

log = structlog.get_logger(__name__)

CACHE_TTL_SECONDS = 900


@dataclass
class PoolEmbeddingCacheEntry:
    candidate_ids: list[str]
    matrix: np.ndarray
    loaded_at: float


_cache: dict[str, PoolEmbeddingCacheEntry] = {}


def invalidate_pool_embedding_cache(pool_name: str | None = None) -> None:
    if pool_name is None:
        _cache.clear()
        return
    _cache.pop(pool_name, None)


async def _latest_resume_embeddings(
    db: AsyncSession,
    candidate_ids: list[uuid.UUID],
) -> dict[uuid.UUID, list[float]]:
    if not candidate_ids:
        return {}
    rows = (
        await db.scalars(
            select(CandidateResume).where(
                CandidateResume.candidate_id.in_(candidate_ids),
                CandidateResume.content_embedding.is_not(None),
            )
        )
    ).all()
    latest: dict[uuid.UUID, CandidateResume] = {}
    for row in rows:
        existing = latest.get(row.candidate_id)
        if existing is None or row.uploaded_at > existing.uploaded_at:
            latest[row.candidate_id] = row
    return {
        candidate_id: list(resume.content_embedding or [])
        for candidate_id, resume in latest.items()
        if resume.content_embedding
    }


async def get_pool_embedding_matrix(
    db: AsyncSession,
    pool_name: str,
    *,
    force_refresh: bool = False,
) -> tuple[list[str], np.ndarray | None]:
    now = time.time()
    cached = _cache.get(pool_name)
    if not force_refresh and cached and now - cached.loaded_at < CACHE_TTL_SECONDS:
        return cached.candidate_ids, cached.matrix

    subscriber_ids = (
        await db.scalars(
            select(UserPoolSubscription.candidate_id).where(
                UserPoolSubscription.pool_name == pool_name,
                UserPoolSubscription.is_active.is_(True),
            )
        )
    ).all()
    embeddings_by_candidate = await _latest_resume_embeddings(db, list(subscriber_ids))
    if not embeddings_by_candidate:
        _cache[pool_name] = PoolEmbeddingCacheEntry(candidate_ids=[], matrix=np.empty((0, 0)), loaded_at=now)
        return [], None

    candidate_ids = list(embeddings_by_candidate.keys())
    vectors = [embeddings_by_candidate[candidate_id] for candidate_id in candidate_ids]
    matrix = np.asarray(vectors, dtype=np.float32)
    _cache[pool_name] = PoolEmbeddingCacheEntry(
        candidate_ids=[str(candidate_id) for candidate_id in candidate_ids],
        matrix=matrix,
        loaded_at=now,
    )
    return [str(candidate_id) for candidate_id in candidate_ids], matrix


def cosine_similarity_distribution(job_embedding: list[float], subscriber_matrix: np.ndarray) -> list[float]:
    if subscriber_matrix.size == 0:
        return []
    job_vector = np.asarray(job_embedding, dtype=np.float32)
    norm = np.linalg.norm(job_vector)
    if norm == 0:
        return []
    normalized_job = job_vector / norm
    norms = np.linalg.norm(subscriber_matrix, axis=1)
    valid = norms > 0
    if not np.any(valid):
        return []
    similarities = subscriber_matrix[valid] @ normalized_job
    return [float(value) for value in similarities.tolist()]


def percentile_values(scores: list[float]) -> dict[str, float] | None:
    if len(scores) < 5:
        return None
    array = np.asarray(scores, dtype=np.float32)
    return {
        "p50": float(np.percentile(array, 50)),
        "p75": float(np.percentile(array, 75)),
        "p90": float(np.percentile(array, 90)),
        "p95": float(np.percentile(array, 95)),
        "computed_at": datetime.now(UTC).isoformat(),
    }
