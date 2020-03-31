from flask_restplus import Resource

from src.api.users.decorators import token_required


class AuthResource(Resource):
    method_decorators = [token_required]