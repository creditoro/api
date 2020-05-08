CREATE TABLE channel_admins
(
    user_uuid UUID REFERENCES users (identifier),
    channel_uuid UUID REFERENCES channels (identifier),
    PRIMARY KEY (user_uuid, channel_uuid)
);
CREATE INDEX channel_admin_user_identifier_idx ON channel_admins USING btree (user_uuid);
CREATE INDEX channel_admin_channel_identifier_idx ON channel_admins USING btree (channel_uuid);
