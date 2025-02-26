"""Created Rooms(nullable descr)

Revision ID: 2aeb04654049
Revises: afa49d2320fa
Create Date: 2025-02-25 11:16:32.423217

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "2aeb04654049"
down_revision: Union[str, None] = "afa49d2320fa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("Rooms", "description", existing_type=sa.VARCHAR(), nullable=True)


def downgrade() -> None:
    op.alter_column("Rooms", "description", existing_type=sa.VARCHAR(), nullable=False)
