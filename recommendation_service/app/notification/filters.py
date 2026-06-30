from __future__ import annotations

from typing import Any

from sqlalchemy import or_

from app.domain import build_domain_filters
from app.models.shared import NormalizedJob
from app.services.profile_loader import UserProfile


def build_digest_filters(
    digest_filters: dict[str, Any] | None,
    user_profile: UserProfile | None = None,
) -> list[Any]:
    """Optional digest-only filters layered on top of profile hard constraints."""
    if not digest_filters:
        return []

    filters: list[Any] = []

    locations = digest_filters.get("locations") or []
    if locations:
        location_clauses = [
            NormalizedJob.location.ilike(f"%{loc}%")
            for loc in locations
            if isinstance(loc, str) and loc.strip()
        ]
        if location_clauses:
            filters.append(or_(*location_clauses))

    minimum_salary = digest_filters.get("minimum_salary")
    if minimum_salary:
        filters.append(
            or_(
                NormalizedJob.salary_max.is_(None),
                NormalizedJob.salary_max >= minimum_salary,
            )
        )

    domains = digest_filters.get("domains") or []
    if domains:
        domain_values = [d for d in domains if isinstance(d, str) and d.strip()]
        if domain_values:
            filters.extend(build_domain_filters(domain_values))

    employment_type = digest_filters.get("employment_type")
    if employment_type == "internship":
        filters.append(NormalizedJob.is_internship.is_(True))
    elif employment_type == "fulltime":
        filters.append(NormalizedJob.is_internship.is_(False))

    return filters


def job_matches_location_constraints(job: NormalizedJob, user_profile: UserProfile) -> bool:
    """Hard location gate for Company Watch when user has location preferences."""
    from app.scoring.location import locations_match

    preferences = user_profile.preferences or {}
    constraints = user_profile.constraints or {}

    preferred_locations = preferences.get("preferred_locations") or []
    preferred_countries = preferences.get("preferred_countries") or []
    preferred_states = preferences.get("preferred_states") or []
    preferred_cities = preferences.get("preferred_cities") or []
    acceptable_locations = preferences.get("acceptable_locations") or []

    has_location_prefs = bool(
        preferred_locations
        or preferred_countries
        or preferred_states
        or preferred_cities
        or acceptable_locations
    )
    if not has_location_prefs:
        return True

    remote_type = job.remote_type or ""
    if remote_type == "remote":
        remote_pref = preferences.get("remote_preference")
        if remote_pref in ("remote_only", "remote_ok", "hybrid_ok"):
            return True

    all_locations = list(preferred_locations) + list(acceptable_locations)
    for loc in all_locations:
        if isinstance(loc, str) and locations_match(loc, job.location):
            return True

    if preferred_countries or preferred_states or preferred_cities:
        from app.scoring.country import extract_job_country, get_effective_countries
        from app.scoring.location import _extract_city, _extract_state

        effective_countries = get_effective_countries(preferences, constraints)
        if effective_countries:
            job_country = extract_job_country(job.location)
            if job_country and job_country not in effective_countries:
                return False
            if preferred_states:
                job_state = _extract_state(job.location)
                state_values = [str(s).upper() for s in preferred_states]
                if job_state and job_state.upper() in state_values:
                    if preferred_cities:
                        job_city = _extract_city(job.location)
                        city_values = [str(c).lower() for c in preferred_cities]
                        if job_city and job_city.lower() in city_values:
                            return True
                        return False
                    return True
                return False
            return job_country in effective_countries if job_country else False

    return False
