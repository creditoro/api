from flask_restplus import fields

SERIALIZE_FIELDS = {
    "identifier": fields.String(required=False),
    "name": fields.String(required=True),
}

SIGNUP_FIELDS = {
    "name": fields.String(required=True),
}

