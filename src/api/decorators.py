import functools
from http import HTTPStatus

import jwt
from flask import request, current_app, g

from src.models.users import User


def token_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("X-API-KEY")
        if not token:
            return "Token is missing", HTTPStatus.UNAUTHORIZED

        try:
            data = jwt.decode(jwt=token, key=current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = User.query.filter_by(email=data["email"]).one_or_none()
        except Exception:
            return "Token is invalid", HTTPStatus.UNAUTHORIZED
        g.current_user = current_user
        return func(*args, **kwargs)

    return wrapper
