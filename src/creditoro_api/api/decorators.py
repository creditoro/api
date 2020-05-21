"""
This module is for commonly used decorators across multiple routes.
"""

import functools
from http import HTTPStatus

from flask import g

from creditoro_api.models.channel_admins import ChannelAdmin
from creditoro_api.models.users import Role


def token_required(func):
    """token_required.

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
        if "token" not in g:
            return "Token is missing or invalid", HTTPStatus.UNAUTHORIZED
        return func(*args, **kwargs)

    return wrapper


@token_required
def is_sys_admin(func):
    """is_sys_admin.

    Args:
        func:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = g.current_user
        if user.role != Role.system_admin:
            return "User doesn't have permission", HTTPStatus.UNAUTHORIZED
        return func(*args, **kwargs)

    return wrapper


@token_required
def is_royalty_user(func):
    """is_royalty_user.

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
        user = g.current_user
        if user.role < Role.royalty_user:
            return "User doesn't have permission", HTTPStatus.UNAUTHORIZED
        return func(*args, **kwargs)

    return wrapper


@token_required
def is_channel_admin(func):
    """is_channel_admin.

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
        user = g.current_user
        if user.role < Role.channel_admin:
            return "User doesn't have permission", HTTPStatus.UNAUTHORIZED
        if user.role == Role.system_admin:
            return func(*args, **kwargs)
        if user.role == Role.channel_admin:
            channel = kwargs.get("channel")
            channel_admin = ChannelAdmin.query.filter(
                ChannelAdmin.channel_uuid == channel.identifier,
                ChannelAdmin.user_uuid == user.identifier,
            ).one_or_none()
            if channel_admin is not None:
                return func(*args, **kwargs)
        return "User doesn't have permission", HTTPStatus.UNAUTHORIZED

    return wrapper
