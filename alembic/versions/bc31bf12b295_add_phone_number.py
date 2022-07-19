"""add phone number

Revision ID: bc31bf12b295
Revises: 62c48e34bf26
Create Date: 2022-07-18 12:32:14.300655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc31bf12b295'
down_revision = '62c48e34bf26'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade():
    op.drop_column('users', 'phone_number')
