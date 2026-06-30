"""Notification channels: digest preferences, company watch, job events."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "20260630_0002"
down_revision = "20260607_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "notification_preferences",
        sa.Column("candidate_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("digest_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("company_watch_enabled", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("cadence_hours", sa.Integer(), nullable=False, server_default=sa.text("24")),
        sa.Column("top_k", sa.Integer(), nullable=False, server_default=sa.text("4")),
        sa.Column("digest_filters", postgresql.JSONB(), nullable=True),
        sa.Column("last_digest_sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_digest_due_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidates.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("candidate_id"),
    )
    op.create_index(
        "ix_notification_preferences_next_digest_due_at",
        "notification_preferences",
        ["next_digest_due_at"],
        unique=False,
    )

    op.create_table(
        "company_watch_subscriptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("candidate_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidates.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "candidate_id",
            "company_id",
            name="uq_company_watch_subscriptions_candidate_company",
        ),
    )
    op.create_index(
        "ix_company_watch_subscriptions_candidate_id",
        "company_watch_subscriptions",
        ["candidate_id"],
        unique=False,
    )
    op.create_index(
        "ix_company_watch_subscriptions_company_id",
        "company_watch_subscriptions",
        ["company_id"],
        unique=False,
    )

    op.create_table(
        "notification_job_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "enqueued_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error", sa.String(length=512), nullable=True),
        sa.ForeignKeyConstraint(["job_id"], ["normalized_jobs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_notification_job_events_pending",
        "notification_job_events",
        ["processed_at", "enqueued_at"],
        unique=False,
    )

    op.add_column(
        "notification_batches",
        sa.Column("channel", sa.String(length=32), nullable=False, server_default="digest"),
    )
    op.add_column(
        "notification_job_history",
        sa.Column("channel", sa.String(length=32), nullable=False, server_default="digest"),
    )
    op.drop_constraint(
        "uq_notification_job_history_candidate_job",
        "notification_job_history",
        type_="unique",
    )
    op.create_unique_constraint(
        "uq_notification_job_history_candidate_job_channel",
        "notification_job_history",
        ["candidate_id", "job_id", "channel"],
    )

    op.execute(
        """
        INSERT INTO notification_preferences (candidate_id, digest_enabled, cadence_hours, top_k, next_digest_due_at)
        SELECT DISTINCT ups.candidate_id, true, 24, 4, NOW()
        FROM user_pool_subscriptions ups
        WHERE ups.is_active = true
        ON CONFLICT (candidate_id) DO NOTHING
        """
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_notification_job_history_candidate_job_channel",
        "notification_job_history",
        type_="unique",
    )
    op.create_unique_constraint(
        "uq_notification_job_history_candidate_job",
        "notification_job_history",
        ["candidate_id", "job_id"],
    )
    op.drop_column("notification_job_history", "channel")
    op.drop_column("notification_batches", "channel")
    op.drop_index("ix_notification_job_events_pending", table_name="notification_job_events")
    op.drop_table("notification_job_events")
    op.drop_index("ix_company_watch_subscriptions_company_id", table_name="company_watch_subscriptions")
    op.drop_index("ix_company_watch_subscriptions_candidate_id", table_name="company_watch_subscriptions")
    op.drop_table("company_watch_subscriptions")
    op.drop_index("ix_notification_preferences_next_digest_due_at", table_name="notification_preferences")
    op.drop_table("notification_preferences")
