from __future__ import annotations

import os
from functools import lru_cache

import structlog

log = structlog.get_logger(__name__)

DEFAULT_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384


def _apply_hf_token() -> None:
    from app.config import get_settings

    token = get_settings().hf_token.strip()
    if not token:
        return
    os.environ.setdefault("HF_TOKEN", token)
    os.environ.setdefault("HUGGING_FACE_HUB_TOKEN", token)


@lru_cache(maxsize=1)
def _load_model():
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError("sentence-transformers is required for embedding computation") from exc
    _apply_hf_token()
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
