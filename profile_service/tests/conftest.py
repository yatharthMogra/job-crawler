import pytest

from app.database import engine


@pytest.fixture(autouse=True)
async def dispose_async_engine_after_test():
    yield
    await engine.dispose()
