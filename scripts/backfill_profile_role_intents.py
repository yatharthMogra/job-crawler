#!/usr/bin/env python3
"""Backfill has_clearance and role_intents on current candidate profiles."""

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

DEFAULT_ROLE_INTENTS = ["engineer", "researcher"]

USER_ROLE_INTENTS = {
    "yatharthmogra@gmail.com": ["engineer", "researcher"],
    "ramparekh208@gmail.com": ["engineer", "researcher", "analyst"],
}


async def main() -> None:
    async with AsyncSessionLocal() as db:
        rows = (
            await db.execute(
                text(
                    """
                    SELECT cp.id, c.email, cp.constraints, cp.preferences
                    FROM candidate_profiles cp
                    JOIN candidates c ON c.id = cp.candidate_id
                    WHERE cp.is_current = TRUE
                    """
                )
            )
        ).all()

        for profile_id, email, constraints, preferences in rows:
            merged_constraints = dict(constraints or {})
            if "has_clearance" not in merged_constraints:
                if merged_constraints.get("exclude_security_clearance"):
                    merged_constraints["has_clearance"] = False
                else:
                    merged_constraints["has_clearance"] = False

            merged_preferences = dict(preferences or {})
            if "role_intents" not in merged_preferences:
                merged_preferences["role_intents"] = USER_ROLE_INTENTS.get(
                    email, DEFAULT_ROLE_INTENTS
                )

            await db.execute(
                text(
                    """
                    UPDATE candidate_profiles
                    SET constraints = CAST(:constraints AS jsonb),
                        preferences = CAST(:preferences AS jsonb)
                    WHERE id = :id
                    """
                ),
                {
                    "constraints": json.dumps(merged_constraints),
                    "preferences": json.dumps(merged_preferences),
                    "id": profile_id,
                },
            )
            print(
                f"updated {email}: has_clearance={merged_constraints['has_clearance']}, "
                f"role_intents={merged_preferences['role_intents']}"
            )
        await db.commit()


if __name__ == "__main__":
    asyncio.run(main())
