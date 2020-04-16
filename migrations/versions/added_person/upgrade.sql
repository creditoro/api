CREATE TABLE people
(
    identifier UUID NOT NULL,
    phone       VARCHAR(256),
    email      email,
    name       VARCHAR(256),
    PRIMARY KEY (identifier)
);
CREATE INDEX people_name_idx ON people USING btree (name);