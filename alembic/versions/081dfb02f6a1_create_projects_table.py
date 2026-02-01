"""create projects table

Revision ID: 081dfb02f6a1
Revises:
Create Date: 2026-01-29 23:40:23.929600

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '081dfb02f6a1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('titulo', sa.String(150), nullable=False),
        sa.Column('lider', sa.String(100), nullable=False),
        sa.Column('descripcion', sa.String(500)),
        sa.Column('fecha_inicio', sa.Date, nullable=False),
        sa.Column('estado', sa.Boolean, default=True)
    )


def downgrade() -> None:
    op.drop_table('projects')
