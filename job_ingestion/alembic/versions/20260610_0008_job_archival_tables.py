"""job archival tables

Revision ID: 20260610_0008
Revises: 20260607_0007
Create Date: 2026-06-10 12:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260610_0008"
down_revision: str = "20260607_0007"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "job_archive",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("external_job_id", sa.String(length=255), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("platform", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("department", sa.String(length=255), nullable=True),
        sa.Column("posting_url", sa.Text(), nullable=True),
        sa.Column("employment_type", sa.String(length=255), nullable=True),
        sa.Column("salary_min", sa.Integer(), nullable=True),
        sa.Column("salary_max", sa.Integer(), nullable=True),
        sa.Column("original_posted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("seniority", sa.String(length=64), nullable=True),
        sa.Column("normalized_roles", postgresql.ARRAY(sa.String(length=64)), nullable=True),
        sa.Column("job_capabilities", postgresql.ARRAY(sa.String(length=128)), nullable=True),
        sa.Column("skills", postgresql.ARRAY(sa.String(length=128)), nullable=True),
        sa.Column("tech_stack", postgresql.ARRAY(sa.String(length=128)), nullable=True),
        sa.Column("remote_type", sa.String(length=32), nullable=True),
        sa.Column("description_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("external_job_id", "company_id", name="uq_job_archive_external_company"),
    )
    op.create_index("idx_job_archive_company_id", "job_archive", ["company_id"])
    op.create_index("idx_job_archive_original_posted_at", "job_archive", ["original_posted_at"])

    op.add_column(
        "normalized_jobs",
        sa.Column("job_archive_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("job_archive.id"), nullable=True),
    )
    op.create_index("idx_normalized_jobs_job_archive_id", "normalized_jobs", ["job_archive_id"])

    op.create_table(
        "user_applications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("candidate_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("candidates.id"), nullable=False),
        sa.Column(
            "job_archive_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("job_archive.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("job_title", sa.String(length=512), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("platform", sa.String(length=64), nullable=True),
        sa.Column("external_job_id", sa.String(length=255), nullable=True),
        sa.Column("applied_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="applied"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("candidate_id", "job_archive_id", name="uq_user_applications_candidate_archive"),
    )
    op.create_index("idx_user_applications_candidate_id", "user_applications", ["candidate_id"])
    op.create_index("idx_user_applications_applied_at", "user_applications", ["applied_at"])


def downgrade() -> None:
    op.drop_index("idx_user_applications_applied_at", table_name="user_applications")
    op.drop_index("idx_user_applications_candidate_id", table_name="user_applications")
    op.drop_table("user_applications")

    op.drop_index("idx_normalized_jobs_job_archive_id", table_name="normalized_jobs")
    op.drop_column("normalized_jobs", "job_archive_id")

    op.drop_index("idx_job_archive_original_posted_at", table_name="job_archive")
    op.drop_index("idx_job_archive_company_id", table_name="job_archive")
    op.drop_table("job_archive")
