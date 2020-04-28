from flask_restplus import fields

SERIALIZE_FIELDS = {
    "user_uuid": fields.String(required=True),
    "channel_uuid": fields.String(required=True),
}