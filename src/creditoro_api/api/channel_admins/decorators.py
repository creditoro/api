import functools
from http import HTTPStatus

from flask import g
from sqlalchemy.exc import DataError

from creditoro_api.api.channels.decorators import id_to_channel
from creditoro_api.api.decorators import token_required
from creditoro_api.api.users import id_to_user
from creditoro_api.models.channel_admins import ChannelAdmin
from creditoro_api.models.channels import Channel
from creditoro_api.models.users import Role, User


def ids_to_channel_admin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user_id = kwargs.get("user_id")
        channel_id = kwargs.get("channel_id")
        try:
            channel_admin = ChannelAdmin.query.filter_by(user_id=user_id,
                                                         channel_id=channel_id)
            if not channel_admin:
                return "ChannelAdmin not found", HTTPStatus.NOT_FOUND  # 404
        except DataError:
            # api.creditoro.nymann.dev/users/k3l;21k3;lk3as
            return ("Provided user_id is invalid syntax for uuid",
                    HTTPStatus.BAD_REQUEST)
        return func(*args, user=channel_admin)

    return wrapper


def create_channel_admin(func):
    @permission
    @id_to_user
    @functools.wraps(func)
    def wrapper(*args, user: User, channel: Channel, **_):
        current_user = g.current_user
        if current_user.role.value < Role.channel_admin.value:
            # The user does not have the necessary permissions.
            return "", HTTPStatus.UNAUTHORIZED
        if user is None or channel is None:
            return "", HTTPStatus.INTERNAL_SERVER_ERROR
        channel_admin = ChannelAdmin(user_id=user.identifier,
                                     channel_id=channel.identifier)
        if channel_admin.store():
            return func(*args, channel_admin=channel_admin)
        return "", HTTPStatus.INTERNAL_SERVER_ERROR

    return wrapper


def permission(func):
    @token_required
    @id_to_channel
    @functools.wraps(func)
    def wrapper(*args, channel: Channel, **kwargs):
        current_user = g.current_user
        if current_user.role.value == Role.system_admin.value:
            return func(*args, channel=channel, **kwargs)
        if current_user.role.value != Role.channel_admin.value:
            return "", HTTPStatus.UNAUTHORIZED
        # Check if the user is channel admin for the specific channel:
        ca = ChannelAdmin.query.filter_by(
            user_id=current_user.identifier,
            channel_id=channel.identifier).first()
        if ca is None:
            return "", HTTPStatus.UNAUTHORIZED
        return func(*args, channel=channel, **kwargs)

    return wrapper
