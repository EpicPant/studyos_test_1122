"""я заебался

Revision ID: ec812b3220a2
Revises: 5e558192d721
Create Date: 2025-01-19 20:17:08.995745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec812b3220a2'
down_revision: Union[str, None] = '5e558192d721'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('topics', 'icon')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('topics', sa.Column('icon', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
