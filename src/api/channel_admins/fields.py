from flask_restplus import fields

SERIALIZE_FIELDS = {
    "identifier": fields.String(required=False),
    "user_id": fields.String(required=False),
    "channel_id": fields.String(required=False)
}

POST_FIELDS = {
    "user_id": fields.String(required=False),
    "channel_id": fields.String(required=False)
}

PATCH_FIELDS = {
    "user_id": fields.String(required=False),
    "channel_id": fields.String(required=False)
}