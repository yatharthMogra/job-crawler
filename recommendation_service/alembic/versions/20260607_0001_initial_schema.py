"""Initial recommendation service schema."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "20260607_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_pool_subscriptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("candidate_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("pool_name", sa.String(length=128), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidates.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("candidate_id", "pool_name", name="uq_user_pool_subscriptions_candidate_pool"),
    )
    op.create_index(
        "ix_user_pool_subscriptions_candidate_id",
        "user_pool_subscriptions",
        ["candidate_id"],
        unique=False,
    )

    op.create_table(
        "notification_batches",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("candidate_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("triggered_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("jobs_in_pools", sa.Integer(), nullable=True),
        sa.Column("jobs_after_filter", sa.Integer(), nullable=True),
        sa.Column("jobs_new_since_last", sa.Integer(), nullable=True),
        sa.Column("jobs_ranked", sa.Integer(), nullable=True),
        sa.Column("jobs_sent", sa.Integer(), nullable=True),
        sa.Column("skip_reason", sa.String(length=64), nullable=True),
        sa.Column("email_delivered", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidates.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_notification_batches_candidate_id", "notification_batches", ["candidate_id"], unique=False)

    op.create_table(
        "notification_job_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("candidate_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("batch_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("rank_in_batch", sa.Integer(), nullable=False),
        sa.Column("recommendation_score", sa.Float(), nullable=False),
        sa.Column("explanation", postgresql.ARRAY(sa.String(length=256)), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["batch_id"], ["notification_batches.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidates.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["job_id"], ["normalized_jobs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("candidate_id", "job_id", name="uq_notification_job_history_candidate_job"),
    )
    op.create_index(
        "ix_notification_job_history_candidate_id",
        "notification_job_history",
        ["candidate_id"],
        unique=False,
    )
    op.create_index(
        "ix_notification_job_history_batch_id",
        "notification_job_history",
        ["batch_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_notification_job_history_batch_id", table_name="notification_job_history")
    op.drop_index("ix_notification_job_history_candidate_id", table_name="notification_job_history")
    op.drop_table("notification_job_history")
    op.drop_index("ix_notification_batches_candidate_id", table_name="notification_batches")
    op.drop_table("notification_batches")
    op.drop_index("ix_user_pool_subscriptions_candidate_id", table_name="user_pool_subscriptions")
    op.drop_table("user_pool_subscriptions")
