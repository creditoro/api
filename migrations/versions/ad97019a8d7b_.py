"""empty message

Revision ID: ad97019a8d7b
Revises: 
Create Date: 2020-03-04 19:25:16.541557

"""
from alembic import op

# revision identifiers, used by Alembic.
from sqlalchemy.orm import sessionmaker

revision = 'ad97019a8d7b'
down_revision = None
branch_labels = None
depends_on = None

Session = sessionmaker()


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    session.execute("""
        CREATE EXTENSION citext;
        CREATE DOMAIN email AS citext
            CHECK ( value ~ '^[a-zA-Z0-9.!#$%&''*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$' );
        CREATE TABLE users (
            identifier UUID NOT NULL,
            name VARCHAR(512),
            email email UNIQUE NOT NULL,
            phone varchar(254),
            created_at timestamp WITH TIME ZONE NOT NULL DEFAULT NOW(),
            password VARCHAR(256),
            PRIMARY KEY (identifier)
        );
        CREATE INDEX email_idx ON users USING btree (email);
        """)
    session.commit()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    session.execute("""
        DROP INDEX email_idx;
        DROP TABLE users CASCADE;
        DROP DOMAIN IF EXISTS email;
        DROP EXTENSION IF EXISTS citext RESTRICT;
    """)
    session.commit()
