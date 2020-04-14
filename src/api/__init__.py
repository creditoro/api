"""
This module is used for adding namespaces to the api.
"""
from flask import make_response
from flask_restplus import Api

from src.api.channels import CHANNELS
from src.api.users import USERS

AUTHORIZATIONS = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

API = Api(
    title="Creditoro API",
    version="1.0.0",
    description="API for Creditoro.",
    contact_email="kristian@nymann.dev",
    doc="/",
    default_mediatype="application/json",
    contact_url="https://github.com/creditoro",
    security="Bearer Auth",
    authorizations=AUTHORIZATIONS
)


@API.representation("application/xml")
def xml(data, code, headers=None):
    resp = make_response(data, code)
    resp.headers.extend(headers or {})
    return resp


# api.creditoro.nymann.dev/users/
API.add_namespace(USERS)

# api.creditoro.nymann.dev/channels/
API.add_namespace(CHANNELS)
