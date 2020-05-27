CREATE TABLE channel_admins
(
    user_id    UUID REFERENCES users (identifier),
    channel_id UUID REFERENCES channels (identifier),
    PRIMARY KEY (user_id, channel_id)
);
CREATE INDEX channel_admins_user_id_idx ON channel_admins USING btree (user_id);
CREATE INDEX channel_admins_channel_id_idx ON channel_admins USING btree (channel_id);
