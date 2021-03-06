"""
This module is for modelling the table "people" to an object Person.
"""
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from validate_email import validate_email

from creditoro_api.extensions import DB
from creditoro_api.models import Base


class Person(Base):
    """Person.
    """

    __tablename__ = "people"
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    phone = DB.Column(DB.String)
    email = DB.Column(DB.String)
    name = DB.Column(DB.String)

    def __init__(self, phone: str, email: str, name: str):
        """__init__.

        Args:
            phone (str): phone
            email (str): email
            name (str): name
        """
        self.identifier = uuid4()
        self.phone = phone
        self.email = email
        self.name = name

    def serialize_auth(self, authenticated: bool):
        """serialize.
        """
        if authenticated:
            return self.serialize()
        return {
            "identifier": str(self.identifier),
            "name": self.name
        }

    def serialize(self):
        return {
            "identifier": str(self.identifier),
            "phone": self.phone,
            "email": self.email,
            "name": self.name,
        }

    def update(self,
               phone: str = None,
               email: str = None,
               name: str = None,
               *_,
               **__) -> bool:
        """update.

        Args:
            phone (str): phone
            email (str): email
            name (str): name
            _:
            __:

        Returns:
            bool:
        """
        if phone is not None:
            self.phone = phone

        if email is not None:
            if validate_email(email):
                self.email = email
            else:
                return False

        if name is not None:
            self.name = name

        return self.store()

    @staticmethod
    def serialize_auth_list(list_to_serialize: [], authenticated: bool):
        """
        Serializes a list of self.
        example usage: return jsonify({"results": YourClass.serialize_list(data)})
        :return (list) of self as dict.
        """
        return [element.serialize_auth(authenticated=authenticated) for element in
                list_to_serialize]
