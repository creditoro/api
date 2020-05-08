"""added Channel_admin

Revision ID: 84760d2e4a11
Revises: 8b3f6a9974ab
Create Date: 2020-05-08 09:45:11.201395

"""
from alembic import op
from sqlalchemy.orm import sessionmaker
from migrations.helper import execute

# revision identifiers, used by Alembic.
revision = '84760d2e4a11'
down_revision = '8b3f6a9974ab'
branch_labels = None
depends_on = None


Session = sessionmaker()
g_bind = op.get_bind()


def upgrade():
    execute(bind=g_bind, filename="added_channel_admin/upgrade.sql")


def downgrade():
    execute(bind=g_bind, filename="added_channel_admin/downgrade.sql")
