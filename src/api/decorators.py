import functools
from http import HTTPStatus

from flask import g

from src.models.channel_admins import ChannelAdmin
from src.models.users import Role


def token_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "token" not in g:
            return "Token is missing or invalid", HTTPStatus.UNAUTHORIZED
        return func(*args, **kwargs)

    return wrapper


@token_required
def is_sys_admin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = g.current_user
        if user.role != Role.system_admin:
            return "User doesn't have permission", HTTPStatus.UNAUTHORIZED
        return func(*args, **kwargs)

    return wrapper


@token_required
def is_royalty_user(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = g.current_user
        if user.role < Role.royalty_user:
            return "User doesn't have permission", HTTPStatus.UNAUTHORIZED
        return func(*args, **kwargs)

    return wrapper


@token_required
def is_channel_admin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = g.current_user
        if user.role < Role.channel_admin:
            return "User doesn't have permission", HTTPStatus.UNAUTHORIZED
        if user.role == Role.system_admin:
            return func(*args, **kwargs)
        if user.role == Role.channel_admin:
            channel = kwargs.get("channel")
            ca = ChannelAdmin.query.filter(ChannelAdmin.channel_uuid ==
                                           channel.identifier,
                                           ChannelAdmin.user_uuid == user.identifier).one_or_none()
            if ca is not None:
                return func(*args, **kwargs)
        return "User doesn't have permission", HTTPStatus.UNAUTHORIZED

    return wrapper
