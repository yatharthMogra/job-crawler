"""v2.1 schema foundation

Revision ID: 20260525_0003
Revises: 20260525_0002
Create Date: 2026-05-25 18:30:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "20260525_0003"
down_revision: str | None = "20260525_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("companies", sa.Column("platform_config", postgresql.JSONB(astext_type=sa.Text()), nullable=True))

    op.add_column(
        "normalized_jobs",
        sa.Column("processing_state", sa.String(length=32), nullable=False, server_default=sa.text("'pending'")),
    )
    op.add_column("normalized_jobs", sa.Column("failure_reason", sa.String(length=64), nullable=True))
    op.add_column("normalized_jobs", sa.Column("last_failure_at", sa.DateTime(timezone=True), nullable=True))

    op.create_table(
        "job_enrichments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "normalized_job_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("normalized_jobs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "raw_job_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("raw_jobs.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("llm_provider", sa.String(length=64), nullable=True),
        sa.Column("llm_model", sa.String(length=128), nullable=True),
        sa.Column("extraction_version", sa.String(length=32), nullable=True),
        sa.Column("seniority", sa.String(length=64), nullable=True),
        sa.Column("is_internship", sa.Boolean(), nullable=True),
        sa.Column("is_new_grad", sa.Boolean(), nullable=True),
        sa.Column("sponsorship_status", sa.String(length=32), nullable=True),
        sa.Column("sponsorship_confidence", sa.String(length=16), nullable=True),
        sa.Column("remote_type", sa.String(length=32), nullable=True),
        sa.Column("tech_stack", postgresql.ARRAY(sa.String(length=128)), nullable=False, server_default="{}"),
        sa.Column("skills", postgresql.ARRAY(sa.String(length=128)), nullable=False, server_default="{}"),
        sa.Column("input_tokens", sa.Integer(), nullable=True),
        sa.Column("output_tokens", sa.Integer(), nullable=True),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("failure_reason", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_job_enrichments_normalized_job_id", "job_enrichments", ["normalized_job_id"])
    op.create_index("ix_job_enrichments_created_at", "job_enrichments", ["created_at"])

    op.create_table(
        "ingestion_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("event_category", sa.String(length=32), nullable=False),
        sa.Column("severity", sa.String(length=16), nullable=False),
        sa.Column("platform", sa.String(length=64), nullable=True),
        sa.Column(
            "company_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("companies.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "pipeline_run_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("pipeline_runs.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "normalized_job_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("normalized_jobs.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_ingestion_events_event_category_created_at", "ingestion_events", ["event_category", "created_at"])
    op.create_index("ix_ingestion_events_company_id_created_at", "ingestion_events", ["company_id", "created_at"])
    op.create_index("ix_ingestion_events_pipeline_run_id", "ingestion_events", ["pipeline_run_id"])


def downgrade() -> None:
    op.drop_index("ix_ingestion_events_pipeline_run_id", table_name="ingestion_events")
    op.drop_index("ix_ingestion_events_company_id_created_at", table_name="ingestion_events")
    op.drop_index("ix_ingestion_events_event_category_created_at", table_name="ingestion_events")
    op.drop_table("ingestion_events")

    op.drop_index("ix_job_enrichments_created_at", table_name="job_enrichments")
    op.drop_index("ix_job_enrichments_normalized_job_id", table_name="job_enrichments")
    op.drop_table("job_enrichments")

    op.drop_column("normalized_jobs", "last_failure_at")
    op.drop_column("normalized_jobs", "failure_reason")
    op.drop_column("normalized_jobs", "processing_state")

    op.drop_column("companies", "platform_config")
