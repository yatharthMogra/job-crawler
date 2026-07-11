#!/usr/bin/env python3
"""Fit qualification-score display bounds from real candidate/job pairs."""

from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from sqlalchemy import func, select

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.config import get_settings  # noqa: E402
from app.database import AsyncSessionLocal  # noqa: E402
from app.models.shared import CandidateProfile, NormalizedJob, QualificationFitCalibration  # noqa: E402
from app.scoring.bm25_corpus import load_idf_cache  # noqa: E402
from app.scoring.qualification_fit import compute_qualification_fit  # noqa: E402
from app.services.profile_loader import load_user_profile  # noqa: E402
from app.services.term_embedding import embed_term  # noqa: E402


async def calibrate(candidate_limit: int, job_limit: int) -> None:
    settings = get_settings().model_copy(update={"qualification_fit_shadow_mode": False})
    async with AsyncSessionLocal() as db:
        await load_idf_cache(db)
        candidate_ids = list(
            (
                await db.scalars(
                    select(CandidateProfile.candidate_id)
                    .where(CandidateProfile.is_current.is_(True))
                    .order_by(func.random())
                    .limit(candidate_limit)
                )
            ).all()
        )
        jobs = list(
            (
                await db.scalars(
                    select(NormalizedJob)
                    .where(
                        NormalizedJob.is_active.is_(True),
                        NormalizedJob.processing_state == "success",
                    )
                    .order_by(func.random())
                    .limit(job_limit)
                )
            ).all()
        )

        scores: list[float] = []
        embed_cache: dict[str, list[float] | None] = {}
        for candidate_id in candidate_ids:
            profile = await load_user_profile(db, candidate_id)
            if profile is None:
                continue
            for job in jobs:
                scores.append(
                    compute_qualification_fit(
                        job,
                        profile,
                        settings,
                        embed_fn=embed_term,
                        embed_cache=embed_cache,
                    ).raw
                )

        if not scores:
            raise RuntimeError("No candidate/job pairs were available for calibration")

        raw_p5, raw_p95 = (float(value) for value in np.percentile(scores, [5, 95]))
        calibration = await db.get(QualificationFitCalibration, 1)
        if calibration is None:
            calibration = QualificationFitCalibration(id=1)
            db.add(calibration)
        calibration.raw_p5 = raw_p5
        calibration.raw_p95 = raw_p95
        calibration.sample_size = len(scores)
        calibration.updated_at = datetime.now(timezone.utc)
        await db.commit()

        print(
            f"Stored qualification calibration: p5={raw_p5:.4f}, "
            f"p95={raw_p95:.4f}, samples={len(scores)}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=int, default=50)
    parser.add_argument("--jobs", type=int, default=100)
    args = parser.parse_args()
    asyncio.run(calibrate(args.candidates, args.jobs))


if __name__ == "__main__":
    main()
