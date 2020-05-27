from flask_restplus import fields

SERIALIZE_FIELDS = {"user": fields.Raw(), "channel": fields.Raw()}

EXPECT_FIELDS = {
    "user_id": fields.String(required=True),
    "channel_id": fields.String(required=True),
}
