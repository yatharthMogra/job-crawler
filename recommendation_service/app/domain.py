"""Domain filter helpers for recommendation retrieval."""

from __future__ import annotations

from typing import Any

from sqlalchemy import or_

from app.models.shared import NormalizedJob


def candidate_domains_from_profile(
    primary_domain: str | None,
    secondary_domain: str | None,
) -> list[str]:
    domains: list[str] = []
    for domain in (primary_domain, secondary_domain):
        if domain and domain != "Other":
            domains.append(domain)
    return domains


def build_domain_filters(candidate_domains: list[str]) -> list[Any]:
    if not candidate_domains:
        return []
    return [
        or_(
            NormalizedJob.job_domain.in_(candidate_domains),
            NormalizedJob.job_secondary_domain.in_(candidate_domains),
        )
    ]
