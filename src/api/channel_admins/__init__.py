from http import HTTPStatus

from flask import request
from flask_restplus import Namespace, Resource

from src.api.auth_resource import AuthResource
from src.api.channel_admins.decorators import id_to_channel_admin, create_channel_admin, update_channel_admins
from src.api.channel_admins.fields import SERIALIZE_FIELDS, POST_FIELDS, PATCH_FIELDS
from src.api.decorators import token_required
from src.models.channel_admins import ChannelAdmin

CHANNEL_ADMINS = Namespace(name="channel_admins", description="Endpoints for channel_admins.")

SERIALIZE_MODEL = CHANNEL_ADMINS.model(name="channel_admins_model", model=SERIALIZE_FIELDS)
EXPECT_MODEL = CHANNEL_ADMINS.model(name="channel_admins_post_model", model=POST_FIELDS)
PATCH_MODEL = CHANNEL_ADMINS.model(name="channel_admins_patch_model", model=PATCH_FIELDS)

@CHANNEL_ADMINS.route("/")
class ListChannelAdmins(Resource):
    @CHANNEL_ADMINS.doc(security=None)
    @CHANNEL_ADMINS.marshal_list_with(SERIALIZE_MODEL)
    @CHANNEL_ADMINS.param(name="q", description="query property, search for name, email and role.")
    def get(self):
        query_prop = request.args.get(key="q", default=None, type=str)
        if query_prop is None:
            results = ChannelAdmin.query.all()
        else:
            results = ChannelAdmin.query.filter(
                ChannelAdmin.title.ilike(f"%{query_prop}%")
            ).all()
        return ChannelAdmin.serialize_list(results), HTTPStatus.OK

    @token_required
    @CHANNEL_ADMINS.expect(EXPECT_MODEL)
    @CHANNEL_ADMINS.marshal_with(SERIALIZE_MODEL)
    @create_channel_admin
    def post(self, channelAdmin: ChannelAdmin):
        return channelAdmin.serialize(), HTTPStatus.CREATED