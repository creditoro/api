import functools
from http import HTTPStatus

import jwt
from flask import request, current_app, g
from sqlalchemy.exc import DataError
from werkzeug.security import check_password_hash

from src.models.users import User


def id_to_user(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user_id = kwargs.get("user_id")
        try:
            user = User.query.get(user_id)
            if not user:
                return "User not found", HTTPStatus.NOT_FOUND
        except DataError:
            return "Provided user_id is invalid syntax for uuid", HTTPStatus.BAD_REQUEST
        return func(*args, user)

    return wrapper


def create_user(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        body = request.json
        email = body.get("email")

        password = body.get("password")
        repeat_password = body.get("repeated_password")
        if password != repeat_password:
            return "", HTTPStatus.BAD_REQUEST

        user = User.query.filter_by(email=email).one_or_none()
        if user:
            # A user with that email already exists.
            return "", HTTPStatus.CONFLICT

        user = User(**body)
        user.store()

        return func(*args, **kwargs, user=user)

    return wrapper


def check_password(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        #auth = request.authorization TODO: needed?
        body = request.json
        if not body:
            return "No email and password provided", HTTPStatus.BAD_REQUEST
        email = body.get("email", None)
        if not email:
            return "Email not  provided", HTTPStatus.BAD_REQUEST
        user = User.query.filter_by(email=email).one_or_none()
        if not user:
            return "User not found", HTTPStatus.NOT_FOUND

        password = body.get("password")
        if not check_password_hash(user.password, password):
            return "Incorrect password", HTTPStatus.BAD_REQUEST
        return func(args, user=user, **kwargs)

    return wrapper


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
