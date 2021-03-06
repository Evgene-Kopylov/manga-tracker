"""update page table

Revision ID: bd00e979d32c
Revises: 5871e794e80e
Create Date: 2022-01-26 11:03:11.173575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd00e979d32c'
down_revision = '5871e794e80e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('page', sa.Column('last_update', sa.DateTime, nullable=False,
                                    server_default='2022-01-27 01:41:17.607058'))
    op.drop_column('page', 'last_check')
    op.add_column('page', sa.Column('last_check', sa.DateTime, nullable=False,
                                    server_default='2022-01-27 01:41:17.607058'))
    op.add_column('page', sa.Column('chapters', sa.String(50000), nullable=False, server_default=''))


def downgrade():
    op.drop_column('page', 'last_update')
    op.drop_column('page', 'chapters')
    op.drop_column('page', 'last_check')
    op.add_column('page', sa.Column('last_check', sa.Date))
