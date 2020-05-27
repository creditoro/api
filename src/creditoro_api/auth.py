"""
This module is for manging user token.
"""
from datetime import datetime, timedelta

import jwt
import sentry_sdk
from flask import g, request
from jwt import DecodeError


class Auth:
    """Auth.
    """
    def __init__(self, app=None, **kwargs):
        """__init__.

        Args:
            app:
            kwargs:
        """
        self._options = kwargs
        self.token = None
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **_):
        """init_app.

        Args:
            app:
            _:
        """
        @app.after_request
        def after_request(response):
            if "current_user" not in g:
                return response
            response.headers["token"] = refresh_token(g.current_user)
            return response

        def refresh_token(user) -> str:
            token = jwt.encode(
                payload={
                    "id": str(user.identifier),
                    "exp": datetime.utcnow() + timedelta(minutes=30),
                },
                key=app.config["SECRET_KEY"],
                algorithm="HS256",
            )
            return token.decode("UTF-8")

        @app.before_request
        def before_request():
            """before_request.
            """
            from creditoro_api.models.users import User

            token = request.headers.get("Authorization")
            if not token:
                return
            try:
                data = jwt.decode(jwt=token,
                                  key=app.config["SECRET_KEY"],
                                  algorithms=["HS256"])
                g.token = token
                g.current_user = User.query.get(data["id"])

            except DecodeError as e:
                sentry_sdk.capture_exception(e)
                return

    def trick(self, token):
        self.token = token
