"""Corrected user data

Revision ID: f54b8f5a067c
Revises: 00de86dbe3c4
Create Date: 2025-02-21 12:14:21.711422

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "f54b8f5a067c"
down_revision: Union[str, None] = "00de86dbe3c4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("Users_username_key", "Users", type_="unique")
    op.drop_column("Users", "username")


def downgrade() -> None:
    op.add_column(
        "Users",
        sa.Column(
            "username", sa.VARCHAR(length=50), autoincrement=False, nullable=False
        ),
    )
    op.create_unique_constraint("Users_username_key", "Users", ["username"])
