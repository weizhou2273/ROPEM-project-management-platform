"""empty message

Revision ID: 7972ed00f16e
Revises: 3c0bb78e422b
Create Date: 2017-11-06 10:33:25.143219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7972ed00f16e'
down_revision = '3c0bb78e422b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employees', sa.Column('permission_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'employees', 'permissions', ['permission_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'employees', type_='foreignkey')
    op.drop_column('employees', 'permission_id')
    # ### end Alembic commands ###
