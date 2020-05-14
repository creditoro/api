"""added channel_admins

Revision ID: e7a3c34e8553
Revises: 3c721bf260ae
Create Date: 2020-05-14 13:46:38.326421

"""
from alembic import op
from sqlalchemy.orm import sessionmaker
from migrations.helper import execute

# revision identifiers, used by Alembic.
revision = 'e7a3c34e8553'
down_revision = '3c721bf260ae'
branch_labels = None
depends_on = None

Session = sessionmaker()
g_bind = op.get_bind()


def upgrade():
    execute(bind=g_bind, filename="added_channel_admin/upgrade.sql")


def downgrade():
    execute(bind=g_bind, filename="added_channel_admin/downgrade.sql")
