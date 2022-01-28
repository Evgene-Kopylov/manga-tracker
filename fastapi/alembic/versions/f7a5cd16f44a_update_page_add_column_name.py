"""update page add column name

Revision ID: f7a5cd16f44a
Revises: bd00e979d32c
Create Date: 2022-01-28 22:20:26.370481

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f7a5cd16f44a'
down_revision = 'bd00e979d32c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('page', sa.Column('name', sa.String(200), nullable=False,
                                    server_default='no name'))


def downgrade():
    op.drop_column('page', 'name')
