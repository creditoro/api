"""added_credit

Revision ID: 0388e86dd103
Revises: 65c5ab9a7eaf
Create Date: 2020-04-17 00:36:09.678493

"""
from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy.orm import sessionmaker

from migrations.helper import execute

revision = '0388e86dd103'
down_revision = '65c5ab9a7eaf'
branch_labels = None
depends_on = None

Session = sessionmaker()
g_bind = op.get_bind()


def upgrade():
    execute(bind=g_bind, filename="added_credit/upgrade.sql")


def downgrade():
    execute(bind=g_bind, filename="added_credit/downgrade.sql")
