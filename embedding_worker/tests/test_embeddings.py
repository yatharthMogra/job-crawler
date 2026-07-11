from __future__ import annotations

import math
from unittest.mock import MagicMock, patch

from app.embeddings.service import EMBEDDING_DIM, embed_text, embedding_model_name


def test_embedding_model_name() -> None:
    assert embedding_model_name() == "all-MiniLM-L6-v2"


def test_embed_text_empty_returns_none() -> None:
    assert embed_text("") is None
    assert embed_text("   ") is None


def test_embed_text_returns_normalized_384_dim_vector() -> None:
    raw = [3.0, 4.0] + [0.0] * (EMBEDDING_DIM - 2)
    norm = math.sqrt(sum(value * value for value in raw))
    normalized = [value / norm for value in raw]

    mock_model = MagicMock()
    mock_model.encode.return_value = MagicMock(tolist=lambda: normalized)

    with patch("app.embeddings.service._load_model", return_value=mock_model):
        result = embed_text("Python engineer")

    assert result is not None
    assert len(result) == EMBEDDING_DIM
    result_norm = math.sqrt(sum(value * value for value in result))
    assert math.isclose(result_norm, 1.0, rel_tol=1e-5)
    mock_model.encode.assert_called_once_with("Python engineer", normalize_embeddings=True)
