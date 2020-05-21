"""
This module is for defining fields (json body) for /credits/.
"""

from flask_restplus import fields

SERIALIZE_FIELDS = {
    "identifier": fields.String(),
    "production": fields.Raw(),
    "person": fields.Raw(),
    "job": fields.String(),
}

EXPECT_FIELDS = {
    "production_id": fields.String(required=True),
    "person_id": fields.String(required=True),
    "job": fields.String(required=True),
}

PATCH_FIELDS = {
    "production_id": fields.String(required=False),
    "person_id": fields.String(required=False),
    "job": fields.String(required=False),
}
