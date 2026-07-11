from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.ingestion.ats_enrichment import _row_to_job_text, backfill_missing_job_embeddings
from app.scoring.text_corpus import IdfJobText


def test_row_to_job_text_maps_columns() -> None:
    job_id = uuid.uuid4()
    row = (
        job_id,
        "Python engineer",
        None,
        ["Build pipelines"],
        ["BS degree"],
        [],
        ["Python"],
        ["Spark"],
        ["DATA_ENGINEERING_FULLTIME"],
    )
    job_text = _row_to_job_text(row)
    assert isinstance(job_text, IdfJobText)
    assert job_text.description_text == "Python engineer"
    assert job_text.tech_stack == ["Python"]


@pytest.mark.asyncio
async def test_backfill_stops_when_no_rows() -> None:
    db = AsyncMock()
    result = MagicMock()
    result.all.return_value = []
    db.execute.return_value = result

    with patch("app.ingestion.ats_enrichment.embed_text") as mock_embed:
        result_stats = await backfill_missing_job_embeddings(db, batch_size=100)
        mock_embed.assert_not_called()

    assert result_stats == {"updated": 0, "skipped": 0, "batches": 0}
