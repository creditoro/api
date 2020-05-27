"""
This module is for decorators used by /credits
"""

from http import HTTPStatus

from flask import request
from flask_restplus import Namespace, Resource
from creditoro_api.api.credits.decorators import can_alter_credit
from creditoro_api.api.auth_resource import AuthResource
from creditoro_api.api.credits.decorators import (
    id_to_credit,
    create_credit,
    update_credit,
)
from creditoro_api.api.credits.fields import (
    SERIALIZE_FIELDS,
    EXPECT_FIELDS,
    PATCH_FIELDS,
    POST_FIELDS,
)
from creditoro_api.models.credits import Credit

CREDITS = Namespace(name="credits", description="Endpoints for credits.")

SERIALIZE_MODEL = CREDITS.model(name="credit_model", model=SERIALIZE_FIELDS)
EXPECT_MODEL = CREDITS.model(name="credits_except_model", model=EXPECT_FIELDS)
PATCH_MODEL = CREDITS.model(name="credits_patch_model", model=PATCH_FIELDS)
POST_MODEL = CREDITS.model(name="credits_post_model", model=POST_FIELDS)


@CREDITS.route("/")
class ListCredits(Resource):
    """ListCredits.
    """
    @CREDITS.marshal_list_with(SERIALIZE_MODEL)
    @CREDITS.param(name="name",
                   description="search for credits with this job.")
    @CREDITS.param(name="person_id",
                   description="search for credits by this person_id.")
    @CREDITS.param(
        name="production_id",
        description="search for credited people for this production_id.",
    )
    def get(self):
        """get.
        """
        job = request.args.get("job", None)
        person_id = request.args.get("person_id", None)
        production_id = request.args.get("production_id", None)
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
            results = Credit.query.filter(
                Credit.person_id == person_id,
                Credit.production_id == production_id).all()
        elif production_id is None and person_id is None:
            # user only provided job
            results = Credit.query.filter(
                Credit.title.ilike(f"%{job}%"), ).all()
        elif production_id is None:
            # user provided job and person_id
            results = Credit.query.filter(Credit.title.ilike(f"%{job}%"),
                                          Credit.person_id == person_id).all()
        elif person_id is None:
            # user provided job and production_id
            results = Credit.query.filter(
                Credit.title.ilike(f"%{job}%"),
                Credit.production_id == production_id).all()
        else:
            # user provided job, person_id and production_id
            results = Credit.query.filter(
                Credit.title.ilike(f"%{job}%"),
                Credit.production_id == production_id,
                Credit.person_id == person_id,
            ).all()
        return Credit.serialize_list(results), HTTPStatus.OK

    @CREDITS.expect(POST_MODEL)
    @CREDITS.marshal_with(SERIALIZE_MODEL)
    @create_credit
    def post(self, credit: Credit):
        """post.

        Args:
            credit (Credit): credit
        """
        return credit.serialize(), HTTPStatus.CREATED


@CREDITS.route("/<string:credit_id>")
class CreditById(AuthResource):
    """CreditById.
    """
    @CREDITS.marshal_with(SERIALIZE_MODEL)
    @id_to_credit
    def get(self, credit: Credit):
        """get.

        Args:
            credit (Credit): credit
        """
        return credit.serialize(), HTTPStatus.OK

    @CREDITS.expect(EXPECT_MODEL)
    @CREDITS.marshal_with(SERIALIZE_MODEL)
    @can_alter_credit
    @update_credit
    def put(self, credit):
        """put.

        Args:
            credit:
        """
        return credit.serialize(), HTTPStatus.OK

    @CREDITS.marshal_with(SERIALIZE_MODEL)
    @CREDITS.expect(PATCH_MODEL)
    @can_alter_credit
    @update_credit
    def patch(self, credit):
        """patch.

        Args:
            credit:
        """
        return credit.serialize(), HTTPStatus.OK

    @CREDITS.marshal_with(SERIALIZE_MODEL)
    @can_alter_credit
    def delete(self, credit):
        """delete.

        Args:
            credit:
        """
        credit.remove()
        return "", HTTPStatus.NO_CONTENT
