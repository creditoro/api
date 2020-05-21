"""
This module is for decorators used by /channels
"""

import functools
from http import HTTPStatus

from flask import request
from sqlalchemy.exc import DataError

from creditoro_api.models.channels import Channel


def create_channel(func):
    """create_channel.

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
        name = body.get("name")
        if name is None:
            return "", HTTPStatus.BAD_REQUEST
        channel = Channel.query.filter_by(name=name).one_or_none()
        if channel:
            # A user with that email already exists.
            return "", HTTPStatus.CONFLICT
        channel = Channel(**body)
        if channel.store():
            return func(*args, **kwargs, channel=channel)
        return "", HTTPStatus.INTERNAL_SERVER_ERROR

    return wrapper


def id_to_channel(func):
    """id_to_channel.

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
        channel_id = kwargs.get("channel_id")
        try:
            channel = Channel.query.get(channel_id)
            if not channel:
                return "User not found", HTTPStatus.NOT_FOUND  # 404
        except DataError:
            return "Provided user_id is invalid syntax for uuid", HTTPStatus.BAD_REQUEST
        return func(*args, channel)

    return wrapper
