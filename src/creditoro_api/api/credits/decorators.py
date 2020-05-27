"""
This module is for decorators used in /credits.
"""
import functools
from http import HTTPStatus

from flask import request
from sqlalchemy.exc import DataError

from creditoro_api.models.channel_admins import ChannelAdmin
from creditoro_api.models.credits import Credit
from creditoro_api.models.productions import Production
from creditoro_api.models.users import Role
from creditoro_api.api.decorators import token_required
from flask import g


def id_to_credit(func):
    """id_to_credit.

    Args:
        func:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        credit_id = kwargs.get("credit_id")
        try:
            credit = Credit.query.get(credit_id)
            if not credit:
                return "Credit not found", HTTPStatus.NOT_FOUND  # 404
        except DataError:
            return (
                "Provided credit_id is invalid syntax for uuid",
                HTTPStatus.BAD_REQUEST,
            )
        return func(*args, credit=credit)

    return wrapper


def create_credit(func):
    """create_credit.

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
        person_id = body.get("person_id")
        production_id = body.get("production_id")
        job = body.get("job")
        credit = Credit.query.filter_by(person_id=person_id,
                                        production_id=production_id,
                                        job=job).one_or_none()
        if credit:
            # A credit with that email already exists.
            return "", HTTPStatus.CONFLICT

        credit = Credit(production_id=production_id,
                        person_id=person_id,
                        job=job)
        if credit.store():
            return func(*args, **kwargs, credit=credit)
        return "", HTTPStatus.INTERNAL_SERVER_ERROR

    return wrapper


def update_credit(func):
    """update_credit.

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
        credit = kwargs.get("credit")
        if credit is None:
            return "", HTTPStatus.NOT_FOUND

        body = request.json
        if credit.update(**body):
            return func(*args, **kwargs)
        return "", HTTPStatus.BAD_REQUEST

    return wrapper


def can_alter_credit(func):
    """This function checks if the current user is the owner of the production
    or otherwise has permission to edit it..

    Args:
        func: The function to return upon success.
    """
    @token_required
    @id_to_credit
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper.

        Args:
            args:
            kwargs:
        """
        user = g.current_user
        if user.role.value == Role.system_admin.value:
            # User is a system administrator, grant access.
            return func(*args, **kwargs)
        credit = kwargs.get("credit")
        production = Production.query.get(credit.production_id)
        if production.producer_id == user.identifier:
            # GRANT ACCESS: The requester is the producer of the production
            return func(*args, **kwargs)

        if user.role.value == Role.channel_admin.value:
            admin_for_specific_channel = ChannelAdmin.query.filter_by(
                user_id=user.identifier,
                channel_id=production.channel_id).first()
            if admin_for_specific_channel is not None:
                # GRANT ACCESS: The requester is a channel admin
                return func(*args, **kwargs)

        return "User doesn't have permission", HTTPStatus.UNAUTHORIZED

    return wrapper
