"""remove_icon_from_module

Revision ID: 63ff6c6db880
Revises: beac1ac977bb
Create Date: 2025-02-13 21:37:41.059268

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63ff6c6db880'
down_revision: Union[str, None] = 'beac1ac977bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
