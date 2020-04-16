from enum import Enum
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from validate_email import validate_email
from werkzeug.security import generate_password_hash

from src.extensions import DB
from src.models import Base


class Role(Enum):
    royalty_user = 20
    channel_admin = 50
    system_admin = 99


class User(Base):
    __tablename__ = "users"
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    name = DB.Column(DB.String)
    email = DB.Column(DB.String, index=True)
    phone = DB.Column(DB.String)
    role = DB.Column(DB.Enum(Role), nullable=False)
    created_at = DB.Column(DB.DateTime(timezone=True), server_default=func.now())
    password = DB.Column(DB.String)

    def __init__(self, name: str, email: str, phone: str, password: str, *_, **__):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = generate_password_hash(password, method="sha256")
        self.identifier = uuid4()
        self.role = Role.royalty_user

    def update(self, name: str = None, email: str = None, phone: str = None, password: str = None, *_, **__) -> bool:
        if name is not None:
            self.name = name

        if email is not None:
            if validate_email(email):
                self.email = email
            else:
                # TODO replace with raise custom invalid email exception
                return False

        if phone is not None:
            self.phone = phone

        if password is not None:
            self.password = generate_password_hash(password=password, method="sha256")
        return self.store()
