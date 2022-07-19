"""add last few columns to posts table

Revision ID: d36a9ebbbdbf
Revises: bd23b9cd3471
Create Date: 2022-07-18 12:13:25.519833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd36a9ebbbdbf'
down_revision = 'bd23b9cd3471'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, server_default=sa.text("TRUE")))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
