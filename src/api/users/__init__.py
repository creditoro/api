import datetime
from http import HTTPStatus

import jwt
from flask import current_app, request
from flask_restplus import Namespace, Resource
from sqlalchemy import or_

from src.api.auth_resource import AuthResource
from src.api.users.decorators import id_to_user, create_user, check_password, token_required
from src.api.users.fields import SERIALIZE_FIELDS, SIGNUP_FIELDS, LOGIN_FIELDS
from src.models.users import User

USERS = Namespace(name="users", description="Endpoints for users.")

MODEL = USERS.model(name="user_model", model=SERIALIZE_FIELDS)
SIGNUP_MODEL = USERS.model(name="users_signup_model", model=SIGNUP_FIELDS)
LOGIN_MODEL = USERS.model(name="auth_model", model=LOGIN_FIELDS)


@USERS.route("/")
class ListUsers(Resource):
    @USERS.marshal_list_with(MODEL)
    @USERS.param(name="q", description="query property, search for name, email and role.")
    def get(self):
        query_prop = request.args.get("q", None)
        if query_prop is None:
            results = User.query.all()
        else:
            q = f"%{query_prop}%"
            query = User.query.filter(
                or_(
                    User.name.ilike(q),
                    User.email.ilike(q)
                )
            )
            results = query.all()
        return User.serialize_list(results), HTTPStatus.OK

    @USERS.expect(SIGNUP_MODEL)
    @USERS.marshal_with(MODEL)
    @create_user
    def post(self, user: User):
        # send_confirmation_email(user=user)
        return user.serialize(), HTTPStatus.CREATED


@USERS.route("/<string:user_id>")
class UserById(AuthResource):
    @USERS.marshal_with(MODEL)
    @id_to_user
    def get(self, user: User):
        return user.serialize(), HTTPStatus.OK

    @USERS.marshal_with(MODEL)
    @id_to_user
    def update(self, user):
        # TODO(HTTP Update provide all keys.)
        return user.serialize(), HTTPStatus.OK

    @USERS.marshal_with(MODEL)
    @id_to_user
    def patch(self, user):
        # TODO(provide a single key and update its value, let everything else remain as it is.)
        return user.serialize(), HTTPStatus.OK

    @USERS.marshal_with(MODEL)
    @id_to_user
    def delete(self, user):
        if user.remove():
            # 2XX - success
            # 4XX - Client error
            # 5XX - Server error
            return "", HTTPStatus.NO_CONTENT  # 204
        return "", HTTPStatus.INTERNAL_SERVER_ERROR  # 500


@USERS.route("/login")
class UserLogin(Resource):
    @USERS.expect(LOGIN_MODEL)
    @check_password
    def post(self, user: User):
        token = jwt.encode(payload={"email": user.email,
                                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           key=current_app.config["SECRET_KEY"],
                           algorithm="HS256")

        return {"token": token.decode("UTF-8")}, HTTPStatus.OK
