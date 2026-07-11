"""Tests for embedding similarity helpers."""

from __future__ import annotations

from app.scoring.embedding_similarity import (
    calibrate_similarity,
    cosine_similarity,
    max_cosine_similarity,
)


def test_cosine_identical() -> None:
    v = [1.0, 0.0, 0.0]
    assert cosine_similarity(v, v) == 1.0


def test_cosine_orthogonal() -> None:
    assert abs(cosine_similarity([1.0, 0.0], [0.0, 1.0]) or 0) < 1e-9


def test_cosine_mismatched_length() -> None:
    assert cosine_similarity([1.0], [1.0, 0.0]) is None


def test_max_cosine_picks_best_resume() -> None:
    job = [1.0, 0.0, 0.0]
    resumes = [
        [0.0, 1.0, 0.0],  # orthogonal
        [0.9, 0.1, 0.0],  # closer
    ]
    score = max_cosine_similarity(job, resumes)
    assert score > 0.8


def test_max_cosine_empty() -> None:
    assert max_cosine_similarity(None, [[1.0]]) == 0.0
    assert max_cosine_similarity([1.0], []) == 0.0


def test_calibrate_similarity() -> None:
    assert calibrate_similarity(0.3, 0.3, 0.9) == 0.0
    assert calibrate_similarity(0.9, 0.3, 0.9) == 1.0
    assert abs(calibrate_similarity(0.6, 0.3, 0.9) - 0.5) < 1e-9
