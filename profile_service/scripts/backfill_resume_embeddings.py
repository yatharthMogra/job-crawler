#!/usr/bin/env python3
"""Backfill content embeddings for candidate resumes."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.embeddings.service import embed_text, embedding_model_name
from app.models.resume import CandidateResume


async def main(*, limit: int) -> None:
    updated = 0
    async with AsyncSessionLocal() as db:
        resumes = (
            await db.scalars(
                select(CandidateResume)
                .where(
                    CandidateResume.extraction_status == "success",
                    CandidateResume.raw_text.is_not(None),
                )
                .order_by(CandidateResume.uploaded_at.desc())
                .limit(limit)
            )
        ).all()
        for resume in resumes:
            embedding = embed_text(resume.raw_text or "")
            if embedding is None:
                continue
            resume.content_embedding = embedding
            resume.content_embedding_model = embedding_model_name()
            resume.content_embedding_computed_at = datetime.now(UTC)
            updated += 1
        await db.commit()
    print(json.dumps({"updated": updated}, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backfill resume embeddings")
    parser.add_argument("--limit", type=int, default=500)
    args = parser.parse_args()
    asyncio.run(main(limit=args.limit))
