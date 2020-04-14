import functools
from http import HTTPStatus

from flask import request
from sqlalchemy.exc import DataError
from validate_email import validate_email
from werkzeug.security import check_password_hash

from src.models.users import User


def id_to_user(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user_id = kwargs.get("user_id")
        try:
            user = User.query.get(user_id)
            if not user:
                return "User not found", HTTPStatus.NOT_FOUND # 404
        except DataError:
            # api.creditoro.nymann.dev/users/k3l;21k3;lk3as
            return "Provided user_id is invalid syntax for uuid", HTTPStatus.BAD_REQUEST
        return func(*args, user)

    return wrapper


def create_user(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        body = request.json
        email = body.get("email")
        if not validate_email(email):
            return "", HTTPStatus.BAD_REQUEST
        password = body.get("password")
        repeat_password = body.get("repeated_password")
        if password != repeat_password:
            return "", HTTPStatus.BAD_REQUEST

        user = User.query.filter_by(email=email).one_or_none()
        if user:
            # A user with that email already exists.
            return "", HTTPStatus.CONFLICT

        user = User(**body)
        if user.store():
            return func(*args, **kwargs, user=user)
        return "", HTTPStatus.INTERNAL_SERVER_ERROR

    return wrapper


def check_password(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # auth = request.authorization TODO: needed?
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


