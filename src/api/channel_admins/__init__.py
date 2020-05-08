from http import HTTPStatus

from flask import request
from flask_restplus import Namespace, Resource

from src.api.auth_resource import AuthResource
from src.api.channel_admins.decorators import create_channel_admin, id_to_channel_admin
from src.api.channel_admins.fields import SERIALIZE_FIELDS, POST_FIELDS
from src.api.decorators import token_required
from src.models.channel_admins import ChannelAdmin

CHANNEL_ADMINS = Namespace(name="channel_admins", description="Endpoints for channel admins.")

SERIALIZE_MODEL = CHANNEL_ADMINS.model(name="channel_admin_model", model=SERIALIZE_FIELDS)
EXPECT_MODEL = CHANNEL_ADMINS.model(name="channel_admin_post", model=POST_FIELDS)

@CHANNEL_ADMINS.route("/")
class ListChannelAdmins(AuthResource):
    @CHANNEL_ADMINS.marshal_list_with(SERIALIZE_MODEL)
    @CHANNEL_ADMINS.param(name="q", description="query property, search for name, email and role.")
    def get(self):
        query_prop = request.args.get("q", None)
        if query_prop is None:
            results = ChannelAdmin.query.all()
        else:
            q = f"%{query_prop}%"
            query = ChannelAdmin.query.filter(
                or_(
                    ChannelAdmin.name.ilike(q),
                    ChannelAdmin.email.ilike(q)
                )
            )
            results = query.all()
        return ChannelAdmin.serialize_list(results), HTTPStatus.OK

    @CHANNEL_ADMINS.expect(EXPECT_MODEL)
    @CHANNEL_ADMINS.marshal_with(SERIALIZE_MODEL)
    @create_channel_admin
    def post(self, channelAdmin: ChannelAdmin):
        return ChannelAdmin.serialize(), HTTPStatus.CREATED

