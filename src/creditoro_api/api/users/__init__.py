"""
This module is for endpoints with base path at /users/
"""

from datetime import timedelta, datetime
from http import HTTPStatus

import jwt
from flask import current_app, request, g
from flask_restplus import Namespace, Resource
from sqlalchemy import or_

from creditoro_api.api.auth_resource import AuthResource
from creditoro_api.api.users.decorators import (
    id_to_user,
    create_user,
    check_password,
    update_user,
)
from creditoro_api.api.users.fields import (
    SERIALIZE_FIELDS,
    SIGNUP_FIELDS,
    LOGIN_FIELDS,
    PATCH_FIELDS,
)
from creditoro_api.models.users import User

USERS = Namespace(name="users", description="Endpoints for users.")

SERIALIZE_MODEL = USERS.model(name="user_model", model=SERIALIZE_FIELDS)
EXPECT_MODEL = USERS.model(name="users_except_model", model=SIGNUP_FIELDS)
PATCH_MODEL = USERS.model(name="users_patch_model", model=PATCH_FIELDS)
LOGIN_MODEL = USERS.model(name="auth_model", model=LOGIN_FIELDS)


@USERS.route("/")
class ListUsers(Resource):
    """ListUsers.
    """
    @USERS.marshal_list_with(SERIALIZE_MODEL)
    @USERS.param(name="q",
                 description="query property, search for name, email and role."
                 )
    def get(self):
        """get.
        """
        query_prop = request.args.get("q", None)
        if query_prop is None:
            results = User.query.all()
        else:
            q = f"%{query_prop}%"
            query = User.query.filter(
                or_(User.name.ilike(q), User.email.ilike(q)))
            results = query.all()
        return User.serialize_list(results), HTTPStatus.OK

    @USERS.expect(EXPECT_MODEL)
    @USERS.marshal_with(SERIALIZE_MODEL)
    @create_user
    def post(self, user: User):
        """post.

        Args:
            user (User): user
        """
        # send_confirmation_email(user=user)
        return user.serialize(), HTTPStatus.CREATED


@USERS.route("/<string:user_id>")
class UserById(AuthResource):
    """UserById.
    """
    @USERS.marshal_with(SERIALIZE_MODEL)
    @id_to_user
    def get(self, user: User):
        """get.

        Args:
            user (User): user
        """
        return user.serialize(), HTTPStatus.OK

    @USERS.expect(EXPECT_MODEL)
    @USERS.marshal_with(SERIALIZE_MODEL)
    @update_user
    def put(self, user):
        """put.

        Args:
            user:
        """
        return user.serialize(), HTTPStatus.OK

    @USERS.marshal_with(SERIALIZE_MODEL)
    @USERS.expect(PATCH_MODEL)
    @update_user
    def patch(self, user):
        """patch.

        Args:
            user:
        """
        return user.serialize(), HTTPStatus.OK

    @USERS.marshal_with(SERIALIZE_MODEL)
    @id_to_user
    def delete(self, user):
        """delete.

        Args:
            user:
        """
        if user.remove():
            # 2XX - success
            # 4XX - Client error
            # 5XX - Server error
            return "", HTTPStatus.NO_CONTENT  # 204
        return "", HTTPStatus.INTERNAL_SERVER_ERROR  # 500


@USERS.route("/login")
class UserLogin(Resource):
    """UserLogin.
    """
    @USERS.expect(LOGIN_MODEL)
    @USERS.marshal_with(SERIALIZE_MODEL)
    @check_password
    def post(self, user: User):
        """post.

        Args:
            user (User): user
        """
        g.current_user = user
        return user.serialize(), HTTPStatus.OK
