"""job description fields on normalized jobs

Revision ID: 20260527_0005
Revises: 20260527_0004
Create Date: 2026-05-27 15:05:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260527_0005"
down_revision: str = "20260527_0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("normalized_jobs", sa.Column("description_text", sa.Text(), nullable=True))
    op.add_column("normalized_jobs", sa.Column("description_preview", sa.Text(), nullable=True))

    # Best-effort backfill from existing raw HTML for current rows.
    op.execute(
        """
        UPDATE normalized_jobs nj
        SET description_text = NULLIF(
                btrim(
                    regexp_replace(
                        regexp_replace(
                            replace(replace(replace(COALESCE(rj.raw_html, ''), '&amp;', '&'), '&lt;', '<'), '&gt;', '>'),
                            '<[^>]*>',
                            ' ',
                            'g'
                        ),
                        '\\s+',
                        ' ',
                        'g'
                    )
                ),
                ''
            ),
            description_preview = CASE
                WHEN LENGTH(
                    btrim(
                        regexp_replace(
                            regexp_replace(
                                replace(replace(replace(COALESCE(rj.raw_html, ''), '&amp;', '&'), '&lt;', '<'), '&gt;', '>'),
                                '<[^>]*>',
                                ' ',
                                'g'
                            ),
                            '\\s+',
                            ' ',
                            'g'
                        )
                    )
                ) > 400
                THEN SUBSTRING(
                    btrim(
                        regexp_replace(
                            regexp_replace(
                                replace(replace(replace(COALESCE(rj.raw_html, ''), '&amp;', '&'), '&lt;', '<'), '&gt;', '>'),
                                '<[^>]*>',
                                ' ',
                                'g'
                            ),
                            '\\s+',
                            ' ',
                            'g'
                        )
                    )
                    FROM 1 FOR 400
                ) || '...'
                ELSE NULLIF(
                    btrim(
                        regexp_replace(
                            regexp_replace(
                                replace(replace(replace(COALESCE(rj.raw_html, ''), '&amp;', '&'), '&lt;', '<'), '&gt;', '>'),
                                '<[^>]*>',
                                ' ',
                                'g'
                            ),
                            '\\s+',
                            ' ',
                            'g'
                        )
                    ),
                    ''
                )
            END
        FROM raw_jobs rj
        WHERE rj.id = nj.raw_job_id
        """
    )


def downgrade() -> None:
    op.drop_column("normalized_jobs", "description_preview")
    op.drop_column("normalized_jobs", "description_text")
