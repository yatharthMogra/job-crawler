from __future__ import annotations

import math

from app.notification.retrieval import pool_floor_size


def test_pool_floor_size_with_ten_pools() -> None:
    assert pool_floor_size(500, 10, 0.1) == math.ceil((500 / 10) * 0.1)


def test_pool_floor_size_minimum_one() -> None:
    assert pool_floor_size(500, 1000, 0.1) == 1


def test_pool_floor_size_empty_pools_returns_cap() -> None:
    assert pool_floor_size(500, 0, 0.1) == 500
