"""Add weekday to routineday

Revision ID: e8b9c1d2f3a4
Revises: f7a8b9c1d2e3
Create Date: 2026-09-04 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8b9c1d2f3a4'
down_revision: Union[str, Sequence[str], None] = 'f7a8b9c1d2e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'routineday',
        sa.Column('weekday', sa.Integer(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('routineday', 'weekday')
