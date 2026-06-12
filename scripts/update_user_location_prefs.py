#!/usr/bin/env python3
"""Set structured location preferences on current candidate profiles."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "job_ingestion"))

import os

os.chdir(ROOT / "job_ingestion")

from sqlalchemy import text

from app.database import AsyncSessionLocal

UPDATES = {
    "yatharthmogra@gmail.com": {
        "preferred_countries": ["US"],
        "preferred_states": ["NY"],
        "preferred_cities": ["New York"],
    },
    "ramparekh208@gmail.com": {
        "preferred_countries": ["US"],
    },
}


async def main() -> None:
    async with AsyncSessionLocal() as db:
        for email, prefs_patch in UPDATES.items():
            row = (
                await db.execute(
                    text(
                        """
                        SELECT cp.id, cp.preferences
                        FROM candidate_profiles cp
                        JOIN candidates c ON c.id = cp.candidate_id
                        WHERE c.email = :email AND cp.is_current = TRUE
                        """
                    ),
                    {"email": email},
                )
            ).one_or_none()
            if row is None:
                print(f"skip {email}: no current profile")
                continue
            profile_id, preferences = row
            merged = dict(preferences or {})
            merged.update(prefs_patch)
            await db.execute(
                text(
                    "UPDATE candidate_profiles SET preferences = CAST(:prefs AS jsonb) WHERE id = :id"
                ),
                {"prefs": json.dumps(merged), "id": profile_id},
            )
            print(f"updated {email}: {prefs_patch}")
        await db.commit()


if __name__ == "__main__":
    asyncio.run(main())
