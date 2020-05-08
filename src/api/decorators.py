import functools
from http import HTTPStatus

from flask import g


def token_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "token" not in g:
            return "Token is missing or invalid", HTTPStatus.UNAUTHORIZED
        return func(*args, **kwargs)

    return wrapper
