"""debug test

Revision ID: f8f56a7bfeba
Revises: 2db2081c35bb
Create Date: 2017-10-10 12:48:53.052376

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f8f56a7bfeba'
down_revision = '2db2081c35bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'projects_ibfk_1', 'projects', type_='foreignkey')
    op.drop_column('projects', 'department_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('department_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key(u'projects_ibfk_1', 'projects', 'departments', ['department_id'], ['id'])
    # ### end Alembic commands ###
