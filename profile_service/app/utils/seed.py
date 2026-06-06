"""Seed test candidates with pre-built profiles."""

from __future__ import annotations

import asyncio
import uuid
from datetime import UTC, datetime

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models.candidate import Candidate
from app.models.capability import CandidateCapability
from app.models.profile import CandidateProfile


SEED_CANDIDATES = [
    {
        "email": "alice.dev@example.com",
        "name": "Alice Chen",
        "skills": {
            "languages": ["Python", "TypeScript"],
            "frameworks": ["FastAPI", "React"],
            "databases": ["PostgreSQL"],
            "cloud": ["AWS"],
            "ai_ml": ["RAG", "LLMs"],
            "infrastructure": ["Docker", "Kafka"],
            "product": [],
        },
        "education": {
            "degree": "MS Computer Science",
            "university": "NYU",
            "graduation_date": "2027-05",
        },
        "constraints": {
            "sponsorship_required": True,
            "visa_type": "F1",
            "work_authorization": "CPT_OPT",
            "internship_only": True,
            "fulltime_only": False,
            "minimum_salary": None,
            "minimum_hourly_rate": 25,
        },
        "preferences": {
            "primary_roles": ["Software Engineer Intern", "AI Engineer Intern"],
            "secondary_roles": ["Data Scientist Intern"],
            "preferred_locations": ["NYC", "Remote"],
            "acceptable_locations": ["New Jersey"],
            "remote_preference": "Hybrid",
            "relocation_allowed": True,
            "preferred_company_stages": ["Startup", "Growth Stage"],
            "preferred_industries": ["AI", "FinTech"],
        },
        "capabilities": [
            ("Backend Engineering", ["FastAPI", "PostgreSQL", "Kafka"]),
            ("AI Systems", ["RAG", "LLMs"]),
        ],
    },
    {
        "email": "bob.fullstack@example.com",
        "name": "Bob Martinez",
        "skills": {
            "languages": ["JavaScript", "Python"],
            "frameworks": ["React", "Node.js"],
            "databases": ["MongoDB"],
            "cloud": ["Google Cloud"],
            "ai_ml": [],
            "infrastructure": ["Kubernetes"],
            "product": ["Rapid Prototyping"],
        },
        "education": {
            "degree": "B.Tech Computer Science",
            "university": "IIT Mandi",
            "graduation_date": "2024-06",
        },
        "constraints": {
            "sponsorship_required": False,
            "visa_type": None,
            "work_authorization": None,
            "internship_only": False,
            "fulltime_only": True,
            "minimum_salary": 120000,
            "minimum_hourly_rate": None,
        },
        "preferences": {
            "primary_roles": ["Full Stack Engineer"],
            "secondary_roles": ["Frontend Engineer"],
            "preferred_locations": ["Remote"],
            "acceptable_locations": [],
            "remote_preference": "Remote",
            "relocation_allowed": False,
            "preferred_company_stages": ["Growth Stage"],
            "preferred_industries": ["SaaS"],
        },
        "capabilities": [
            ("Full Stack Development", ["React", "Node.js"]),
            ("Frontend Engineering", ["React"]),
        ],
    },
]


async def seed() -> None:
    async with AsyncSessionLocal() as db:
        for entry in SEED_CANDIDATES:
            existing = await db.execute(select(Candidate).where(Candidate.email == entry["email"]))
            if existing.scalar_one_or_none():
                continue

            candidate = Candidate(email=entry["email"], name=entry["name"])
            db.add(candidate)
            await db.flush()

            profile = CandidateProfile(
                candidate_id=candidate.id,
                version=1,
                is_current=True,
                schema_version="v1",
                constraints=entry["constraints"],
                preferences=entry["preferences"],
                skills=entry["skills"],
                education=entry["education"],
                patch_id=None,
            )
            db.add(profile)

            for name, evidence in entry["capabilities"]:
                db.add(
                    CandidateCapability(
                        candidate_id=candidate.id,
                        profile_version=1,
                        taxonomy_version="v1",
                        capability_name=name,
                        supporting_evidence=evidence,
                        computed_at=datetime.now(UTC),
                    )
                )

        await db.commit()


def main() -> None:
    asyncio.run(seed())
    print("Seed complete.")


if __name__ == "__main__":
    main()
