"""empty message

Revision ID: ad97019a8d7b
Revises: 
Create Date: 2020-03-04 19:25:16.541557

"""
from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy.orm import sessionmaker

from migrations.helper import execute

revision = 'ad97019a8d7b'
down_revision = None
branch_labels = None
depends_on = None

Session = sessionmaker()

g_bind = op.get_bind()


def upgrade():
    execute(bind=g_bind, filename="added_user/upgrade.sql")


def downgrade():
    execute(bind=g_bind, filename="added_user/downgrade.sql")
