#!/usr/bin/env python3
"""Estimate embedding similarity calibration bounds from resume/job pairs."""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.embeddings.service import embed_text
from app.models.candidate_resume import CandidateResume
from app.models.job_term_idf import EmbeddingCalibration
from app.models.normalized_job import NormalizedJob
from app.scoring.text_corpus import job_content_text


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


async def main(*, sample_size: int) -> None:
    async with AsyncSessionLocal() as db:
        jobs = (
            await db.scalars(
                select(NormalizedJob)
                .where(NormalizedJob.is_active.is_(True), NormalizedJob.processing_state == "success")
                .limit(sample_size)
            )
        ).all()
        resumes = (
            await db.scalars(
                select(CandidateResume)
                .where(CandidateResume.extraction_status == "success", CandidateResume.raw_text.is_not(None))
                .limit(sample_size)
            )
        ).all()
        if not jobs or not resumes:
            print(json.dumps({"error": "insufficient_data"}, ensure_ascii=True))
            return

        scores: list[float] = []
        for job in jobs:
            job_embedding = embed_text(job_content_text(job))
            if job_embedding is None:
                continue
            resume = random.choice(resumes)
            resume_embedding = embed_text(resume.raw_text or "")
            if resume_embedding is None:
                continue
            scores.append(_cosine(job_embedding, resume_embedding))

        if len(scores) < 10:
            print(json.dumps({"error": "insufficient_pairs"}, ensure_ascii=True))
            return

        scores.sort()
        min_sim = scores[int(len(scores) * 0.05)]
        max_sim = scores[int(len(scores) * 0.95)]
        row = await db.get(EmbeddingCalibration, 1)
        if row is None:
            row = EmbeddingCalibration(id=1, min_similarity=min_sim, max_similarity=max_sim, model_name="all-MiniLM-L6-v2")
            db.add(row)
        else:
            row.min_similarity = min_sim
            row.max_similarity = max_sim
        await db.commit()
        print(json.dumps({"pairs": len(scores), "min_similarity": min_sim, "max_similarity": max_sim}, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calibrate embedding similarity bounds")
    parser.add_argument("--sample-size", type=int, default=200)
    args = parser.parse_args()
    asyncio.run(main(sample_size=args.sample_size))
