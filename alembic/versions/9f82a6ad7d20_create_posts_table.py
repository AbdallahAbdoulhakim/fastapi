"""create posts table

Revision ID: 9f82a6ad7d20
Revises: 
Create Date: 2022-07-18 10:43:07.583663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f82a6ad7d20'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id', sa.INTEGER, nullable=False, primary_key=True),
    sa.Column('title', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
