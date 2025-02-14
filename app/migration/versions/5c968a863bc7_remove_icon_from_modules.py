"""remove_icon_from_modules

Revision ID: 5c968a863bc7
Revises: 63ff6c6db880
Create Date: 2025-02-13 21:42:29.116820

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c968a863bc7'
down_revision: Union[str, None] = '63ff6c6db880'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
