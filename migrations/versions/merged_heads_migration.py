"""merge heads

Revision ID: merged_heads
Revises: 57a314a67c73, 9a9a9a9a9a9a
Create Date: 2025-08-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'merged_heads'
down_revision = ('57a314a67c73', '9a9a9a9a9a9a')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass