"""merge float and unconfirmed_email branches

Revision ID: 9756c11897d0
Revises: 42e0143b1ae1, a494c707198b
Create Date: 2025-05-10 22:54:05.526345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9756c11897d0'
down_revision = ('42e0143b1ae1', 'a494c707198b')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
