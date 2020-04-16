from flask_restplus import fields

SERIALIZE_FIELDS = {
    "identifier": fields.String(),
    "phone": fields.String(),
    "email": fields.String(),
    "name": fields.String(),
}

EXPECT_FIELDS = {
    "phone": fields.String(required=True),
    "email": fields.String(required=True),
    "name": fields.String(required=True),
}

PATCH_FIELDS = {
    "phone": fields.String(required=False),
    "email": fields.String(required=False),
    "name": fields.String(required=False),
}
