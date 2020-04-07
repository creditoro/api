from flask_restplus import Resource

from src.api.decorators import token_required


class AuthResource(Resource):
    method_decorators = [token_required]
