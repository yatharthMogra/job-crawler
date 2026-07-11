"""Shared embedding similarity helpers for RRF retrieval and ATS fit."""

from __future__ import annotations

import math


def cosine_similarity(a: list[float], b: list[float]) -> float | None:
    if not a or not b or len(a) != len(b):
        return None
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return None
    return dot / (norm_a * norm_b)


def max_cosine_similarity(
    job_embedding: list[float] | None,
    resume_embeddings: list[list[float]],
) -> float:
    """Return max cosine similarity across resume vectors, or 0.0 if none compare."""
    if not job_embedding or not resume_embeddings:
        return 0.0
    best = 0.0
    for resume_embedding in resume_embeddings:
        score = cosine_similarity(job_embedding, resume_embedding)
        if score is not None and score > best:
            best = score
    return best


def calibrate_similarity(raw: float, min_sim: float, max_sim: float) -> float:
    if max_sim <= min_sim:
        return 0.5
    return max(0.0, min(1.0, (raw - min_sim) / (max_sim - min_sim)))
