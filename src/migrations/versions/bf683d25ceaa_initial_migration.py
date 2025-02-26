"""initial migration

Revision ID: bf683d25ceaa
Revises: 
Create Date: 2025-02-17 10:30:39.680648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'bf683d25ceaa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('Rooms',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('hotel_id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('cost', sa.Integer(), nullable=False),
                    sa.Column('quantity', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['hotel_id'], ['Hotels.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('Rooms')
