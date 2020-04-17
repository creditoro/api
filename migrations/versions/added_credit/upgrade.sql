CREATE TABLE credits
(
    identifier    UUID         NOT NULL,
    job           VARCHAR(256) NOT NULL,
    production_id UUID REFERENCES productions (identifier),
    person_id     UUID REFERENCES users (identifier),
    PRIMARY KEY (identifier)
);
CREATE INDEX credit_job_idx ON credits USING btree (job);
CREATE INDEX credit_identifier_idx ON credits USING btree (identifier);
