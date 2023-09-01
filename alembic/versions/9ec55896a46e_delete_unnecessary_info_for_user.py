"""delete unnecessary info for user

Revision ID: 9ec55896a46e
Revises: 5be96ace3b5c
Create Date: 2023-06-28 00:27:17.513927

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9ec55896a46e'
down_revision = '5be96ace3b5c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'must')
    op.drop_column('user', 'mymajor')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('mymajor', mysql.TEXT(), nullable=True))
    op.add_column('user', sa.Column('must', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    # ### end Alembic commands ###