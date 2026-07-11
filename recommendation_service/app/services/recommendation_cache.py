"""Redis-backed recommendation session cache (reference-token pagination)."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from types import SimpleNamespace
from typing import Any

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.models.shared import CandidateProfile
from app.services.profile_loader import UserProfile
from app.services.recommendation_pipeline import AuxSnapshot, PipelineResult, RankedJobEntry
from app.services.redis_client import get_redis
from app.services.resume_embedding_loader import load_resume_fingerprint

log = structlog.get_logger(__name__)

CACHE_KEY_PREFIX = "rec:session:"


@dataclass
class CachedRecommendationSession:
    candidate_id: uuid.UUID
    profile_version: int
    resume_fingerprint: str
    ranked_entries: list[RankedJobEntry]
    profile_snapshot: dict[str, Any]
    aux_snapshot: AuxSnapshot
    created_at: str
    reference_token: str = ""


def _serialize_profile(profile: UserProfile) -> dict[str, Any]:
    return {
        "candidate_id": str(profile.candidate_id),
        "email": profile.email,
        "name": profile.name,
        "constraints": profile.constraints or {},
        "preferences": profile.preferences or {},
        "skills": profile.skills or {},
        "education": profile.education or {},
        "primary_domain": profile.primary_domain,
        "secondary_domain": profile.secondary_domain,
        "capabilities": [
            {
                "id": str(cap.id),
                "capability_name": cap.capability_name,
                "supporting_evidence": list(getattr(cap, "supporting_evidence", None) or []),
            }
            for cap in (profile.capabilities or [])
        ],
        "evidence": [
            {
                "id": str(ev.id),
                "evidence_type": getattr(ev, "evidence_type", ""),
                "normalized_data": getattr(ev, "normalized_data", None) or {},
                "raw_source_text": getattr(ev, "raw_source_text", None),
            }
            for ev in (profile.evidence or [])
        ],
    }


def deserialize_profile(snapshot: dict[str, Any]) -> UserProfile:
    capabilities = [
        SimpleNamespace(
            id=uuid.UUID(c["id"]),
            capability_name=c["capability_name"],
            supporting_evidence=c.get("supporting_evidence") or [],
        )
        for c in snapshot.get("capabilities") or []
    ]
    evidence = [
        SimpleNamespace(
            id=uuid.UUID(e["id"]),
            evidence_type=e.get("evidence_type", ""),
            normalized_data=e.get("normalized_data") or {},
            raw_source_text=e.get("raw_source_text"),
        )
        for e in snapshot.get("evidence") or []
    ]
    return UserProfile(
        candidate_id=uuid.UUID(snapshot["candidate_id"]),
        email=snapshot.get("email", ""),
        name=snapshot.get("name", ""),
        constraints=snapshot.get("constraints") or {},
        preferences=snapshot.get("preferences") or {},
        skills=snapshot.get("skills") or {},
        education=snapshot.get("education") or {},
        primary_domain=snapshot.get("primary_domain"),
        secondary_domain=snapshot.get("secondary_domain"),
        capabilities=capabilities,  # type: ignore[arg-type]
        evidence=evidence,  # type: ignore[arg-type]
    )


def _entries_to_json(entries: list[RankedJobEntry]) -> list[dict[str, Any]]:
    return [
        {
            "job_id": str(e.job_id),
            "personal_score": e.personal_score,
            "opportunity_score": e.opportunity_score,
            "reference_timestamp": e.reference_timestamp,
            "company_name": e.company_name,
        }
        for e in entries
    ]


def _entries_from_json(raw: list[dict[str, Any]]) -> list[RankedJobEntry]:
    return [
        RankedJobEntry(
            job_id=uuid.UUID(e["job_id"]),
            personal_score=float(e["personal_score"]),
            opportunity_score=float(e["opportunity_score"]),
            reference_timestamp=float(e["reference_timestamp"]),
            company_name=e.get("company_name", ""),
        )
        for e in raw
    ]


async def store_recommendation_session(
    result: PipelineResult,
    settings: Settings,
) -> str:
    token = str(uuid.uuid4())
    payload = {
        "candidate_id": str(result.profile.candidate_id),
        "profile_version": result.profile_version,
        "resume_fingerprint": result.resume_fingerprint,
        "ranked_entries": _entries_to_json(result.ranked_entries),
        "profile_snapshot": _serialize_profile(result.profile),
        "aux_snapshot": {"applied_counts": result.aux_snapshot.applied_counts},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "reference_token": token,
    }
    redis = get_redis()
    key = f"{CACHE_KEY_PREFIX}{token}"
    await redis.set(key, json.dumps(payload), ex=settings.recommendation_cache_ttl_seconds)
    log.info(
        "recommendation_cache_store",
        token=token,
        ranked=len(result.ranked_entries),
        ttl=settings.recommendation_cache_ttl_seconds,
    )
    return token


async def load_recommendation_session(
    token: str,
) -> CachedRecommendationSession | None:
    redis = get_redis()
    raw = await redis.get(f"{CACHE_KEY_PREFIX}{token}")
    if not raw:
        return None
    data = json.loads(raw)
    return CachedRecommendationSession(
        candidate_id=uuid.UUID(data["candidate_id"]),
        profile_version=int(data["profile_version"]),
        resume_fingerprint=data["resume_fingerprint"],
        ranked_entries=_entries_from_json(data["ranked_entries"]),
        profile_snapshot=data["profile_snapshot"],
        aux_snapshot=AuxSnapshot(
            applied_counts=data.get("aux_snapshot", {}).get("applied_counts") or {}
        ),
        created_at=data["created_at"],
        reference_token=token,
    )


async def delete_recommendation_session(token: str) -> None:
    redis = get_redis()
    await redis.delete(f"{CACHE_KEY_PREFIX}{token}")


async def session_is_stale(
    db: AsyncSession,
    session: CachedRecommendationSession,
) -> bool:
    """True if profile version or resume embeddings changed since cache write."""
    live_version = await db.scalar(
        select(CandidateProfile.version).where(
            CandidateProfile.candidate_id == session.candidate_id,
            CandidateProfile.is_current.is_(True),
        )
    )
    if live_version is not None and int(live_version) != session.profile_version:
        return True
    live_fp = await load_resume_fingerprint(db, session.candidate_id)
    return live_fp != session.resume_fingerprint
