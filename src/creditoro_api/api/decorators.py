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
        # try:
        if g.token is None:
            return "Token is missing or invalid", HTTPStatus.UNAUTHORIZED
        return func(*args, **kwargs)

    return wrapper


def is_sys_admin(func):
    """is_sys_admin.

    Args:
        func:
    """
    @token_required
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = g.current_user
        if user.role != Role.system_admin:
            return "User doesn't have permission", HTTPStatus.UNAUTHORIZED
        return func(*args, **kwargs)

    return wrapper


def is_royalty_user(func):
    """is_royalty_user.

    Args:
        func:
    """
    @token_required
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


def is_channel_admin(func):
    """is_channel_admin.

    Args:
        func:
    """
    @token_required
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper.

        Args:
            args:
            kwargs:
        """
        user = g.current_user
        if user.role.value < Role.channel_admin.value:
            return "User doesn't have permission", HTTPStatus.UNAUTHORIZED
        if user.role.value == Role.system_admin.value:
            return func(*args, **kwargs)
        if user.role.value == Role.channel_admin.value:
            channel = kwargs.get("channel")
            channel_admin = ChannelAdmin.query.filter(
                ChannelAdmin.channel_id == channel.identifier,
                ChannelAdmin.user_id == user.identifier,
            ).one_or_none()
            if channel_admin is not None:
                return func(*args, **kwargs)
        return "User doesn't have permission", HTTPStatus.UNAUTHORIZED

    return wrapper
