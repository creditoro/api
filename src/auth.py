"""

"""
from datetime import datetime, timedelta
from http import HTTPStatus

import jwt
from flask import g, request
from jwt import DecodeError


class Auth(object):
    def __init__(self, app=None, **kwargs):
        self._options = kwargs
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **_):
        @app.after_request
        def after_request(response):
            if "current_user" not in g:
                print("Current user not found")
                return response
            response.headers["token"] = refresh_token(g.current_user)
            return response

        def refresh_token(user) -> str:
            token = jwt.encode(payload={"id": str(user.identifier),
                                        "exp": datetime.utcnow() + timedelta(minutes=30)},
                               key=app.config["SECRET_KEY"],
                               algorithm="HS256")
            return token.decode("UTF-8")

        @app.before_request
        def before_request():
            from src.models.users import User
            token = request.headers.get("Authorization")
            if not token:
                return
            try:
                data = jwt.decode(jwt=token, key=app.config["SECRET_KEY"], algorithms=["HS256"])
                g.current_user = User.query.get(data["id"])
                g.token = token
            except DecodeError:
                return
