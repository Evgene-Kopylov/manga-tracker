"""create user page page_user

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
        'user',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('email', sa.String(200), nullable=False, unique=True),
        sa.Column('username', sa.String(200)),
        sa.Column('password', sa.String(200))
    )
    op.create_table(
        'page',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('element', sa.String()),
        sa.Column('block', sa.String()),
    )
    op.create_table(
        'page_user',
        sa.Column('page_id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, primary_key=True)
    )


def downgrade():
    op.drop_table('user')
    op.drop_table('page')
    op.drop_table('page_user')