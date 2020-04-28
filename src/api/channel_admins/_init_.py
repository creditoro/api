from http import HTTPStatus

from flask import request
from flask_restplus import Namespace, Resource

from src.api.auth_resource import AuthResource
from src.api.channel_admins.decorators import create_channel_admin
from src.api.channel_admins.fields import SERIALIZE_FIELDS
from src.api.decorators import token_required
from src.models.channel_admins import ChannelAdmin

CHANNEL_ADMINS = Namespace(name="channel_admins", description="Endpoints for channel admins.")

MODEL = CHANNEL_ADMINS.model(name="channel_admin_model", model=SERIALIZE_FIELDS)

@CHANNEL_ADMINS.route("/<string:channel_identifier")
class ChannelAdminByChannelId(AuthResource):
    @CHANNEL_ADMINS.marshal_with(MODEL)
    @id_to_channel
    def get(self, channel_admin: ChannelAdmin):
        return ChannelAdmin.serialize(), HTTPStatus.OK