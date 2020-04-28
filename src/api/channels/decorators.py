import functools
from http import HTTPStatus

from flask import request
from sqlalchemy.exc import DataError

from src.models.channels import Channel


def create_channel(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
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
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        channel_id = kwargs.get("channel_id")
        try:
            channel = Channel.query.get(channel_id)
            if not channel:
                return "Channel not found", HTTPStatus.NOT_FOUND  # 404
        except DataError:
            return "Provided channel_id is invalid syntax for uuid", HTTPStatus.BAD_REQUEST
        return func(*args, channel)

    return wrapper
