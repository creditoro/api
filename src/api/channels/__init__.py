from http import HTTPStatus

from flask import request
from flask_restplus import Namespace, Resource

from src.api.auth_resource import AuthResource
from src.api.channels.decorators import id_to_channel, create_channel
from src.api.channels.fields import SERIALIZE_FIELDS, POST_FIELDS
from src.api.decorators import token_required
from src.models.channels import Channel

CHANNELS = Namespace(name="channels", description="Endpoints for channels.")

MODEL = CHANNELS.model(name="channel_model", model=SERIALIZE_FIELDS)
EXPECT_MODEL = CHANNELS.model(name="CHANNELS_signup_model", model=POST_FIELDS)


@CHANNELS.route("/")
class ListChannels(Resource):
    @CHANNELS.doc(security=None)
    @CHANNELS.marshal_list_with(MODEL)
    @CHANNELS.param(name="q", description="query property, search for name.")
    def get(self):
        query_prop = request.args.get(key="q", default=None, type=str)
        if query_prop is None:
            results = Channel.query.all()
        else:
            results = Channel.query.filter(
                Channel.name.ilike(f"%{query_prop}%")
            ).all()
        return Channel.serialize_list(results), HTTPStatus.OK

    @token_required
    @CHANNELS.expect(EXPECT_MODEL)
    @CHANNELS.marshal_with(MODEL)
    @create_channel
    def post(self, channel: Channel):
        return channel.serialize(), HTTPStatus.CREATED


@CHANNELS.route("/<string:channel_id>")
class ChannelById(AuthResource):
    @CHANNELS.marshal_with(MODEL)
    @id_to_channel
    def get(self, channel: Channel):
        return channel.serialize(), HTTPStatus.OK

    @CHANNELS.marshal_with(MODEL)
    @CHANNELS.expect(EXPECT_MODEL)
    @id_to_channel
    def patch(self, channel):
        body = CHANNELS.payload
        name = body.get("name")
        channel.name = name
        channel.store()
        return channel.serialize(), HTTPStatus.OK

    @id_to_channel
    def delete(self, channel):
        if channel.remove():
            # 2XX - success
            # 4XX - Client error
            # 5XX - Server error
            return "", HTTPStatus.NO_CONTENT  # 204
        return "", HTTPStatus.INTERNAL_SERVER_ERROR  # 500
