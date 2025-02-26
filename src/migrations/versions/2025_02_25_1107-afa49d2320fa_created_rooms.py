"""Created Rooms

Revision ID: afa49d2320fa
Revises: f54b8f5a067c
Create Date: 2025-02-25 11:07:37.060086

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "afa49d2320fa"
down_revision: Union[str, None] = "f54b8f5a067c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("Rooms", "description", existing_type=sa.VARCHAR(), nullable=False)


def downgrade() -> None:
    op.alter_column("Rooms", "description", existing_type=sa.VARCHAR(), nullable=True)
