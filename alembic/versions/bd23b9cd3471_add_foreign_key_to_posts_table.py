"""add foreign key to posts table

Revision ID: bd23b9cd3471
Revises: 1ced5bef7cd2
Create Date: 2022-07-18 11:40:42.235196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd23b9cd3471'
down_revision = '1ced5bef7cd2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("posts_users_fkey",source_table="posts", referent_table="users",local_cols=["owner_id"], remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("posts_users_fkey",table_name="posts")
    op.drop_column("posts","owner_id")
    pass
