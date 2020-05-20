"""productions

Revision ID: 8cd96098c27f
Revises: 4a44d1fb8d44
Create Date: 2020-04-16 14:08:34.356116

"""
from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy.orm import sessionmaker

from migrations.helper import execute

revision = '8cd96098c27f'
down_revision = '4a44d1fb8d44'
branch_labels = None
depends_on = None

Session = sessionmaker()
g_bind = op.get_bind()


def upgrade():
    execute(bind=g_bind, filename="added_production/upgrade.sql")


def downgrade():
    execute(bind=g_bind, filename="added_production/downgrade.sql")
