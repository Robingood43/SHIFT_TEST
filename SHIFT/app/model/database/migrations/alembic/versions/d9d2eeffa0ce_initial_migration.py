"""initial migration

Revision ID: d9d2eeffa0ce
Revises: 
Create Date: 2024-05-14 11:43:10.899535

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd9d2eeffa0ce'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'users',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('username', sa.VARCHAR(length=255), nullable=False),
        sa.Column('hashed_password', sa.VARCHAR(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )
    op.create_table(
        'salary_details',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('salary', sa.FLOAT(), nullable=False),
        sa.Column('next_raise', sa.DATE(), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('salary_details')
    # ### end Alembic commands ###
