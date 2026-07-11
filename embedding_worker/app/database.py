from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings


class Base(DeclarativeBase):
    pass


def _engine_kwargs(database_url: str) -> dict:
    is_pooler = "pooler.supabase.com" in database_url or ":6543" in database_url
    if is_pooler:
        return {
            "pool_pre_ping": True,
            "pool_size": 5,
            "max_overflow": 2,
            "connect_args": {"statement_cache_size": 0, "prepared_statement_cache_size": 0},
        }
    return {"pool_pre_ping": True}


settings = get_settings()
engine = create_async_engine(settings.database_url, **_engine_kwargs(settings.database_url))
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
