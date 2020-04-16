from http import HTTPStatus

from flask import request
from flask_restplus import Namespace, Resource

from src.api.auth_resource import AuthResource
from src.api.productions.decorators import id_to_production, create_production
from src.api.productions.fields import SERIALIZE_FIELDS, POST_FIELDS
from src.api.decorators import token_required
from src.models.productions import Production

PRODUCTIONS = Namespace(name="productions", description="Endpoints for productions.")

MODEL = PRODUCTIONS.model(name="production_model", model=SERIALIZE_FIELDS)
EXPECT_MODEL = PRODUCTIONS.model(name="PRODUCTIONS_signup_model", model=POST_FIELDS)


@PRODUCTIONS.route("/")
class ListProductions(Resource):
    @PRODUCTIONS.doc(security=None)
    @PRODUCTIONS.marshal_list_with(MODEL)
    @PRODUCTIONS.param(name="q", description="query property, search for name, email and role.")
    def get(self):
        query_prop = request.args.get(key="q", default=None, type=str)
        if query_prop is None:
            results = Production.query.all()
        else:
            results = Production.query.filter(
                Production.title.ilike(f"%{query_prop}%")
            ).all()
        return Production.serialize_list(results), HTTPStatus.OK

    @token_required
    @PRODUCTIONS.expect(EXPECT_MODEL)
    @PRODUCTIONS.marshal_with(MODEL)
    @create_production
    def post(self, production: Production):
        return production.serialize(), HTTPStatus.CREATED


@PRODUCTIONS.route("/<string:production_id>")
class ProductionById(AuthResource):
    @PRODUCTIONS.marshal_with(MODEL)
    @id_to_production
    def get(self, production: Production):
        return production.serialize(), HTTPStatus.OK

    @PRODUCTIONS.marshal_with(MODEL)
    @PRODUCTIONS.expect(EXPECT_MODEL)
    @id_to_production
    def patch(self, production):
        body = PRODUCTIONS.payload
        name = body.get("name")
        production.name = name
        production.store()
        return production.serialize(), HTTPStatus.OK

    @id_to_production
    def delete(self, production):
        if production.remove():
            # 2XX - success
            # 4XX - Client error
            # 5XX - Server error
            return "", HTTPStatus.NO_CONTENT  # 204
        return "", HTTPStatus.INTERNAL_SERVER_ERROR  # 500
