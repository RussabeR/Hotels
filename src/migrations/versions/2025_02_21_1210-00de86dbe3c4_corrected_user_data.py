"""Corrected user data

Revision ID: 00de86dbe3c4
Revises: 2e7a9d02f1e1
Create Date: 2025-02-21 12:10:39.195685

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "00de86dbe3c4"
down_revision: Union[str, None] = "2e7a9d02f1e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("Users", "name")
    op.drop_column("Users", "age")


def downgrade() -> None:
    op.add_column(
        "Users", sa.Column("age", sa.INTEGER(), autoincrement=False, nullable=False)
    )
    op.add_column(
        "Users",
        sa.Column("name", sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    )
