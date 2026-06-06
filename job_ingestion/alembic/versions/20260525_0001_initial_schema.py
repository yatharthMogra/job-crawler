"""initial schema

Revision ID: 20260525_0001
Revises:
Create Date: 2026-05-25 12:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "20260525_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("platform", sa.String(length=64), nullable=False),
        sa.Column("board_token", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("consecutive_fetch_failures", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("last_successful_fetch_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("board_token", name="uq_companies_board_token"),
    )
    op.create_index("ix_companies_board_token", "companies", ["board_token"])

    op.create_table(
        "pipeline_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("run_type", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("total_companies", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("successful_companies", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("failed_companies", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("jobs_fetched", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("jobs_new", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("jobs_updated", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("jobs_unchanged", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("jobs_removed", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("error_summary", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )

    op.create_table(
        "raw_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("external_job_id", sa.String(length=255), nullable=False),
        sa.Column("platform", sa.String(length=64), nullable=False),
        sa.Column("raw_api_response", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("raw_html", sa.Text(), nullable=True),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("fetch_timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_raw_jobs_company_id", "raw_jobs", ["company_id"])
    op.create_index("ix_raw_jobs_content_hash", "raw_jobs", ["content_hash"])
    op.create_index("ix_raw_jobs_company_external", "raw_jobs", ["company_id", "external_job_id"])

    op.create_table(
        "normalized_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("raw_job_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("raw_jobs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("external_job_id", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("department", sa.String(length=255), nullable=True),
        sa.Column("employment_type", sa.String(length=255), nullable=True),
        sa.Column("posting_url", sa.Text(), nullable=True),
        sa.Column("posted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("consecutive_misses", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("seniority", sa.String(length=64), nullable=False),
        sa.Column("is_internship", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_new_grad", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("sponsorship_status", sa.String(length=32), nullable=False),
        sa.Column("sponsorship_confidence", sa.String(length=16), nullable=False),
        sa.Column("remote_type", sa.String(length=32), nullable=False),
        sa.Column("tech_stack", postgresql.ARRAY(sa.String(length=128)), nullable=False),
        sa.Column("skills", postgresql.ARRAY(sa.String(length=128)), nullable=False),
        sa.Column("llm_provider", sa.String(length=64), nullable=True),
        sa.Column("llm_model", sa.String(length=128), nullable=True),
        sa.Column("extraction_version", sa.String(length=32), nullable=False),
        sa.Column("extracted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("company_id", "external_job_id", name="uq_normalized_jobs_company_external"),
    )
    op.create_index("ix_normalized_jobs_company_id", "normalized_jobs", ["company_id"])

    op.create_table(
        "company_run_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "pipeline_run_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("pipeline_runs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("jobs_fetched", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("jobs_new", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("jobs_updated", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("jobs_unchanged", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("jobs_removed", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_company_run_results_pipeline_run_id", "company_run_results", ["pipeline_run_id"])
    op.create_index("ix_company_run_results_company_id", "company_run_results", ["company_id"])


def downgrade() -> None:
    op.drop_index("ix_company_run_results_company_id", table_name="company_run_results")
    op.drop_index("ix_company_run_results_pipeline_run_id", table_name="company_run_results")
    op.drop_table("company_run_results")
    op.drop_index("ix_normalized_jobs_company_id", table_name="normalized_jobs")
    op.drop_table("normalized_jobs")
    op.drop_index("ix_raw_jobs_company_external", table_name="raw_jobs")
    op.drop_index("ix_raw_jobs_content_hash", table_name="raw_jobs")
    op.drop_index("ix_raw_jobs_company_id", table_name="raw_jobs")
    op.drop_table("raw_jobs")
    op.drop_table("pipeline_runs")
    op.drop_index("ix_companies_board_token", table_name="companies")
    op.drop_table("companies")
