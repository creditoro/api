from http import HTTPStatus

from flask_restplus import Namespace, Resource

from src.api.auth_resource import AuthResource
from src.api.channels.decorators import id_to_channel, create_channel
from src.api.channels.fields import SERIALIZE_FIELDS, SIGNUP_FIELDS
from src.models.channels import Channel

CHANNELS = Namespace(name="CHANNELS", description="Endpoints for CHANNELS.")

MODEL = CHANNELS.model(name="channel_model", model=SERIALIZE_FIELDS)
SIGNUP_MODEL = CHANNELS.model(name="CHANNELS_signup_model", model=SIGNUP_FIELDS)


@CHANNELS.route("/")
class CHANNELS(Resource):
    @CHANNELS.marshal_list_with(MODEL)
    @CHANNELS.param(name="q", description="query property, search for name, email and role.")
    def get(self):
        results = Channel.query.all()
        return Channel.serialize_list(results), HTTPStatus.OK

    @CHANNELS.expect(SIGNUP_MODEL)
    @CHANNELS.marshal_with(MODEL)
    @create_channel
    def post(self, channel: Channel):
        # send_confirmation_email(channel=channel)
        return channel.serialize(), HTTPStatus.CREATED


@CHANNELS.route("/<string:channel_id>")
class ChannelById(AuthResource):
    @CHANNELS.marshal_with(MODEL)
    @id_to_channel
    def get(self, channel: Channel):
        return channel.serialize(), HTTPStatus.OK

    @CHANNELS.marshal_with(MODEL)
    @id_to_channel
    def update(self, channel):
        # TODO(HTTP Update provide all keys.)
        return channel.serialize(), HTTPStatus.OK

    @CHANNELS.marshal_with(MODEL)
    @id_to_channel
    def patch(self, channel):
        # TODO(provide a single key and update its value, let everything else remain as it is.)
        return channel.serialize(), HTTPStatus.OK

    @CHANNELS.marshal_with(MODEL)
    @id_to_channel
    def delete(self, channel):
        if channel.remove():
            # 2XX - success
            # 4XX - Client error
            # 5XX - Server error
            return "", HTTPStatus.NO_CONTENT  # 204
        return "", HTTPStatus.INTERNAL_SERVER_ERROR  # 500
