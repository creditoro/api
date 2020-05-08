import functools
from http import HTTPStatus

from flask import request
from sqlalchemy.exc import DataError

from src.models.channel_admins import ChannelAdmin

def id_to_channel_admin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        channel_admin_id = kwargs.get("channel_uuid")
        try:
            channel_admin = ChannelAdmin.query.get(channel_admin_id)
            if not channel_admin:
                return "Channel_admin not found", HTTPStatus.NOT_FOUND  # 404
        except DataError:
            return "Provided channel_admin_identifier is invalid syntax for uuid", HTTPStatus.BAD_REQUEST
    return wrapper

def create_channel_admin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        body = request.json
        channel_admin = ChannelAdmin(**body)
        if channel_admin.store():
            return func(*args, **kwargs, channelAdmin=channel_admin)
        return "", HTTPStatus.INTERNAL_SERVER_ERROR

    return wrapper