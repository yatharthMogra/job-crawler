import uuid
from unittest.mock import AsyncMock

import pytest

from app.ingestion.notification_events import enqueue_notification_job_events


@pytest.mark.asyncio
async def test_enqueue_notification_job_events_inserts_rows() -> None:
    db = AsyncMock()
    db.execute = AsyncMock()
    job_id = uuid.uuid4()
    company_id = uuid.uuid4()

    await enqueue_notification_job_events(db, [(job_id, company_id)])

    db.execute.assert_called_once()
    params = db.execute.call_args[0][1]
    assert params["job_id"] == job_id
    assert params["company_id"] == company_id


@pytest.mark.asyncio
async def test_enqueue_notification_job_events_noop_when_empty() -> None:
    db = AsyncMock()
    await enqueue_notification_job_events(db, [])
    db.execute.assert_not_called()
