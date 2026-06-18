#!/usr/bin/env python3
"""Backfill primary_role_intents and sync pool_role_intents from active subscriptions."""

from __future__ import annotations

import asyncio
import json
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "recommendation_service"))

import os

os.chdir(ROOT / "recommendation_service")

from sqlalchemy import text

from app.database import AsyncSessionLocal
from app.services.role_intent_preferences import sync_pool_role_intents

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
                    SELECT cp.id, c.id, c.email, cp.preferences
                    FROM candidate_profiles cp
                    JOIN candidates c ON c.id = cp.candidate_id
                    WHERE cp.is_current = TRUE
                    """
                )
            )
        ).all()

        for profile_id, candidate_id, email, preferences in rows:
            merged_preferences = dict(preferences or {})
            if "primary_role_intents" not in merged_preferences:
                if "role_intents" in merged_preferences:
                    merged_preferences["primary_role_intents"] = merged_preferences["role_intents"]
                else:
                    merged_preferences["primary_role_intents"] = USER_ROLE_INTENTS.get(
                        email, DEFAULT_ROLE_INTENTS
                    )
                    merged_preferences["role_intents"] = merged_preferences["primary_role_intents"]

            await db.execute(
                text(
                    """
                    UPDATE candidate_profiles
                    SET preferences = CAST(:preferences AS jsonb)
                    WHERE id = :id
                    """
                ),
                {
                    "preferences": json.dumps(merged_preferences),
                    "id": profile_id,
                },
            )
            await db.commit()

            pool_intents = await sync_pool_role_intents(db, candidate_id=uuid.UUID(str(candidate_id)))
            await db.commit()
            print(
                f"updated {email}: primary_role_intents={merged_preferences['primary_role_intents']}, "
                f"pool_role_intents={pool_intents}"
            )


if __name__ == "__main__":
    asyncio.run(main())
