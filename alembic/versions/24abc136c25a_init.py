"""init

Revision ID: 24abc136c25a
Revises: 
Create Date: 2023-06-23 05:29:08.942621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24abc136c25a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('conne',
    sa.Column('connid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mid', sa.Integer(), nullable=False),
    sa.Column('mmid', sa.Integer(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('connid')
    )
    op.create_index(op.f('ix_conne_mid'), 'conne', ['mid'], unique=False)
    op.create_index(op.f('ix_conne_mmid'), 'conne', ['mmid'], unique=False)
    op.create_index(op.f('ix_conne_year'), 'conne', ['year'], unique=False)
    op.create_table('major',
    sa.Column('mid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mname', sa.String(length=64), nullable=False),
    sa.Column('sid', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('mid')
    )
    op.create_index(op.f('ix_major_mname'), 'major', ['mname'], unique=False)
    op.create_index(op.f('ix_major_sid'), 'major', ['sid'], unique=False)
    op.create_table('must',
    sa.Column('mmid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mname', sa.String(length=64), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('sid', sa.Integer(), nullable=False),
    sa.Column('must', sa.Integer(), nullable=False),
    sa.Column('include', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('mmid')
    )
    op.create_index(op.f('ix_must_include'), 'must', ['include'], unique=False)
    op.create_index(op.f('ix_must_mname'), 'must', ['mname'], unique=False)
    op.create_index(op.f('ix_must_must'), 'must', ['must'], unique=False)
    op.create_index(op.f('ix_must_sid'), 'must', ['sid'], unique=False)
    op.create_index(op.f('ix_must_year'), 'must', ['year'], unique=False)
    op.create_table('rank',
    sa.Column('rmid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mid', sa.Integer(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('rank', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.Column('schedule', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('rmid')
    )
    op.create_index(op.f('ix_rank_mid'), 'rank', ['mid'], unique=False)
    op.create_index(op.f('ix_rank_rank'), 'rank', ['rank'], unique=False)
    op.create_index(op.f('ix_rank_score'), 'rank', ['score'], unique=False)
    op.create_index(op.f('ix_rank_year'), 'rank', ['year'], unique=False)
    op.create_table('tag',
    sa.Column('tid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tname', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('tid')
    )
    op.create_index(op.f('ix_tag_tname'), 'tag', ['tname'], unique=False)
    op.create_table('univ',
    sa.Column('sid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uname', sa.String(length=64), nullable=False),
    sa.Column('utags', sa.String(length=64), nullable=False),
    sa.Column('province', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('sid')
    )
    op.create_index(op.f('ix_univ_province'), 'univ', ['province'], unique=False)
    op.create_index(op.f('ix_univ_uname'), 'univ', ['uname'], unique=False)
    op.create_table('user',
    sa.Column('uid', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.Column('passwd', sa.String(length=64), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('must', sa.Integer(), nullable=True),
    sa.Column('mymajor', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_index(op.f('ix_univ_uname'), table_name='univ')
    op.drop_index(op.f('ix_univ_province'), table_name='univ')
    op.drop_table('univ')
    op.drop_index(op.f('ix_tag_tname'), table_name='tag')
    op.drop_table('tag')
    op.drop_index(op.f('ix_rank_year'), table_name='rank')
    op.drop_index(op.f('ix_rank_score'), table_name='rank')
    op.drop_index(op.f('ix_rank_rank'), table_name='rank')
    op.drop_index(op.f('ix_rank_mid'), table_name='rank')
    op.drop_table('rank')
    op.drop_index(op.f('ix_must_year'), table_name='must')
    op.drop_index(op.f('ix_must_sid'), table_name='must')
    op.drop_index(op.f('ix_must_must'), table_name='must')
    op.drop_index(op.f('ix_must_mname'), table_name='must')
    op.drop_index(op.f('ix_must_include'), table_name='must')
    op.drop_table('must')
    op.drop_index(op.f('ix_major_sid'), table_name='major')
    op.drop_index(op.f('ix_major_mname'), table_name='major')
    op.drop_table('major')
    op.drop_index(op.f('ix_conne_year'), table_name='conne')
    op.drop_index(op.f('ix_conne_mmid'), table_name='conne')
    op.drop_index(op.f('ix_conne_mid'), table_name='conne')
    op.drop_table('conne')
    # ### end Alembic commands ###
