import functools
from http import HTTPStatus

from flask import request
from sqlalchemy.exc import DataError

from creditoro_api.models.productions import Production


def create_production(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        body = request.json
        title = body.get("title")
        production = Production.query.filter_by(title=title).one_or_none()
        if production:
            # A user with that email already exists.
            return "", HTTPStatus.CONFLICT

        # Check if partition exists.
        if len(title) == 0:
            return "", HTTPStatus.BAD_REQUEST
        production = Production(**body)
        if production.store():
            return func(*args, **kwargs, production=production)
        return "", HTTPStatus.INTERNAL_SERVER_ERROR

    return wrapper


def id_to_production(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        production_id = kwargs.get("production_id")
        try:
            production = Production.query.get(production_id)
            if not production:
                return "Production not found", HTTPStatus.NOT_FOUND  # 404
        except DataError:
            return "Provided production_id is invalid syntax for uuid", HTTPStatus.BAD_REQUEST
        return func(*args, production=production)

    return wrapper


def update_production(func):
    @id_to_production
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        production = kwargs.get("production")
        if production is None:
            # A user with that email already exists.
            return "", HTTPStatus.NOT_FOUND

        body = request.json
        if production.update(**body):
            return func(*args, **kwargs)
        return "", HTTPStatus.BAD_REQUEST

    return wrapper
