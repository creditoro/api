"""added descriptions_to_productions

Revision ID: 3c721bf260ae
Revises: 8b3f6a9974ab
Create Date: 2020-05-08 14:47:10.467726

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from migrations.helper import execute

# revision identifiers, used by Alembic.
revision = '3c721bf260ae'
down_revision = '8b3f6a9974ab'
branch_labels = None
depends_on = None

Session = sessionmaker()
g_bind = op.get_bind()


def upgrade():
    execute(bind=g_bind, filename="added_description_to_productions/upgrade.sql")


def downgrade():
    execute(bind=g_bind, filename="added_description_to_productions/downgrade.sql")