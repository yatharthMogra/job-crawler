"""Reciprocal Rank Fusion for multi-signal retrieval."""

from __future__ import annotations

from collections import defaultdict
from uuid import UUID


def reciprocal_rank_fusion(
    ranked_lists: list[list[UUID]],
    *,
    k: int = 60,
) -> list[UUID]:
    """Fuse ranked ID lists via Σ 1/(k + rank). Ranks are 1-based."""
    scores: dict[UUID, float] = defaultdict(float)
    for ranked in ranked_lists:
        for rank, job_id in enumerate(ranked, start=1):
            scores[job_id] += 1.0 / (k + rank)
    return sorted(scores.keys(), key=lambda job_id: scores[job_id], reverse=True)
