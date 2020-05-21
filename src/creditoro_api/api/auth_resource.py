"""
This module is used by routes that all require token validation.
"""
from flask_restplus import Resource

from creditoro_api.api.decorators import token_required


class AuthResource(Resource):
    """AuthResource.
    """

    method_decorators = [token_required]
