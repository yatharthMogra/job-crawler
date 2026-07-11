"""Tests for recommendation session cache (fakeredis)."""

from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, patch

import pytest

from app.config import Settings
from app.services.profile_loader import UserProfile
from app.services.recommendation_pipeline import AuxSnapshot, PipelineResult, RankedJobEntry


@pytest.fixture
async def fake_redis():
    fakeredis = pytest.importorskip("fakeredis")
    from fakeredis import aioredis as fake_aioredis

    client = fake_aioredis.FakeRedis(decode_responses=True)
    import app.services.redis_client as redis_mod

    prev = redis_mod._redis
    redis_mod._redis = client
    yield client
    redis_mod._redis = prev
    await client.aclose()


def _pipeline_result(candidate_id: uuid.UUID | None = None) -> PipelineResult:
    cid = candidate_id or uuid.uuid4()
    profile = UserProfile(
        candidate_id=cid,
        email="t@example.com",
        name="Test",
        constraints={},
        preferences={},
        skills={"languages": ["Python"]},
    )
    job_id = uuid.uuid4()
    return PipelineResult(
        ranked_entries=[
            RankedJobEntry(
                job_id=job_id,
                personal_score=0.8,
                opportunity_score=0.7,
                reference_timestamp=1.0,
                company_name="Acme",
            )
        ],
        profile=profile,
        profile_version=1,
        resume_fingerprint="abc123",
        aux_snapshot=AuxSnapshot(applied_counts={}),
    )


@pytest.mark.asyncio
async def test_store_and_load_session(fake_redis) -> None:
    from app.services.recommendation_cache import (
        load_recommendation_session,
        store_recommendation_session,
    )

    settings = Settings(recommendation_cache_ttl_seconds=1800)
    result = _pipeline_result()
    token = await store_recommendation_session(result, settings)
    session = await load_recommendation_session(token)
    assert session is not None
    assert session.candidate_id == result.profile.candidate_id
    assert session.profile_version == 1
    assert session.resume_fingerprint == "abc123"
    assert len(session.ranked_entries) == 1
    assert session.ranked_entries[0].personal_score == 0.8


@pytest.mark.asyncio
async def test_missing_token_returns_none(fake_redis) -> None:
    from app.services.recommendation_cache import load_recommendation_session

    assert await load_recommendation_session(str(uuid.uuid4())) is None


@pytest.mark.asyncio
async def test_delete_session(fake_redis) -> None:
    from app.services.recommendation_cache import (
        delete_recommendation_session,
        load_recommendation_session,
        store_recommendation_session,
    )

    settings = Settings(recommendation_cache_ttl_seconds=1800)
    token = await store_recommendation_session(_pipeline_result(), settings)
    await delete_recommendation_session(token)
    assert await load_recommendation_session(token) is None


@pytest.mark.asyncio
async def test_session_is_stale_on_profile_version_change(fake_redis) -> None:
    from app.services.recommendation_cache import (
        load_recommendation_session,
        session_is_stale,
        store_recommendation_session,
    )

    settings = Settings(recommendation_cache_ttl_seconds=1800)
    result = _pipeline_result()
    token = await store_recommendation_session(result, settings)
    session = await load_recommendation_session(token)
    assert session is not None

    db = AsyncMock()
    db.scalar = AsyncMock(return_value=2)  # profile version bumped
    with patch(
        "app.services.recommendation_cache.load_resume_fingerprint",
        new=AsyncMock(return_value="abc123"),
    ):
        assert await session_is_stale(db, session) is True
