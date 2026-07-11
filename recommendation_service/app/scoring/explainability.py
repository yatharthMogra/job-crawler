from __future__ import annotations

from typing import Any

from app.models.shared import NormalizedJob
from app.scoring.coverage import flatten_skills
from app.services.profile_loader import UserProfile


def generate_explanations(job: NormalizedJob, user_profile: UserProfile) -> list[str]:
    reasons: list[str] = []

    user_cap_names = {cap.capability_name for cap in user_profile.capabilities}
    for cap in job.job_capabilities:
        if cap in user_cap_names:
            reasons.append(cap)

    all_user_skills = flatten_skills(user_profile.skills)
    user_skills_lower = {skill.lower(): skill for skill in all_user_skills}
    for skill in job.tech_stack:
        if skill.lower() in user_skills_lower:
            reasons.append(skill)
        if len(reasons) >= 5:
            break

    if len(reasons) < 3:
        user_keywords = _collect_evidence_keywords(user_profile.evidence)
        for kw in job.skills:
            if kw.lower() in {keyword.lower() for keyword in user_keywords}:
                reasons.append(kw)
            if len(reasons) >= 5:
                break

    return reasons[:5]


def _collect_evidence_keywords(evidence: list[Any]) -> list[str]:
    keywords: list[str] = []
    for item in evidence:
        data = item.normalized_data or {}
        item_keywords = data.get("evidence_keywords")
        if isinstance(item_keywords, list):
            keywords.extend(str(keyword) for keyword in item_keywords)
    return keywords
