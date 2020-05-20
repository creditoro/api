from flask_restplus import Resource

from creditoro_api.api.decorators import token_required


class AuthResource(Resource):
    method_decorators = [token_required]
