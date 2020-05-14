import functools
from http import HTTPStatus

from flask import request
from sqlalchemy.exc import DataError

from src.models.channel_admins import ChannelAdmin


def create_channel_admin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        body = request.json
        title = body.get("user_id")
        channel_admin = channel_admin.query.filter_by(user_id=user_id).one_or_none()
        if channel_admin:
            # A user with that email already exists.
            return "", HTTPStatus.CONFLICT

        # Check if partition exists.
        if len(title) == 0:
            return "", HTTPStatus.BAD_REQUEST
        channel_admin = channel_admin(**body)
        if channel_admin.store():
            return func(*args, **kwargs, channel_admin=channel_admin)
        return "", HTTPStatus.INTERNAL_SERVER_ERROR

    return wrapper


def id_to_channel_admin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        channel_admin_id = kwargs.get("channel_admin_id")
        try:
            channel_admin = channel_admin.query.get(channel_admin_id)
            if not channel_admin:
                return "channel_admin not found", HTTPStatus.NOT_FOUND  # 404
        except DataError:
            return "Provided channel_admin_id is invalid syntax for uuid", HTTPStatus.BAD_REQUEST
        return func(*args, channel_admin=channel_admin)

    return wrapper


def update_channel_admins(func):
    @id_to_channel_admin
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        channel_admin = kwargs.get("channel_admin")
        if channel_admin is None:
            # A user with that email already exists.
            return "", HTTPStatus.NOT_FOUND

        body = request.json
        if channel_admin.update(**body):
            return func(*args, **kwargs)
        return "", HTTPStatus.BAD_REQUEST

    return wrapper