"""create table page

Revision ID: 5871e794e80e
Revises: 
Create Date: 2022-01-20 11:32:12.980647

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5871e794e80e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'page',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('element', sa.String()),
        sa.Column('block', sa.String()),
        sa.Column('last_check', sa.Date),
    )


def downgrade():
    op.drop_table('page')
