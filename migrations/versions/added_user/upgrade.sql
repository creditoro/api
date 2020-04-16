CREATE EXTENSION citext;
CREATE DOMAIN email AS citext
    CHECK ( value ~
            '^[a-zA-Z0-9.!#$%&''*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$' );
CREATE TYPE role AS ENUM ('royalty_user', 'channel_admin', 'system_admin');
CREATE TABLE users
(
    identifier UUID         NOT NULL,
    name       VARCHAR(512),
    email      email UNIQUE NOT NULL,
    phone      varchar(254),
    password   VARCHAR(256),
    role       role         NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (identifier)
);
CREATE INDEX users_email_idx ON users USING btree (email);
CREATE INDEX users_name_idx ON users USING btree (name);
