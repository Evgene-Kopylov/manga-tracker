"""create page._parsing_attempt 

Revision ID: d78fae804169
Revises: 480f2d2e71d7
Create Date: 2022-02-07 01:38:26.516151

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd78fae804169'
down_revision = '480f2d2e71d7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('page', sa.Column('parsing_attempt', sa.String))


def downgrade():
    op.drop_column('page', 'parsing_attempt')
