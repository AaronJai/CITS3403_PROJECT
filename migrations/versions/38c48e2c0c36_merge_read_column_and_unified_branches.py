"""merge read column and unified branches

Revision ID: 38c48e2c0c36
Revises: 718f5ac0d15f, 9756c11897d0
Create Date: 2025-05-10 23:27:09.230167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38c48e2c0c36'
down_revision = ('718f5ac0d15f', '9756c11897d0')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
