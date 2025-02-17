"""add rooms

Revision ID: c271f9a7f2c2
Revises: bf683d25ceaa
Create Date: 2025-02-17 10:40:37.943939

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "c271f9a7f2c2"
down_revision: Union[str, None] = "bf683d25ceaa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
