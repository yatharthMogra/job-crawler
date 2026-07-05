"""gemini errors observability table

Revision ID: 20260705_0019
Revises: 20260703_0018
Create Date: 2026-07-05 12:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260705_0019"
down_revision: str = "20260703_0018"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "gemini_errors",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("assigned_failure_reason", sa.String(length=64), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=False),
        sa.Column("exception_type", sa.String(length=128), nullable=False),
        sa.Column("failure_stage", sa.String(length=32), nullable=False),
        sa.Column("call_site", sa.String(length=64), nullable=False),
        sa.Column("llm_provider", sa.String(length=32), nullable=True),
        sa.Column("llm_model", sa.String(length=128), nullable=True),
        sa.Column(
            "enrichment_batch_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("enrichment_batches.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "company_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("companies.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "normalized_job_ids",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("batch_size", sa.Integer(), nullable=True),
        sa.Column("source", sa.String(length=64), nullable=True),
        sa.Column(
            "error_metadata",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index(
        "ix_gemini_errors_assigned_failure_reason_created_at",
        "gemini_errors",
        ["assigned_failure_reason", "created_at"],
    )
    op.create_index(
        "ix_gemini_errors_failure_stage_created_at",
        "gemini_errors",
        ["failure_stage", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_gemini_errors_failure_stage_created_at", table_name="gemini_errors")
    op.drop_index("ix_gemini_errors_assigned_failure_reason_created_at", table_name="gemini_errors")
    op.drop_table("gemini_errors")
