CREATE TABLE channel_admins
(
    identifier  UUID         NOT NULL,
    user_id UUID REFERENCES users (identifier),
    channel_id  UUID REFERENCES channels (identifier),
    PRIMARY KEY (identifier)
);
CREATE INDEX channel_admins_identifier_idx ON productions USING btree (identifier);