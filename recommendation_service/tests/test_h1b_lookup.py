from __future__ import annotations

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from sqlalchemy.exc import ProgrammingError

from app.services.h1b_lookup import load_h1b_summary_lookup


class _UndefinedTableError(Exception):
    pass


@pytest.mark.asyncio
async def test_load_h1b_summary_lookup_returns_empty_when_table_missing() -> None:
    db = AsyncMock()
    db.scalars = AsyncMock(
        side_effect=ProgrammingError(
            "SELECT ...",
            {},
            _UndefinedTableError('relation "h1b_company_pool_summary" does not exist'),
        )
    )

    lookup = await load_h1b_summary_lookup(db, {uuid4()})

    assert lookup == {}
    db.scalars.assert_awaited_once()


@pytest.mark.asyncio
async def test_load_h1b_summary_lookup_reraises_other_programming_errors() -> None:
    db = AsyncMock()
    db.scalars = AsyncMock(
        side_effect=ProgrammingError("SELECT ...", {}, Exception("syntax error at or near"))
    )

    with pytest.raises(ProgrammingError):
        await load_h1b_summary_lookup(db, {uuid4()})
