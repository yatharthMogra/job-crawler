from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    pass

log = structlog.get_logger(__name__)

DEFAULT_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384


@lru_cache(maxsize=1)
def _load_model():
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError("sentence-transformers is required for embedding computation") from exc
    return SentenceTransformer(DEFAULT_MODEL)


def embed_text(text: str) -> list[float] | None:
    cleaned = text.strip()
    if not cleaned:
        return None
    try:
        model = _load_model()
        vector = model.encode(cleaned, normalize_embeddings=True)
        return [float(value) for value in vector.tolist()]
    except Exception as exc:
        log.warning("embedding_failed", error=str(exc))
        return None


def embedding_model_name() -> str:
    return DEFAULT_MODEL
