"""
This module is used for adding namespaces to the api.
"""
from flask import make_response
from flask_restplus import Api

from creditoro_api.api.channel_admins import CHANNEL_ADMINS
from creditoro_api.api.channels import CHANNELS
from creditoro_api.api.credits import CREDITS
from creditoro_api.api.people import PEOPLE
from creditoro_api.api.productions import PRODUCTIONS
from creditoro_api.api.users import USERS

AUTHORIZATIONS = {
    "Bearer Auth": {"type": "apiKey", "in": "header", "name": "Authorization"}
}

API = Api(
    title="Creditoro API",
    version="1.0.0",
    description="API for Creditoro.",
    contact_email="contact@nymann.dev",
    doc="/",
    default_mediatype="application/json",
    contact_url="https://github.com/creditoro",
    security="Bearer Auth",
    authorizations=AUTHORIZATIONS,
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

# api.creditoro.nymann.dev/productions/
API.add_namespace(PRODUCTIONS)

# api.creditoro.nymann.dev/people/
API.add_namespace(PEOPLE)

# api.creditoro.nymann.dev/credits/
API.add_namespace(CREDITS)

# api.creditoro.nymann.dev/channel_admins/
API.add_namespace(CHANNEL_ADMINS)
