from __future__ import annotations

import uuid
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shared import Company, JobArchive, NormalizedJob, UserApplication
from app.schemas.applications import UserApplicationOut, UserApplicationPatchIn


def format_application_row(
    application: UserApplication,
    *,
    archive: Optional[JobArchive],
    normalized_job_id: Optional[uuid.UUID] = None,
) -> UserApplicationOut:
    skills = list(archive.skills or []) if archive else []
    tech_stack = list(archive.tech_stack or []) if archive else []
    return UserApplicationOut(
        id=application.id,
        candidate_id=application.candidate_id,
        job_archive_id=application.job_archive_id,
        normalized_job_id=normalized_job_id,
        company_name=archive.company_name if archive else application.company_name,
        job_title=archive.title if archive and archive.title else application.job_title,
        location=archive.location if archive and archive.location else application.location,
        platform=archive.platform if archive else application.platform,
        external_job_id=archive.external_job_id if archive else application.external_job_id,
        posting_url=archive.posting_url if archive else None,
        salary_min=archive.salary_min if archive else None,
        salary_max=archive.salary_max if archive else None,
        seniority=archive.seniority if archive else None,
        skills=skills,
        tech_stack=tech_stack,
        description_text=archive.description_text if archive else None,
        applied_at=application.applied_at,
        status=application.status,
        notes=application.notes,
    )


async def get_user_applications(
    db: AsyncSession,
    candidate_id: uuid.UUID,
) -> list[UserApplicationOut]:
    result = await db.execute(
        select(UserApplication, JobArchive)
        .outerjoin(JobArchive, UserApplication.job_archive_id == JobArchive.id)
        .where(UserApplication.candidate_id == candidate_id)
        .order_by(UserApplication.applied_at.desc())
    )
    rows = result.all()
    normalized_ids: dict[uuid.UUID, uuid.UUID] = {}
    archive_ids = [
        application.job_archive_id for application, _archive in rows if application.job_archive_id
    ]
    if archive_ids:
        norm_rows = (
            await db.scalars(
                select(NormalizedJob).where(NormalizedJob.job_archive_id.in_(archive_ids))
            )
        ).all()
        for norm in norm_rows:
            if norm.job_archive_id is not None:
                normalized_ids[norm.job_archive_id] = norm.id

    return [
        format_application_row(
            application,
            archive=archive,
            normalized_job_id=normalized_ids.get(application.job_archive_id)
            if application.job_archive_id
            else None,
        )
        for application, archive in rows
    ]


async def applied_count_by_company(
    db: AsyncSession,
    candidate_id: uuid.UUID,
) -> dict[str, int]:
    rows = (
        await db.execute(
            select(func.lower(UserApplication.company_name), func.count())
            .where(UserApplication.candidate_id == candidate_id)
            .group_by(func.lower(UserApplication.company_name))
        )
    ).all()
    return {company: count for company, count in rows if company}


async def apply_to_job(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    job_id: uuid.UUID,
) -> UserApplicationOut:
    job = await db.scalar(select(NormalizedJob).where(NormalizedJob.id == job_id))
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if job.job_archive_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job archive not available for this job",
        )

    company = await db.scalar(select(Company).where(Company.id == job.company_id))
    platform = company.platform if company else None

    stmt = (
        pg_insert(UserApplication)
        .values(
            id=uuid.uuid4(),
            candidate_id=candidate_id,
            job_archive_id=job.job_archive_id,
            company_name=job.company_name,
            job_title=job.title,
            location=job.location,
            platform=platform,
            external_job_id=job.external_job_id,
        )
        .on_conflict_do_update(
            index_elements=["candidate_id", "job_archive_id"],
            set_={
                "company_name": job.company_name,
                "job_title": job.title,
                "location": job.location,
                "platform": platform,
                "external_job_id": job.external_job_id,
            },
        )
        .returning(UserApplication)
    )
    application = (await db.execute(stmt)).scalar_one()
    archive = await db.scalar(select(JobArchive).where(JobArchive.id == job.job_archive_id))
    await db.commit()
    await db.refresh(application)
    return format_application_row(application, archive=archive, normalized_job_id=job.id)


async def patch_application(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    application_id: uuid.UUID,
    payload: UserApplicationPatchIn,
) -> UserApplicationOut:
    application = await db.scalar(
        select(UserApplication).where(
            UserApplication.id == application_id,
            UserApplication.candidate_id == candidate_id,
        )
    )
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    patch_data = payload.model_dump(exclude_none=True)
    for key, value in patch_data.items():
        setattr(application, key, value)

    archive = None
    if application.job_archive_id is not None:
        archive = await db.scalar(select(JobArchive).where(JobArchive.id == application.job_archive_id))

    normalized_job_id = None
    if application.job_archive_id is not None:
        normalized_job_id = await db.scalar(
            select(NormalizedJob.id).where(NormalizedJob.job_archive_id == application.job_archive_id)
        )

    await db.commit()
    await db.refresh(application)
    return format_application_row(
        application,
        archive=archive,
        normalized_job_id=normalized_job_id,
    )
