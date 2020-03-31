"""
This module is used for adding namespaces to the api.
"""
from flask import make_response
from flask_restplus import Api
from src.api.users import USERS

AUTHORIZATIONS = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-KEY"
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
    authorizations=AUTHORIZATIONS
)


@API.representation("application/xml")
def xml(data, code, headers=None):
    resp = make_response(data, code)
    resp.headers.extend(headers or {})
    return resp


# api.creditoro.nymann.dev/users/
API.add_namespace(USERS)
