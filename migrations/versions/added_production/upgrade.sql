CREATE TABLE productions
(
    identifier  UUID         NOT NULL,
    title       VARCHAR(256) NOT NULL,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    producer_id UUID REFERENCES users (identifier),
    channel_id  UUID REFERENCES channels (identifier)
) PARTITION BY LIST (left(title, 1));
CREATE INDEX production_title_idx ON productions USING btree (title);
CREATE INDEX production_identifier_idx ON productions USING btree (identifier);
