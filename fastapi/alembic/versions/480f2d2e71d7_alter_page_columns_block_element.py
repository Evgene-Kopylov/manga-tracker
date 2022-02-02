"""alter page columns block, element, chapters

Revision ID: 480f2d2e71d7
Revises: 05e4b1867a04
Create Date: 2022-02-02 18:43:26.159643

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '480f2d2e71d7'
down_revision = '05e4b1867a04'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('page', 'block', new_column_name='_block')
    op.alter_column('page', 'element', new_column_name='_element')
    op.alter_column('page', 'chapters', new_column_name='_chapters')


def downgrade():
    op.alter_column('page', '_block', new_column_name='block')
    op.alter_column('page', '_element', new_column_name='element')
    op.alter_column('page', '_chapters', new_column_name='chapters')
