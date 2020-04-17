from http import HTTPStatus

from flask import request
from flask_restplus import Namespace, Resource

from src.api.auth_resource import AuthResource
from src.api.credits.decorators import id_to_credit, create_credit, update_credit
from src.api.credits.fields import SERIALIZE_FIELDS, EXPECT_FIELDS, PATCH_FIELDS
from src.models.credits import Credit

CREDITS = Namespace(name="credits", description="Endpoints for credits.")

SERIALIZE_MODEL = CREDITS.model(name="credit_model", model=SERIALIZE_FIELDS)
EXPECT_MODEL = CREDITS.model(name="credits_except_model", model=EXPECT_FIELDS)
PATCH_MODEL = CREDITS.model(name="credits_patch_model", model=PATCH_FIELDS)


@CREDITS.route("/")
class ListCredits(Resource):
    @CREDITS.marshal_list_with(SERIALIZE_MODEL)
    @CREDITS.param(name="name", description="search for credits with this job.")
    @CREDITS.param(name="person_id", description="search for credits by this person_id.")
    @CREDITS.param(name="production_id", description="search for credited people for this production_id.")
    def get(self):
        job = request.args.get("job", None)
        person_id = request.args.get("person_id", None)
        production_id = request.args.get("production_id")
        if job is None and person_id is None and production_id is None:
            # user provided no parameters, query it all.
            results = Credit.query.all()
        elif job is None and person_id is None:
            # user only provided production_id
            results = Credit.query.filter_by(production_id=production_id).all()
        elif job is None and production_id is None:
            # user only provided person_id
            results = Credit.query.filter_by(person_id=person_id).all()
        elif job is None:
            # user provided person_id and production_id
            results = Credit.query.filter_by(person_id=person_id, production_id=production_id).all()
        elif production_id is None and person_id is None:
            # user only provided job
            results = Credit.query.filter(
                Credit.title.ilike(f"%{job}%"),
            ).all()
        elif production_id is None:
            # user provided job and person_id
            results = Credit.query.filter(
                Credit.title.ilike(f"%{job}%"),
                Credit.person_id == person_id
            ).all()
        elif person_id is None:
            # user provided job and production_id
            results = Credit.query.filter(
                Credit.title.ilike(f"%{job}%"),
                Credit.production_id == production_id
            ).all()
        else:
            # user provided job, person_id and production_id
            results = Credit.query.filter(
                Credit.title.ilike(f"%{job}%"),
                Credit.production_id == production_id,
                Credit.person_id == person_id
            ).all()
        return Credit.serialize_list(results), HTTPStatus.OK

    @CREDITS.expect(EXPECT_MODEL)
    @CREDITS.marshal_with(SERIALIZE_MODEL)
    @create_credit
    def post(self, credit: Credit):
        return credit.serialize(), HTTPStatus.CREATED


@CREDITS.route("/<string:credit_id>")
class CreditById(AuthResource):
    @CREDITS.marshal_with(SERIALIZE_MODEL)
    @id_to_credit
    def get(self, credit: Credit):
        return credit.serialize(), HTTPStatus.OK

    @CREDITS.expect(EXPECT_MODEL)
    @CREDITS.marshal_with(SERIALIZE_MODEL)
    @update_credit
    def put(self, credit):
        return credit.serialize(), HTTPStatus.OK

    @CREDITS.marshal_with(SERIALIZE_MODEL)
    @CREDITS.expect(PATCH_MODEL)
    @update_credit
    def patch(self, credit):
        return credit.serialize(), HTTPStatus.OK

    @CREDITS.marshal_with(SERIALIZE_MODEL)
    @id_to_credit
    def delete(self, credit):
        credit.remove()
        return "", HTTPStatus.NO_CONTENT
