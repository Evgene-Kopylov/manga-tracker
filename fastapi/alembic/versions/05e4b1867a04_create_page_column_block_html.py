"""create page column block_html

Revision ID: 05e4b1867a04
Revises: d362a72bf0a5
Create Date: 2022-02-02 17:52:04.354123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05e4b1867a04'
down_revision = 'd362a72bf0a5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('page', sa.Column('block_html', sa.TEXT))


def downgrade():
    op.drop_column('page', 'block_html')
