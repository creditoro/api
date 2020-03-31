from uuid import uuid4

from flask import current_app
from itsdangerous import URLSafeTimedSerializer, BadData
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash

from src.extensions import DB
from src.models import Base


class User(Base):
    __tablename__ = "users"
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    given_name = DB.Column(DB.String)
    surname = DB.Column(DB.String)
    email = DB.Column(DB.String, index=True)
    phone = DB.Column(DB.String)
    created_at = DB.Column(DB.DateTime(timezone=True), server_default=func.now())
    updated_at = DB.Column(DB.DateTime(timezone=True), onupdate=func.now())
    password = DB.Column(DB.String)
    verified = DB.Column(DB.Boolean, default=False)

    def __init__(self, given_name: str, surname: str, email: str, phone: str, password: str, *_, **__):
        self.given_name = given_name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.password = generate_password_hash(password, method="sha256")
        self.identifier = uuid4()

    def generate_confirmation_token(self):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(self.email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

    @staticmethod
    def confirm_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=current_app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except BadData as _:
            return False
        return email
