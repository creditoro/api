"""added_icon_to_channel

Revision ID: 8b3f6a9974ab
Revises: 0388e86dd103
Create Date: 2020-04-20 22:26:12.229834

"""
from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy.orm import sessionmaker

from migrations.helper import execute

revision = '8b3f6a9974ab'
down_revision = '0388e86dd103'
branch_labels = None
depends_on = None

Session = sessionmaker()
g_bind = op.get_bind()


def upgrade():
    execute(bind=g_bind, filename="added_icon_to_channel/upgrade.sql")


def downgrade():
    execute(bind=g_bind, filename="added_icon_to_channel/downgrade.sql")
