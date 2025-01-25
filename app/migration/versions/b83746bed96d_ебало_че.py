"""ебало че

Revision ID: b83746bed96d
Revises: 
Create Date: 2025-01-19 11:11:23.663771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b83746bed96d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        op.create_table(
        'courses',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('sphere_id', sa.Integer, sa.ForeignKey('spheres.id')),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now())
    )
        
        op.create_table(
        'topics',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('icon', sa.String),
        sa.Column('text', sa.Text),
        sa.Column('course_id', sa.Integer, sa.ForeignKey('courses.id')),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now())
    )
        op.create_table(
        'cards',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('front_card', sa.Text, nullable=False),
        sa.Column('back_card', sa.Text, nullable=False),
        sa.Column('info', sa.JSON),
        sa.Column('topic_id', sa.Integer, sa.ForeignKey('topics.id')),
    )

def downgrade() -> None:

    op.drop_table('topics')
    # Удаление таблицы courses
    op.drop_table('courses')
