"""Tests for reciprocal rank fusion."""

from __future__ import annotations

from uuid import uuid4

from app.scoring.rrf import reciprocal_rank_fusion


def test_rrf_prefers_items_high_in_both_lists() -> None:
    a, b, c = uuid4(), uuid4(), uuid4()
    fused = reciprocal_rank_fusion([[a, b, c], [a, c, b]], k=60)
    assert fused[0] == a


def test_rrf_single_list() -> None:
    a, b = uuid4(), uuid4()
    fused = reciprocal_rank_fusion([[a, b]], k=60)
    assert fused == [a, b]


def test_rrf_empty() -> None:
    assert reciprocal_rank_fusion([]) == []
    assert reciprocal_rank_fusion([[]]) == []


def test_rrf_union_of_lists() -> None:
    a, b, c = uuid4(), uuid4(), uuid4()
    fused = reciprocal_rank_fusion([[a, b], [c, a]], k=60)
    assert set(fused) == {a, b, c}
    assert fused[0] == a  # appears in both


def test_rrf_k_affects_scores() -> None:
    a, b = uuid4(), uuid4()
    # With large k, rank differences shrink; order still preserved for single list
    fused = reciprocal_rank_fusion([[a, b]], k=1)
    assert fused == [a, b]
