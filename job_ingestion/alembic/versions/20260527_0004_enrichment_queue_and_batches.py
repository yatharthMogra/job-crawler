"""enrichment queue and batches

Revision ID: 20260527_0004
Revises: 20260525_0003
Create Date: 2026-05-27 10:55:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "20260527_0004"
down_revision: str = "20260525_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "enrichment_queue",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "normalized_job_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("normalized_jobs.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "pipeline_run_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("pipeline_runs.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("source", sa.String(length=32), nullable=False, server_default=sa.text("'pipeline'")),
        sa.Column("status", sa.String(length=32), nullable=False, server_default=sa.text("'queued'")),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("priority", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("next_retry_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("estimated_input_tokens", sa.Integer(), nullable=True),
        sa.Column("last_actual_input_tokens", sa.Integer(), nullable=True),
        sa.Column("last_actual_output_tokens", sa.Integer(), nullable=True),
        sa.Column("last_failure_reason", sa.String(length=64), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_enrichment_queue_normalized_job_id", "enrichment_queue", ["normalized_job_id"])
    op.create_index("ix_enrichment_queue_pipeline_run_id", "enrichment_queue", ["pipeline_run_id"])
    op.create_index("ix_enrichment_queue_status", "enrichment_queue", ["status"])
    op.create_index("ix_enrichment_queue_next_retry_at", "enrichment_queue", ["next_retry_at"])
    op.create_index("ix_enrichment_queue_created_at", "enrichment_queue", ["created_at"])
    op.create_index("ix_enrichment_queue_updated_at", "enrichment_queue", ["updated_at"])

    op.create_table(
        "enrichment_batches",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "pipeline_run_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("pipeline_runs.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("source", sa.String(length=32), nullable=False, server_default=sa.text("'worker'")),
        sa.Column("status", sa.String(length=32), nullable=False, server_default=sa.text("'running'")),
        sa.Column("jobs_total", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("jobs_first_attempt", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("jobs_retry", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("estimated_input_tokens", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("actual_input_tokens", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("actual_output_tokens", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("latency_ms", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("failure_reason", sa.String(length=64), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_enrichment_batches_pipeline_run_id", "enrichment_batches", ["pipeline_run_id"])
    op.create_index("ix_enrichment_batches_status", "enrichment_batches", ["status"])
    op.create_index("ix_enrichment_batches_started_at", "enrichment_batches", ["started_at"])
    op.create_index("ix_enrichment_batches_completed_at", "enrichment_batches", ["completed_at"])

    op.create_table(
        "enrichment_batch_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "batch_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("enrichment_batches.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "queue_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("enrichment_queue.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "normalized_job_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("normalized_jobs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("status", sa.String(length=32), nullable=False, server_default=sa.text("'pending'")),
        sa.Column("priority_bucket", sa.String(length=32), nullable=False, server_default=sa.text("'first_attempt'")),
        sa.Column("attempt_number", sa.Integer(), nullable=False, server_default=sa.text("1")),
        sa.Column("estimated_input_tokens", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("actual_input_tokens", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("actual_output_tokens", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("failure_reason", sa.String(length=64), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_enrichment_batch_items_batch_id", "enrichment_batch_items", ["batch_id"])
    op.create_index("ix_enrichment_batch_items_queue_id", "enrichment_batch_items", ["queue_id"])
    op.create_index("ix_enrichment_batch_items_normalized_job_id", "enrichment_batch_items", ["normalized_job_id"])
    op.create_index("ix_enrichment_batch_items_created_at", "enrichment_batch_items", ["created_at"])

    op.add_column("job_enrichments", sa.Column("enrichment_batch_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(
        "fk_job_enrichments_enrichment_batch_id",
        "job_enrichments",
        "enrichment_batches",
        ["enrichment_batch_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_job_enrichments_enrichment_batch_id", "job_enrichments", ["enrichment_batch_id"])


def downgrade() -> None:
    op.drop_index("ix_job_enrichments_enrichment_batch_id", table_name="job_enrichments")
    op.drop_constraint("fk_job_enrichments_enrichment_batch_id", "job_enrichments", type_="foreignkey")
    op.drop_column("job_enrichments", "enrichment_batch_id")

    op.drop_index("ix_enrichment_batch_items_created_at", table_name="enrichment_batch_items")
    op.drop_index("ix_enrichment_batch_items_normalized_job_id", table_name="enrichment_batch_items")
    op.drop_index("ix_enrichment_batch_items_queue_id", table_name="enrichment_batch_items")
    op.drop_index("ix_enrichment_batch_items_batch_id", table_name="enrichment_batch_items")
    op.drop_table("enrichment_batch_items")

    op.drop_index("ix_enrichment_batches_completed_at", table_name="enrichment_batches")
    op.drop_index("ix_enrichment_batches_started_at", table_name="enrichment_batches")
    op.drop_index("ix_enrichment_batches_status", table_name="enrichment_batches")
    op.drop_index("ix_enrichment_batches_pipeline_run_id", table_name="enrichment_batches")
    op.drop_table("enrichment_batches")

    op.drop_index("ix_enrichment_queue_updated_at", table_name="enrichment_queue")
    op.drop_index("ix_enrichment_queue_created_at", table_name="enrichment_queue")
    op.drop_index("ix_enrichment_queue_next_retry_at", table_name="enrichment_queue")
    op.drop_index("ix_enrichment_queue_status", table_name="enrichment_queue")
    op.drop_index("ix_enrichment_queue_pipeline_run_id", table_name="enrichment_queue")
    op.drop_index("ix_enrichment_queue_normalized_job_id", table_name="enrichment_queue")
    op.drop_table("enrichment_queue")
