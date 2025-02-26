"""add user

Revision ID: 2e7a9d02f1e1
Revises: b7758c2664ca
Create Date: 2025-02-20 10:42:39.484073

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "2e7a9d02f1e1"
down_revision: Union[str, None] = "b7758c2664ca"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("Users", sa.Column("name", sa.String(length=20), nullable=False))
    op.add_column("Users", sa.Column("age", sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_column("Users", "age")
    op.drop_column("Users", "name")
