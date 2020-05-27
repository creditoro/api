from flask_restplus import fields

from creditoro_api.models.users import Role

SERIALIZE_FIELDS = {
    "identifier": fields.String(required=False),
    "name": fields.String(required=True),
    "phone": fields.String(required=True),
    "email": fields.String(required=True),
    "role": fields.Integer(required=True)
}

SIGNUP_FIELDS = {
    "name": fields.String(required=True),
    "email": fields.String(required=True),
    "phone": fields.String(required=False),
    "password": fields.String(required=True),
    "repeated_password": fields.String(required=True),
    "role": fields.Integer(default=Role.royalty_user.value)
}

PATCH_FIELDS = {
    "name": fields.String(required=False),
    "email": fields.String(required=False),
    "phone": fields.String(required=False),
    "password": fields.String(required=False),
    "role": fields.Integer(required=False)
}

LOGIN_FIELDS = {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
}
