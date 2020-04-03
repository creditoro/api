from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash

from src.extensions import DB
from src.models import Base


class User(Base):
    __tablename__ = "users"
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    name = DB.Column(DB.String)
    email = DB.Column(DB.String, index=True)
    phone = DB.Column(DB.String)
    created_at = DB.Column(DB.DateTime(timezone=True), server_default=func.now())
    password = DB.Column(DB.String)

    def __init__(self, name: str, email: str, phone: str, password: str, *_, **__):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = generate_password_hash(password, method="sha256")
        self.identifier = uuid4()
