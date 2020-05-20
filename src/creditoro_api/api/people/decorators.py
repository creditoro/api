import functools
from http import HTTPStatus

from flask import request
from sqlalchemy.exc import DataError
from validate_email import validate_email

from creditoro_api.models.people import Person


def id_to_person(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        person_id = kwargs.get("person_id")
        try:
            person = Person.query.get(person_id)
            if not person:
                return "Person not found", HTTPStatus.NOT_FOUND  # 404
        except DataError:
            return "Provided person_id is invalid syntax for uuid", HTTPStatus.BAD_REQUEST
        return func(*args, person=person)

    return wrapper


def create_person(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        body = request.json
        email = body.get("email")
        if not validate_email(email):
            return "", HTTPStatus.BAD_REQUEST

        person = Person.query.filter_by(email=email).one_or_none()
        if person:
            # A person with that email already exists.
            return "", HTTPStatus.CONFLICT

        person = Person(**body)
        if person.store():
            return func(*args, **kwargs, person=person)
        return "", HTTPStatus.INTERNAL_SERVER_ERROR

    return wrapper


def update_person(func):
    @id_to_person
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        person = kwargs.get("person")
        if person is None:
            # A person with that email already exists.
            return "", HTTPStatus.NOT_FOUND

        body = request.json
        if person.update(**body):
            return func(*args, **kwargs)
        return "", HTTPStatus.BAD_REQUEST

    return wrapper
