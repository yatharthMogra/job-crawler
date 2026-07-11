from __future__ import annotations

import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.backfill import backfill_missing_resume_embeddings
from app.models.resume import CandidateResume


@pytest.mark.asyncio
async def test_backfill_stops_when_no_rows() -> None:
    db = AsyncMock()
    scalars_result = MagicMock()
    scalars_result.all.return_value = []
    db.scalars.return_value = scalars_result

    with patch("app.backfill.AsyncSessionLocal") as mock_session_local:
        mock_session_local.return_value.__aenter__.return_value = db
        with patch("app.backfill.embed_text") as mock_embed:
            result = await backfill_missing_resume_embeddings(batch_size=100)
            mock_embed.assert_not_called()

    assert result == {"updated": 0, "skipped": 0, "batches": 0}


@pytest.mark.asyncio
async def test_backfill_filters_null_embeddings_only() -> None:
    resume = CandidateResume(
        id=uuid.uuid4(),
        extraction_status="success",
        raw_text="Python engineer with FastAPI experience",
        uploaded_at=datetime.now(UTC),
        content_embedding=None,
    )
    db = AsyncMock()
    scalars_result = MagicMock()
    scalars_result.all.side_effect = [[resume], []]
    db.scalars.return_value = scalars_result

    fake_vector = [0.1] * 384
    with patch("app.backfill.AsyncSessionLocal") as mock_session_local:
        mock_session_local.return_value.__aenter__.return_value = db
        with patch("app.backfill.embed_text", return_value=fake_vector):
            result = await backfill_missing_resume_embeddings(batch_size=100)

    assert result["updated"] == 1
    assert resume.content_embedding == fake_vector
    assert resume.content_embedding_model == "all-MiniLM-L6-v2"
    db.commit.assert_awaited()
