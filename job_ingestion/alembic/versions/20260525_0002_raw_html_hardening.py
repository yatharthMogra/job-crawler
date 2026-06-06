"""raw html hardening

Revision ID: 20260525_0002
Revises: 20260525_0001
Create Date: 2026-05-25 18:25:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260525_0002"
down_revision: str | None = "20260525_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE raw_jobs
        SET raw_html = raw_api_response->>'content'
        WHERE raw_html IS NULL
          AND raw_api_response->>'content' IS NOT NULL
        """
    )
    op.execute("UPDATE raw_jobs SET raw_html = '' WHERE raw_html IS NULL")
    op.alter_column(
        "raw_jobs",
        "raw_html",
        existing_type=sa.Text(),
        nullable=False,
        server_default=sa.text("''"),
    )


def downgrade() -> None:
    op.alter_column(
        "raw_jobs",
        "raw_html",
        existing_type=sa.Text(),
        nullable=True,
        server_default=None,
    )
