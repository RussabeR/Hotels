"""bookings add -> created_at

Revision ID: bff4901b23d2
Revises: efd09ef7eff2
Create Date: 2025-03-02 10:41:03.637605

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bff4901b23d2"
down_revision: Union[str, None] = "efd09ef7eff2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "bookings",
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("bookings", "created_at")
    # ### end Alembic commands ###
