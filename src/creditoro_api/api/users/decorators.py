"""
This module is for decorators used by /users
"""

import functools
from http import HTTPStatus

import sentry_sdk
from flask import request, g
from sqlalchemy.exc import DataError
from validate_email import validate_email
from werkzeug.security import check_password_hash

from creditoro_api.models.users import User, Role


def id_to_user(func):
    """id_to_user.

    Args:
        func:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper.

        Args:
            args:
            kwargs:
        """
        user_id = kwargs.get("user_id")
        try:
            user = User.query.get(user_id)
            if not user:
                return "User not found", HTTPStatus.NOT_FOUND  # 404
        except DataError:
            # api.creditoro.nymann.dev/users/k3l;21k3;lk3as
            return ("Provided user_id is invalid syntax for uuid",
                    HTTPStatus.BAD_REQUEST)
        return func(*args, user=user)

    return wrapper


def create_user(func):
    """create_user.

    Args:
        func:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper.

        Args:
            args:
            kwargs:
        """
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
        if can_alter_user and user.store():
            return func(*args, **kwargs, user=user)
        return "", HTTPStatus.INTERNAL_SERVER_ERROR

    return wrapper


def can_alter_user(role: Role) -> bool:
    """Checks if the current user's role is "higher" or the same as the role
    of the user that's to be created.

    Args:
        role (Role): The role of the user to be created

    Returns:
        bool: True if the current user has permission to create the new user.
        Otherwise false.
    """

    current_user = g.current_user
    return current_user.role.value >= role.value


def update_user(func):
    """update_user.

    Args:
        func:
    """
    @id_to_user
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper.

        Args:
            args:
            kwargs:
        """
        user = kwargs.get("user")
        if user is None:
            # A user with that email already exists.
            return "", HTTPStatus.NOT_FOUND

        body = request.json
        if can_alter_user(user.role) and user.update(**body):
            return func(*args, **kwargs)
        return "", HTTPStatus.BAD_REQUEST

    return wrapper


def check_password(func):
    """check_password.

    Args:
        func:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper.

        Args:
            args:
            kwargs:
        """
        # auth = request.authorization TODO: needed?
        body = request.json
        if not body:
            sentry_sdk.capture_message(f"body was, {body}.")
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
