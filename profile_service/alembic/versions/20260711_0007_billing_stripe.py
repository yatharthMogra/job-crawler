"""Add Stripe billing fields and billing_events table.

Revision ID: 20260711_0007
Revises: 20260710_0006
Create Date: 2026-07-11 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260711_0007"
down_revision: str = "20260710_0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "candidates",
        sa.Column("stripe_customer_id", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "candidates",
        sa.Column("stripe_subscription_id", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "candidates",
        sa.Column(
            "subscription_status",
            sa.String(length=32),
            nullable=False,
            server_default="none",
        ),
    )
    op.create_index(
        "ix_candidates_stripe_customer_id",
        "candidates",
        ["stripe_customer_id"],
        unique=True,
    )
    op.create_index(
        "ix_candidates_stripe_subscription_id",
        "candidates",
        ["stripe_subscription_id"],
        unique=False,
    )

    op.create_table(
        "billing_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("candidate_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("stripe_event_id", sa.String(length=255), nullable=False),
        sa.Column("event_type", sa.String(length=128), nullable=False),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidates.id"]),
        sa.UniqueConstraint("stripe_event_id", name="uq_billing_events_stripe_event_id"),
    )
    op.create_index("ix_billing_events_candidate_id", "billing_events", ["candidate_id"])


def downgrade() -> None:
    op.drop_index("ix_billing_events_candidate_id", table_name="billing_events")
    op.drop_table("billing_events")
    op.drop_index("ix_candidates_stripe_subscription_id", table_name="candidates")
    op.drop_index("ix_candidates_stripe_customer_id", table_name="candidates")
    op.drop_column("candidates", "subscription_status")
    op.drop_column("candidates", "stripe_subscription_id")
    op.drop_column("candidates", "stripe_customer_id")
