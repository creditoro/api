CREATE TABLE channels
(
    identifier UUID NOT NULL,
    name       VARCHAR(512),
    PRIMARY KEY (identifier)
);
CREATE INDEX channels_name_idx ON channels USING btree (name);