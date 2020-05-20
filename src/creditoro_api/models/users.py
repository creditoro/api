from enum import Enum
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from validate_email import validate_email
from werkzeug.security import generate_password_hash

from creditoro_api.extensions import DB
from creditoro_api.models import Base


class Role(Enum):
    """Role.
    """

    royalty_user = 20
    channel_admin = 50
    system_admin = 99


class User(Base):
    """User.
    """

    __tablename__ = "users"
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    name = DB.Column(DB.String)
    email = DB.Column(DB.String, index=True)
    phone = DB.Column(DB.String)
    role = DB.Column(DB.Enum(Role), nullable=False)
    created_at = DB.Column(DB.DateTime(timezone=True),
                           server_default=func.now())
    password = DB.Column(DB.String)

    def __init__(self, name: str, email: str, phone: str, password: str, *_,
                 **__):
        """__init__.

        Args:
            name (str): name
            email (str): email
            phone (str): phone
            password (str): password
            _:
            __:
        """
        self.name = name
        self.email = email
        self.phone = phone
        self.password = generate_password_hash(password, method="sha256")
        self.identifier = uuid4()
        self.role = Role.royalty_user

    def update(self,
               name: str = None,
               email: str = None,
               phone: str = None,
               password: str = None,
               *_,
               **__) -> bool:
        """update.

        Args:
            name (str): name
            email (str): email
            phone (str): phone
            password (str): password
            _:
            __:

        Returns:
            bool:
        """
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
            self.password = generate_password_hash(password=password,
                                                   method="sha256")
        return self.store()

    def serialize(self):
        """serialize.
        """
        return {
            "identifier": str(self.identifier),
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }
