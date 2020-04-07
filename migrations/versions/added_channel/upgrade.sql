CREATE EXTENSION citext;
CREATE DOMAIN email AS citext
    CHECK ( value ~
            '^[a-zA-Z0-9.!#$%&''*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$' );
CREATE TYPE role AS ENUM ('royalty_user', 'channel_admin', 'system_admin');
CREATE TABLE users
(
    identifier UUID                     NOT NULL,
    name       VARCHAR(512),
    email      email UNIQUE             NOT NULL,
    phone      varchar(254),
    created_at timestamp WITH TIME ZONE NOT NULL DEFAULT NOW(),
    password   VARCHAR(256),
    role       role                     NOT NULL,
    PRIMARY KEY (identifier)
);
CREATE INDEX email_idx ON users USING btree (email);
CREATE INDEX name_idx ON users USING btree (name);
