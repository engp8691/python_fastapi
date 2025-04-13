"""Add hashed_password to users

Revision ID: add_hashed_password
Revises: 
Create Date: 2025-04-10 12:04:32.407400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Replace with the real previous revision ID
revision = 'add_hashed_password'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users',
        sa.Column('hashed_password2', sa.String(), nullable=False, server_default='')
    )
    op.alter_column('users', 'hashed_password2', server_default=None)


def downgrade():
    op.drop_column('users', 'hashed_password2')
