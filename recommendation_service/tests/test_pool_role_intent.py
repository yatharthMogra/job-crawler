from __future__ import annotations

import pytest

from app.pool_role_intent import (
    POOL_BASE_TO_ROLE_INTENT,
    pool_base_name,
    role_intent_for_pool,
    role_intents_for_pools,
)
from app.constants import ROLE_INTENTS


@pytest.mark.parametrize(
    ("pool_name", "expected_base", "expected_intent"),
    [
        ("SWE_FULLTIME", "SWE", "engineer"),
        ("BACKEND_ENGINEER_INTERNSHIP", "BACKEND_ENGINEER", "engineer"),
        ("DATA_ANALYST_NEW_GRAD", "DATA_ANALYST", "analyst"),
        ("DATA_SCIENTIST_FULLTIME", "DATA_SCIENTIST", "researcher"),
        ("SOLUTIONS_CONSULTANT_FULLTIME", "SOLUTIONS_CONSULTANT", "consultant"),
        ("SALES_FULLTIME", "SALES", "sales"),
    ],
)
def test_pool_role_intent_mapping(
    pool_name: str,
    expected_base: str,
    expected_intent: str,
) -> None:
    assert pool_base_name(pool_name) == expected_base
    assert role_intent_for_pool(pool_name) == expected_intent


def test_role_intents_for_pools_deduplicates() -> None:
    pools = ["SWE_FULLTIME", "BACKEND_ENGINEER_FULLTIME", "DATA_ANALYST_FULLTIME"]
    assert role_intents_for_pools(pools) == ["engineer", "analyst"]


def test_all_mapped_intents_are_valid() -> None:
    for intent in set(POOL_BASE_TO_ROLE_INTENT.values()):
        assert intent in ROLE_INTENTS
