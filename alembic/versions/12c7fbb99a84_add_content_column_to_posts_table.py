"""add content column to posts table

Revision ID: 12c7fbb99a84
Revises: 9f82a6ad7d20
Create Date: 2022-07-18 10:57:19.976930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12c7fbb99a84'
down_revision = '9f82a6ad7d20'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
