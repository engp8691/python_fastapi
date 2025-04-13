"""Change userid to uuid from intto users

Revision ID: 80e4acc18c54
Revises: add_role_to_users
Create Date: 2025-04-12 22:02:14.209316

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80e4acc18c54'
down_revision: Union[str, None] = 'add_role_to_users'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
