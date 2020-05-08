"""added description to productions

Revision ID: f82f482e4bd4
Revises: 84760d2e4a11
Create Date: 2020-05-08 12:00:32.220633

"""
from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy.orm import sessionmaker
from migrations.helper import execute

# revision identifiers, used by Alembic.
revision = 'f82f482e4bd4'
down_revision = '84760d2e4a11'
branch_labels = None
depends_on = None

Session = sessionmaker()
g_bind = op.get_bind()


def upgrade():
    execute(bind=g_bind, filename="added_description_to_production/upgrade.sql")


def downgrade():
    execute(bind=g_bind, filename="added_description_to_production/downgrade.sql")
