import datetime
from http import HTTPStatus

from flask import current_app, request, g
from flask_restplus import Namespace, Resource
import jwt

from src.api.auth_resource import AuthResource
from src.mail import send_confirmation_email
from src.models.users import User
from src.api.users.decorators import id_to_user, create_user, check_password, token_required
from src.api.users.fields import SERIALIZE_FIELDS, SIGNUP_FIELDS, LOGIN_FIELDS

USERS = Namespace(name="users", description="Endpoints for users.")

MODEL = USERS.model(name="user_model", model=SERIALIZE_FIELDS)
SIGNUP_MODEL = USERS.model(name="users_signup_model", model=SIGNUP_FIELDS)
LOGIN_MODEL = USERS.model(name="auth_model", model=LOGIN_FIELDS)


@USERS.route("/")
class Users(Resource):
    @USERS.marshal_list_with(MODEL)
    @USERS.doc(security="apikey")
    @token_required
    def get(self):
        results = User.query.all()
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
    @USERS.doc(security="apikey")
    @id_to_user
    def get(self, user):
        return user.serialize(), HTTPStatus.OK


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


@USERS.route("/confirm")
class ConfirmUser(Resource):
    @USERS.param("token")
    def post(self):
        token = request.args.get("token", None)
        if token is None:
            return "Provide a token", HTTPStatus.BAD_REQUEST
        email = User.confirm_token(token=token)
        if email is False:
            return "The confirmation link is invalid or has expired", HTTPStatus.BAD_REQUEST
        user = User.query.filter_by(email=email).one_or_none()
        if user.verified:
            return "User is already verified", HTTPStatus.NOT_MODIFIED
        user.verified = True
        user.store()
        return user.serialize(), HTTPStatus.OK

    @USERS.doc(security="apikey")
    @token_required
    def get(self):
        user = g.current_user
        if user is None:
            return "User is not logged in", HTTPStatus.UNAUTHORIZED
        if not user.verified:
            send_confirmation_email(user=user)
            return "confirmation email sent", HTTPStatus.OK

        return "Your email is already confirmed", HTTPStatus.NO_CONTENT
