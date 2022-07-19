"""Add user table

Revision ID: 1ced5bef7cd2
Revises: 12c7fbb99a84
Create Date: 2022-07-18 11:04:35.070688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ced5bef7cd2'
down_revision = '12c7fbb99a84'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer, nullable=False, primary_key=True),
    sa.Column('email', sa.String, nullable=False, unique=True),
    sa.Column('password', sa.String, nullable=False),
    sa.Column('disabled', sa.Boolean, nullable=False, server_default=sa.text("FALSE")),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()"))
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
