import functools
from http import HTTPStatus

from flask import request
from sqlalchemy.exc import DataError
from werkzeug.security import check_password_hash

from creditoro_api.models.credits import Credit


def id_to_credit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        credit_id = kwargs.get("credit_id")
        try:
            credit = Credit.query.get(credit_id)
            if not credit:
                return "Credit not found", HTTPStatus.NOT_FOUND  # 404
        except DataError:
            return "Provided credit_id is invalid syntax for uuid", HTTPStatus.BAD_REQUEST
        return func(*args, credit=credit)

    return wrapper


def create_credit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        body = request.json
        person_id = body.get("person_id")
        production_id = body.get("production_id")
        job = body.get("job")
        credit = Credit.query.filter_by(person_id=person_id, production_id=production_id, job=job).one_or_none()
        if credit:
            # A credit with that email already exists.
            return "", HTTPStatus.CONFLICT

        credit = Credit(production_id=production_id, person_id=person_id, job=job)
        if credit.store():
            return func(*args, **kwargs, credit=credit)
        return "", HTTPStatus.INTERNAL_SERVER_ERROR

    return wrapper


def update_credit(func):
    @id_to_credit
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        credit = kwargs.get("credit")
        if credit is None:
            return "", HTTPStatus.NOT_FOUND

        body = request.json
        if credit.update(**body):
            return func(*args, **kwargs)
        return "", HTTPStatus.BAD_REQUEST

    return wrapper
