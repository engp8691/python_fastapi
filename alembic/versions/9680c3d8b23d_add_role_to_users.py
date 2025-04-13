"""Add role to users

Revision ID: add_role_to_users
Revises: add_hashed_password
Create Date: 2025-04-11 15:44:59.826458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_role_to_users'
down_revision: Union[str, None] = 'add_hashed_password'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users',
        sa.Column('role', sa.String(), nullable=False, server_default='')
    )
    op.alter_column('users', 'role', server_default=None)


def downgrade():
    op.drop_column('users', 'role')
