"""cw_m_category

Revision ID: 502693a4d106
Revises: ca74e5ff74e2
Create Date: 2020-04-22 22:44:16.642976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '502693a4d106'
down_revision = 'ca74e5ff74e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cw_m_category',
    sa.Column('mcid', sa.Integer(), nullable=False),
    sa.Column('mc_level', sa.String(length=3), nullable=True),
    sa.Column('mc_definition', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('mcid'),
    sa.UniqueConstraint('mc_level')
    )
    op.drop_table('sqlite_sequence')
    op.alter_column('cw_user', 'u_phone',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_unique_constraint(None, 'cw_user', ['u_email'])
    op.create_unique_constraint(None, 'cw_user', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cw_user', type_='unique')
    op.drop_constraint(None, 'cw_user', type_='unique')
    op.alter_column('cw_user', 'u_phone',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_table('sqlite_sequence',
    sa.Column('name', sa.NullType(), nullable=True),
    sa.Column('seq', sa.NullType(), nullable=True)
    )
    op.drop_table('cw_m_category')
    # ### end Alembic commands ###
