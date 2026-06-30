#!/usr/bin/env python3
"""Backfill current_experience_tier on current candidate profiles."""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE_SERVICE = ROOT / "profile_service"
sys.path.insert(0, str(PROFILE_SERVICE))
os.chdir(PROFILE_SERVICE)

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.experience_tier_sync import refresh_experience_tier_constraints
from app.models.profile import CandidateProfile


async def backfill_profiles(*, dry_run: bool) -> int:
    updated = 0
    async with AsyncSessionLocal() as db:
        profiles = (
            await db.scalars(
                select(CandidateProfile).where(CandidateProfile.is_current.is_(True))
            )
        ).all()
        for profile in profiles:
            new_constraints = await refresh_experience_tier_constraints(
                db,
                candidate_id=profile.candidate_id,
                constraints=dict(profile.constraints or {}),
                education=dict(profile.education or {}),
            )
            if new_constraints.get("current_experience_tier") == (
                profile.constraints or {}
            ).get("current_experience_tier"):
                continue
            updated += 1
            if dry_run:
                print(
                    f"{profile.candidate_id}: "
                    f"{(profile.constraints or {}).get('current_experience_tier')} -> "
                    f"{new_constraints.get('current_experience_tier')}"
                )
                continue
            profile.constraints = new_constraints
        if not dry_run:
            await db.commit()
    return updated


async def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill candidate current_experience_tier")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    count = await backfill_profiles(dry_run=args.dry_run)
    print(f"{'Would update' if args.dry_run else 'Updated'} {count} profiles.")


if __name__ == "__main__":
    asyncio.run(main())
