"""
Module for endpoints to routes at /productions
"""

from http import HTTPStatus

from flask import request
from flask_restplus import Namespace, Resource
from creditoro_api.api.auth_resource import AuthResource
from creditoro_api.api.productions.decorators import (
    id_to_production,
    create_production,
    update_production,
)
from creditoro_api.api.productions.fields import (
    SERIALIZE_FIELDS,
    POST_FIELDS,
    PATCH_FIELDS,
)
from creditoro_api.api.decorators import token_required
from creditoro_api.models.productions import Production

PRODUCTIONS = Namespace(name="productions",
                        description="Endpoints for productions.")

SERIALIZE_MODEL = PRODUCTIONS.model(name="production_model",
                                    model=SERIALIZE_FIELDS)
EXPECT_MODEL = PRODUCTIONS.model(name="productions_post_model",
                                 model=POST_FIELDS)
PATCH_MODEL = PRODUCTIONS.model(name="productions_patch_model",
                                model=PATCH_FIELDS)


@PRODUCTIONS.route("/")
class ListProductions(Resource):
    """ListProductions.
    """
    @PRODUCTIONS.doc(security=None)
    @PRODUCTIONS.marshal_list_with(SERIALIZE_MODEL)
    @PRODUCTIONS.param(
        name="q",
        description="query property, search for name, email and role.")
    def get(self):
        """get.
        """
        query_prop = request.args.get(key="q", default=None, type=str)
        if query_prop is None:
            results = Production.query.all()
        else:
            results = Production.query.filter(
                Production.title.ilike(f"%{query_prop}%")).all()
        return Production.serialize_list(results), HTTPStatus.OK

    @token_required
    @PRODUCTIONS.expect(EXPECT_MODEL)
    @PRODUCTIONS.marshal_with(SERIALIZE_MODEL)
    @create_production
    def post(self, production: Production):
        """post.

        Args:
            production (Production): production
        """
        return production.serialize(), HTTPStatus.CREATED


@PRODUCTIONS.route("/<string:production_id>")
class ProductionById(AuthResource):
    """ProductionById.
    """
    @PRODUCTIONS.marshal_with(SERIALIZE_MODEL)
    @id_to_production
    def get(self, production: Production):
        """get.

        Args:
            production (Production): production
        """
        return production.serialize(), HTTPStatus.OK

    @PRODUCTIONS.marshal_with(SERIALIZE_MODEL)
    @PRODUCTIONS.expect(PATCH_MODEL)
    @update_production
    def patch(self, production):
        """patch.

        Args:
            production:
        """
        return production.serialize(), HTTPStatus.OK

    @PRODUCTIONS.marshal_with(SERIALIZE_MODEL)
    @PRODUCTIONS.expect(EXPECT_MODEL)
    @update_production
    def put(self, production):
        """put.

        Args:
            production:
        """
        return production.serialize(), HTTPStatus.OK

    @id_to_production
    def delete(self, production):
        """delete.

        Args:
            production:
        """
        if production.remove():
            # 2XX - success
            # 4XX - Client error
            # 5XX - Server error
            return "", HTTPStatus.NO_CONTENT  # 204
        return "", HTTPStatus.INTERNAL_SERVER_ERROR  # 500
