import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.notification.digest import clamp_cadence_hours, clamp_top_k, get_or_create_preferences
from app.models.notification_preferences import NotificationPreferences


@pytest.mark.asyncio
async def test_get_or_create_preferences_existing() -> None:
    db = AsyncMock()
    candidate_id = uuid.uuid4()
    existing = NotificationPreferences(candidate_id=candidate_id, cadence_hours=12, top_k=5)
    db.get = AsyncMock(return_value=existing)

    prefs = await get_or_create_preferences(db, candidate_id)
    assert prefs.cadence_hours == 12
    db.add.assert_not_called()


@pytest.mark.asyncio
async def test_get_or_create_preferences_creates_new() -> None:
    db = AsyncMock()
    candidate_id = uuid.uuid4()
    db.get = AsyncMock(return_value=None)
    db.add = MagicMock()
    db.flush = AsyncMock()

    prefs = await get_or_create_preferences(db, candidate_id)
    assert prefs.candidate_id == candidate_id
    assert prefs.digest_enabled is True
    db.add.assert_called_once()


def test_clamp_cadence_for_api() -> None:
    assert clamp_cadence_hours(500) == 168
    assert clamp_top_k(100) == 20
