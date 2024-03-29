"""delete year for conne

Revision ID: 44f1b28accd2
Revises: 9ec55896a46e
Create Date: 2024-01-12 20:59:44.766618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44f1b28accd2'
down_revision = '9ec55896a46e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_conne_year', table_name='conne')
    op.drop_column('conne', 'year')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('conne', sa.Column('year', sa.INTEGER(), nullable=False))
    op.create_index('ix_conne_year', 'conne', ['year'], unique=False)
    # ### end Alembic commands ###
