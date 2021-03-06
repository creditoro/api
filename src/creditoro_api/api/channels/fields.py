"""
This module is for fields (json body) used by /channels/.
"""
from flask_restplus import fields

SERIALIZE_FIELDS = {
    "identifier": fields.String(required=False),
    "name": fields.String(required=True),
    "icon_url": fields.String(required=True),
}

POST_FIELDS = {
    "name": fields.String(required=True),
    "icon_url": fields.String(required=True),
}
