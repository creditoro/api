from flask_restplus import fields

SERIALIZE_FIELDS = {
    "identifier": fields.String(required=False),
    "title": fields.String(required=True),
    "producer": fields.Raw(),
    "channel": fields.Raw()
}

POST_FIELDS = {
    "title": fields.String(required=True),
    "producer_id": fields.String(required=True),
    "channel_id": fields.String(required=True)
}

PATCH_FIELDS = {
    "title": fields.String(required=False),
    "producer_id": fields.String(required=False),
    "channel_id": fields.String(required=False)
}
