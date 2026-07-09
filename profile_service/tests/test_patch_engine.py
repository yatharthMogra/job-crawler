import pytest

from app.pipeline.patch_engine import _merge_constraints


def test_merge_constraints_merges_eeo_nested() -> None:
    out = _merge_constraints(
        {"eeo": {"gender": "prefer_not"}, "minimum_salary": 100000},
        {"eeo": {"requires_sponsorship": True}, "internship_only": True},
    )
    assert out["eeo"] == {"gender": "prefer_not", "requires_sponsorship": True}
    assert out["minimum_salary"] == 100000
    assert out["internship_only"] is True


def test_merge_constraints_flat_update() -> None:
    out = _merge_constraints({"fulltime_only": False}, {"fulltime_only": True})
    assert out["fulltime_only"] is True


@pytest.mark.asyncio
async def test_write_profile_filters_requires_updates() -> None:
    from unittest.mock import AsyncMock

    from app.pipeline.patch_engine import write_profile_filters

    with pytest.raises(ValueError, match="No filter updates"):
        await write_profile_filters(
            AsyncMock(),
            candidate_id=__import__("uuid").uuid4(),
            constraints_updates={},
            preferences_updates={},
        )
