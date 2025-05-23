"""create_db1

Revision ID: edadd4019c72
Revises: 666122444510
Create Date: 2025-05-20 16:24:34.308841

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'edadd4019c72'
down_revision: Union[str, None] = '666122444510'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'sellers', ['kaspi_email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'sellers', type_='unique')
    # ### end Alembic commands ###
