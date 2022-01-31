"""update page add column new

Revision ID: d362a72bf0a5
Revises: f7a5cd16f44a
Create Date: 2022-01-31 11:43:40.090288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd362a72bf0a5'
down_revision = 'f7a5cd16f44a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('page', sa.Column('new', sa.Integer, default=0))


def downgrade():
    op.drop_column('page', 'new')

