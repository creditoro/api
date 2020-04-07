"""added channel

Revision ID: 4a44d1fb8d44
Revises: ad97019a8d7b
Create Date: 2020-04-07 14:59:49.195181

"""

from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy.orm import sessionmaker

from migrations.helper import execute

revision = '4a44d1fb8d44'
down_revision = 'ad97019a8d7b'
branch_labels = None
depends_on = None

Session = sessionmaker()
g_bind = op.get_bind()


def upgrade():
    execute(bind=g_bind, filename="added_channel/upgrade.sql")


def downgrade():
    execute(bind=g_bind, filename="added_channel/downgrade.sql")
