import functools
from http import HTTPStatus

from flask import request
from sqlalchemy.exc import DataError
from validate_email import validate_email
from werkzeug.security import check_password_hash, generate_password_hash

from src.models.people import Person


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
        person = Person.query.filter_by(email=email).one_or_none()
        if not person:
            return "Person not found", HTTPStatus.NOT_FOUND

        password = body.get("password")
        if not check_password_hash(person.password, password):
            return "Incorrect password", HTTPStatus.BAD_REQUEST
        return func(args, person=person, **kwargs)

    return wrapper
