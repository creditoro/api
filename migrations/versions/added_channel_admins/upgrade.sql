CREATE TABLE channel_admins
(
    user_id     UUID REFERENCES users (identifier),
    channel_id  UUID REFERENCES channels (identifier),
    PRIMARY KEY (user_id, channel_id)
);