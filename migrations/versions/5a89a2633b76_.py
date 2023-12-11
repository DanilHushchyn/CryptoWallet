"""empty message

Revision ID: 5a89a2633b76
Revises: bbab2a1f7076
Create Date: 2023-12-11 17:13:02.058345

"""
from typing import Sequence, Union
import sqlalchemy_utils

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a89a2633b76'
down_revision: Union[str, None] = 'bbab2a1f7076'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blockchains',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('image', sqlalchemy_utils.types.url.URLType(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_blockchains_id'), 'blockchains', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_blockchains_id'), table_name='blockchains')
    op.drop_table('blockchains')
    # ### end Alembic commands ###