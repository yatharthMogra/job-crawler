"""Email alert tier fields and company watch pending queue."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "20260705_0003"
down_revision = "20260630_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "notification_preferences",
        sa.Column("company_watch_cadence_minutes", sa.Integer(), nullable=False, server_default=sa.text("360")),
    )
    op.add_column(
        "notification_preferences",
        sa.Column("max_emails_per_day", sa.Integer(), nullable=False, server_default=sa.text("3")),
    )
    op.add_column(
        "notification_preferences",
        sa.Column("last_company_watch_batch_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "notification_preferences",
        sa.Column("next_company_watch_due_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_notification_preferences_next_company_watch_due_at",
        "notification_preferences",
        ["next_company_watch_due_at"],
        unique=False,
    )

    op.create_table(
        "company_watch_pending_alerts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("candidate_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "enqueued_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("included_in_batch_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidates.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["job_id"], ["normalized_jobs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["included_in_batch_id"], ["notification_batches.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "candidate_id",
            "job_id",
            name="uq_company_watch_pending_alerts_candidate_job",
        ),
    )
    op.create_index(
        "ix_company_watch_pending_alerts_candidate_id",
        "company_watch_pending_alerts",
        ["candidate_id"],
        unique=False,
    )
    op.create_index(
        "ix_company_watch_pending_alerts_pending",
        "company_watch_pending_alerts",
        ["candidate_id", "included_in_batch_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_company_watch_pending_alerts_pending", table_name="company_watch_pending_alerts")
    op.drop_index("ix_company_watch_pending_alerts_candidate_id", table_name="company_watch_pending_alerts")
    op.drop_table("company_watch_pending_alerts")
    op.drop_index(
        "ix_notification_preferences_next_company_watch_due_at",
        table_name="notification_preferences",
    )
    op.drop_column("notification_preferences", "next_company_watch_due_at")
    op.drop_column("notification_preferences", "last_company_watch_batch_at")
    op.drop_column("notification_preferences", "max_emails_per_day")
    op.drop_column("notification_preferences", "company_watch_cadence_minutes")
