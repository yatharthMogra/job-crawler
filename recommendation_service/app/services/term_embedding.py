from __future__ import annotations

from functools import lru_cache

import structlog

log = structlog.get_logger(__name__)

MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def _model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(MODEL_NAME)


@lru_cache(maxsize=4096)
def embed_term(term: str) -> list[float] | None:
    cleaned = term.strip().lower()
    if not cleaned:
        return None
    try:
        vector = _model().encode(cleaned, normalize_embeddings=True)
        return [float(value) for value in vector.tolist()]
    except Exception as exc:
        log.warning("term_embedding_failed", error=str(exc))
        return None
