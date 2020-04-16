from flask_restplus import fields

SERIALIZE_FIELDS = {
    "identifier": fields.String(required=False),
    "name": fields.String(required=True),
    "phone": fields.String(required=True),
    "email": fields.String(required=True),
}

SIGNUP_FIELDS = {
    "name": fields.String(required=True),
    "email": fields.String(required=True),
    "phone": fields.String(required=False),
    "password": fields.String(required=True),
    "repeated_password": fields.String(required=True),
}

PATCH_FIELDS = {
    "name": fields.String(required=False),
    "email": fields.String(required=False),
    "phone": fields.String(required=False),
    "password": fields.String(required=False),
}

LOGIN_FIELDS = {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
}
