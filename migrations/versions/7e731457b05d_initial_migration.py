"""Initial migration.

Revision ID: 7e731457b05d
Revises: 40554799f3f5
Create Date: 2022-06-24 20:05:45.039794

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7e731457b05d'
down_revision = '40554799f3f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.Text(), nullable=False))
    op.drop_column('users', 'passworddd')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('passworddd', mysql.TEXT(), nullable=False))
    op.drop_column('users', 'password')
    # ### end Alembic commands ###
