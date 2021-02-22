"""empty message

Revision ID: 437e4d8bfacc
Revises: 
Create Date: 2021-02-21 17:45:51.263704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '437e4d8bfacc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('departments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('employees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('second_name', sa.String(length=64), nullable=False),
    sa.Column('bday', sa.Date(), nullable=False),
    sa.Column('salary', sa.Float(), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('employees')
    op.drop_table('departments')
