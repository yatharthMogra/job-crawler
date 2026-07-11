"""Async Redis client lifecycle for recommendation session cache."""

from __future__ import annotations

from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from redis.asyncio import Redis

log = structlog.get_logger(__name__)

_redis: Redis | None = None


async def init_redis(redis_url: str) -> Redis:
    global _redis
    if not redis_url:
        raise RuntimeError("REDIS_URL is required for recommendation cache")
    from redis.asyncio import from_url

    _redis = from_url(redis_url, decode_responses=True)
    await _redis.ping()
    log.info("redis_connected")
    return _redis


async def close_redis() -> None:
    global _redis
    if _redis is not None:
        await _redis.aclose()
        _redis = None
        log.info("redis_closed")


def get_redis() -> Redis:
    if _redis is None:
        raise RuntimeError("Redis client is not initialized")
    return _redis
