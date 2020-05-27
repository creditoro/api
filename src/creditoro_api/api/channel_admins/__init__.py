"""
This module is for endpoints with base path at /users/
"""

from http import HTTPStatus

from flask_restplus import Namespace, Resource

from creditoro_api.api.auth_resource import AuthResource
from creditoro_api.api.channel_admins.decorators import (create_channel_admin,
                                                         permission)
from creditoro_api.api.channel_admins.fields import (SERIALIZE_FIELDS,
                                                     EXPECT_FIELDS)
from creditoro_api.models.channel_admins import ChannelAdmin

CHANNEL_ADMINS = Namespace(
    name="channel_admins",
    description="API endpoint for managing channel admins")

SERIALIZE_MODEL = CHANNEL_ADMINS.model(name="channel_admins_model",
                                       model=SERIALIZE_FIELDS)
EXPECT_MODEL = CHANNEL_ADMINS.model(name="channel_admins_expect_model",
                                    model=EXPECT_FIELDS)


@CHANNEL_ADMINS.route("/")
class ListChannelAdmins(Resource):
    """Lists all channel admins for all channels.
    """

    @CHANNEL_ADMINS.marshal_list_with(SERIALIZE_MODEL)
    def get(self):
        """Lists all channel admins for all channels that the requester is
        channel admin for.
        """
        channel_admins = ChannelAdmin.query.all()
        return ChannelAdmin.serialize_list(channel_admins), HTTPStatus.OK

    @CHANNEL_ADMINS.expect(EXPECT_MODEL)
    @CHANNEL_ADMINS.marshal_with(SERIALIZE_MODEL)
    @create_channel_admin
    def post(self, channel_admin: ChannelAdmin):
        """post.

        Args:
            channel_admin (ChannelAdmin): channel admin
        """
        # send_confirmation_email(user=user)
        return channel_admin.serialize(), HTTPStatus.CREATED


@CHANNEL_ADMINS.route("/<string:user_id>")
class ChannelsByUserId(AuthResource):
    """Channels that the user (given by user_id) is admin for.
    """

    @CHANNEL_ADMINS.marshal_list_with(SERIALIZE_MODEL)
    def get(self, user_id: str):
        """get a list of channels that the user is admin for.

        Args:
            user_id (str): user_id
        """
        channels = ChannelAdmin.query.filter_by(user_id=user_id).all()
        return ChannelAdmin.serialize_list(channels), HTTPStatus.OK


@CHANNEL_ADMINS.route("/<string:user_id>/<string:channel_id>")
class ChannelByUserIdAndChannelId(AuthResource):
    @CHANNEL_ADMINS.marshal_with(SERIALIZE_MODEL)
    def get(self, user_id: str, channel_id: str):
        channel_admin = ChannelAdmin.query.filter_by(
            user_id=user_id, channel_id=channel_id).first()
        if channel_admin is None:
            return "", HTTPStatus.NOT_FOUND
        return channel_admin.serialize(), HTTPStatus.OK

    @permission
    def delete(self, user_id: str, channel_id: str):
        channel_admin = ChannelAdmin.query.filter_by(
            user_id=user_id, channel_id=channel_id).first()
        if channel_admin.remove():
            return "", HTTPStatus.NO_CONTENT
        return HTTPStatus.INTERNAL_SERVER_ERROR
