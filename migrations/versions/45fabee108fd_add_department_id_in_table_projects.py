"""Add department_id in TABLE projects

Revision ID: 45fabee108fd
Revises: 0e50c20e6985
Create Date: 2017-10-10 10:46:31.934540

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '45fabee108fd'
down_revision = '0e50c20e6985'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # op.drop_table('Projects')
    op.drop_constraint(u'employees_ibfk_3', 'employees', type_='foreignkey')
    op.drop_column('employees', 'project_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employees', sa.Column('project_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key(u'employees_ibfk_3', 'employees', 'projects', ['project_id'], ['id'])
    op.create_table('Projects',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=60), nullable=True),
    sa.Column('description', mysql.VARCHAR(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    op.drop_table('projects')
    # ### end Alembic commands ###
