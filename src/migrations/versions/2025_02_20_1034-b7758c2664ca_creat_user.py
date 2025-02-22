"""creat user

Revision ID: b7758c2664ca
Revises: c271f9a7f2c2
Create Date: 2025-02-20 10:34:35.291404

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "b7758c2664ca"
down_revision: Union[str, None] = "c271f9a7f2c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "Users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )


def downgrade() -> None:
    op.drop_table("Users")
