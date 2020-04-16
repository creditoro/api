"""added_person

Revision ID: 65c5ab9a7eaf
Revises: 8cd96098c27f
Create Date: 2020-04-16 22:05:12.880331

"""
from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy.orm import sessionmaker

from migrations.helper import execute

revision = '65c5ab9a7eaf'
down_revision = '8cd96098c27f'
branch_labels = None
depends_on = None

Session = sessionmaker()
g_bind = op.get_bind()


def upgrade():
    execute(bind=g_bind, filename="added_person/upgrade.sql")


def downgrade():
    execute(bind=g_bind, filename="added_person/downgrade.sql")
