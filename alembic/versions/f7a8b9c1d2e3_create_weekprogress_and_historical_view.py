"""Create weekprogress table and userstadistichistorical view

Revision ID: f7a8b9c1d2e3
Revises: acbb413308a4
Create Date: 2026-08-06 16:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7a8b9c1d2e3'
down_revision: Union[str, Sequence[str], None] = 'acbb413308a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create weekprogress table
    op.create_table(
        'weekprogress',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('week_start_date', sa.Date(), nullable=False),
        sa.Column('total_workouts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_volume', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('muscle_distribution', sa.String(), nullable=False, server_default='{}'),
        sa.Column('active_streak', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )

    # 2. Create userstadistichistorical View
    op.execute("""
        CREATE OR REPLACE VIEW userstadistichistorical AS
        SELECT 
            s.user_id,
            DATE_TRUNC('week', s.session_date)::date AS week_start_date,
            COUNT(DISTINCT s.id) AS workouts_completed,
            COALESCE(SUM(w.reps * w.weight), 0.0) AS total_volume,
            COUNT(w.id) AS total_sets
        FROM session s
        LEFT JOIN workoutset w ON s.id = w.session_id
        GROUP BY s.user_id, DATE_TRUNC('week', s.session_date);
    """)


def downgrade() -> None:
    # 1. Drop userstadistichistorical View
    op.execute("DROP VIEW IF EXISTS userstadistichistorical;")

    # 2. Drop weekprogress table
    op.drop_table('weekprogress')
