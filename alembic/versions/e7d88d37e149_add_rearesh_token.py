"""add_rearesh_token

Revision ID: e7d88d37e149
Revises: 0f87b725840d
Create Date: 2024-08-20 16:22:16.925739

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7d88d37e149'
down_revision: Union[str, None] = '0f87b725840d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('refresh_token', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'refresh_token')
    # ### end Alembic commands ###
