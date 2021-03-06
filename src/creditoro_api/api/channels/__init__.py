"""
This module is for /channels endpoints.
"""

from http import HTTPStatus

from flask import request
from flask_restplus import Namespace, Resource

from creditoro_api.api.channels.decorators import id_to_channel, create_channel
from creditoro_api.api.channels.fields import SERIALIZE_FIELDS, POST_FIELDS
from creditoro_api.api.decorators import is_sys_admin, is_channel_admin
from creditoro_api.models.channels import Channel

CHANNELS = Namespace(name="channels", description="Endpoints for channels.")

MODEL = CHANNELS.model(name="channel_model", model=SERIALIZE_FIELDS)
EXPECT_MODEL = CHANNELS.model(name="CHANNELS_signup_model", model=POST_FIELDS)


@CHANNELS.route("/")
class ListChannels(Resource):
    """ListChannels.
    """

    @CHANNELS.doc(security=None)
    @CHANNELS.marshal_list_with(MODEL)
    @CHANNELS.param(name="q", description="query property, search for name.")
    def get(self):
        """Anyone can get channels.
        """
        query_prop = request.args.get(key="q", default=None, type=str)
        if query_prop is None:
            results = Channel.query.all()
        else:
            results = Channel.query.filter(
                Channel.name.ilike(f"%{query_prop}%")).all()
        return Channel.serialize_list(results), HTTPStatus.OK

    @CHANNELS.expect(EXPECT_MODEL)
    @CHANNELS.marshal_with(MODEL)
    @is_sys_admin
    @create_channel
    def post(self, channel: Channel):
        """Only system administrators can create a channel.

        Args:
            channel (Channel): Channel to serialize.
        """
        return channel.serialize(), HTTPStatus.CREATED


@CHANNELS.route("/<string:channel_id>")
class ChannelById(Resource):
    """ChannelById.
    """

    @CHANNELS.marshal_with(MODEL)
    @id_to_channel
    def get(self, channel: Channel):
        """Anyone can get a specific channel.

        Args:
            channel (Channel): channel
        """
        return channel.serialize(), HTTPStatus.OK

    @CHANNELS.marshal_with(MODEL)
    @CHANNELS.expect(EXPECT_MODEL)
    @is_channel_admin
    @id_to_channel
    def patch(self, channel):
        """patch.

        Args:
            channel:
        """
        body = CHANNELS.payload
        name = body.get("name")
        channel.name = name
        channel.store()
        return channel.serialize(), HTTPStatus.OK

    @id_to_channel
    @is_sys_admin
    def delete(self, channel):
        """delete.

        Args:
            channel:
        """
        if channel.remove():
            # 2XX - success
            # 4XX - Client error
            # 5XX - Server error
            return "", HTTPStatus.NO_CONTENT  # 204
        return "", HTTPStatus.INTERNAL_SERVER_ERROR  # 500
