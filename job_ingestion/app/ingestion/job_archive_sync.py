from __future__ import annotations

from typing import Any, Optional
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company
from app.models.job_archive import JobArchive
from app.models.normalized_job import NormalizedJob


def _archive_values_from_deterministic(
    det_fields: dict[str, Any],
    company: Company,
    *,
    description_text: Optional[str] = None,
) -> dict[str, Any]:
    return {
        "external_job_id": det_fields["external_job_id"],
        "company_id": company.id,
        "company_name": company.name,
        "platform": company.platform,
        "title": det_fields.get("title"),
        "location": det_fields.get("location"),
        "department": det_fields.get("department"),
        "posting_url": det_fields.get("posting_url"),
        "employment_type": det_fields.get("employment_type"),
        "salary_min": det_fields.get("salary_min"),
        "salary_max": det_fields.get("salary_max"),
        "original_posted_at": det_fields.get("posted_at"),
        "description_text": description_text,
    }


def _archive_conflict_update(
    det_fields: dict[str, Any],
    *,
    description_text: Optional[str] = None,
) -> dict[str, Any]:
    return {
        "title": det_fields.get("title"),
        "location": det_fields.get("location"),
        "department": det_fields.get("department"),
        "posting_url": det_fields.get("posting_url"),
        "employment_type": det_fields.get("employment_type"),
        "salary_min": det_fields.get("salary_min"),
        "salary_max": det_fields.get("salary_max"),
        "original_posted_at": det_fields.get("posted_at"),
        "description_text": description_text,
    }


async def upsert_job_archive_from_deterministic(
    db: AsyncSession,
    det_fields: dict[str, Any],
    company: Company,
    *,
    description_text: Optional[str] = None,
) -> UUID:
    values = _archive_values_from_deterministic(
        det_fields, company, description_text=description_text
    )
    stmt = (
        pg_insert(JobArchive)
        .values(**values)
        .on_conflict_do_update(
            index_elements=["external_job_id", "company_id"],
            set_=_archive_conflict_update(det_fields, description_text=description_text),
        )
        .returning(JobArchive.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one()


async def upsert_job_archive_from_normalized(
    db: AsyncSession,
    normalized: NormalizedJob,
    company: Company,
) -> UUID:
    det_fields = {
        "external_job_id": normalized.external_job_id,
        "title": normalized.title,
        "location": normalized.location,
        "department": normalized.department,
        "posting_url": normalized.posting_url,
        "employment_type": normalized.employment_type,
        "posted_at": normalized.posted_at,
        "salary_min": normalized.salary_min,
        "salary_max": normalized.salary_max,
    }
    values = _archive_values_from_deterministic(
        det_fields, company, description_text=normalized.description_text
    )
    values.update(
        {
            "seniority": normalized.seniority,
            "normalized_roles": normalized.normalized_roles or None,
            "job_capabilities": normalized.job_capabilities or None,
            "skills": normalized.skills or None,
            "tech_stack": normalized.tech_stack or None,
            "remote_type": normalized.remote_type,
        }
    )
    conflict_update = _archive_conflict_update(
        det_fields, description_text=normalized.description_text
    )
    conflict_update.update(
        {
            "seniority": normalized.seniority,
            "normalized_roles": normalized.normalized_roles or None,
            "job_capabilities": normalized.job_capabilities or None,
            "skills": normalized.skills or None,
            "tech_stack": normalized.tech_stack or None,
            "remote_type": normalized.remote_type,
            "salary_min": normalized.salary_min,
            "salary_max": normalized.salary_max,
        }
    )
    stmt = (
        pg_insert(JobArchive)
        .values(**values)
        .on_conflict_do_update(
            index_elements=["external_job_id", "company_id"],
            set_=conflict_update,
        )
        .returning(JobArchive.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one()


async def update_job_archive_after_enrichment(
    db: AsyncSession,
    job_archive_id: UUID,
    *,
    seniority: str,
    normalized_roles: list[str],
    job_capabilities: list[str],
    skills: list[str],
    tech_stack: list[str],
    remote_type: str,
    salary_min: Optional[int],
    salary_max: Optional[int],
    job_domain: Optional[str] = None,
    job_secondary_domain: Optional[str] = None,
) -> None:
    await db.execute(
        update(JobArchive)
        .where(JobArchive.id == job_archive_id)
        .values(
            seniority=seniority,
            normalized_roles=normalized_roles or None,
            job_capabilities=job_capabilities or None,
            skills=skills or None,
            tech_stack=tech_stack or None,
            remote_type=remote_type,
            salary_min=salary_min,
            salary_max=salary_max,
            job_domain=job_domain,
            job_secondary_domain=job_secondary_domain,
        )
    )


async def update_job_archive_from_normalized_fields(
    db: AsyncSession,
    job_archive_id: UUID,
    normalized: NormalizedJob,
) -> None:
    await update_job_archive_after_enrichment(
        db,
        job_archive_id,
        seniority=normalized.seniority,
        normalized_roles=list(normalized.normalized_roles),
        job_capabilities=list(normalized.job_capabilities),
        skills=list(normalized.skills),
        tech_stack=list(normalized.tech_stack),
        remote_type=normalized.remote_type,
        salary_min=normalized.salary_min,
        salary_max=normalized.salary_max,
        job_domain=normalized.job_domain,
        job_secondary_domain=normalized.job_secondary_domain,
    )
