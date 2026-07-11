from __future__ import annotations

import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch

import pytest

from app.handlers.resume import ResumeEmbedOutcome, _process_resume_embedding
from app.models.resume import CandidateResume


@pytest.mark.asyncio
async def test_process_resume_skips_when_already_embedded() -> None:
    resume_id = uuid.uuid4()
    resume = CandidateResume(
        id=resume_id,
        extraction_status="success",
        raw_text="Some resume text",
        uploaded_at=datetime.now(UTC),
        content_embedding=[0.1] * 384,
    )
    db = AsyncMock()
    db.get.return_value = resume

    with patch("app.handlers.resume.embed_text") as mock_embed:
        outcome = await _process_resume_embedding(db, resume_id)
        mock_embed.assert_not_called()

    assert outcome == ResumeEmbedOutcome.SKIPPED
