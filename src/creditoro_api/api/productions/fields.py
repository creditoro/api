"""
This module is for defining json body fields for /productions
"""

from flask_restplus import fields

SERIALIZE_FIELDS = {
    "identifier": fields.String(required=False),
    "title": fields.String(required=True),
    "producer": fields.Raw(),
    "channel": fields.Raw(),
    "description": fields.String(required=True),
}

POST_FIELDS = {
    "title": fields.String(required=True),
    "producer_id": fields.String(required=True),
    "channel_id": fields.String(required=True),
    "description": fields.String(required=True),
}

PATCH_FIELDS = {
    "title": fields.String(required=False),
    "producer_id": fields.String(required=False),
    "channel_id": fields.String(required=False),
    "description": fields.String(required=True),
}
