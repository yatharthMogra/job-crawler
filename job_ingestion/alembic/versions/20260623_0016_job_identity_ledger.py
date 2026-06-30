"""job identity ledger table

Revision ID: 20260623_0016
Revises: 20260621_0015
Create Date: 2026-06-23 12:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260623_0016"
down_revision: str = "20260621_0015"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "job_identity_ledger",
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("external_job_id", sa.String(length=255), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_changed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("company_id", "external_job_id", name="pk_job_identity_ledger"),
    )
    op.create_index("ix_job_identity_ledger_company_id", "job_identity_ledger", ["company_id"])


def downgrade() -> None:
    op.drop_index("ix_job_identity_ledger_company_id", table_name="job_identity_ledger")
    op.drop_table("job_identity_ledger")
