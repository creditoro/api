from sqlalchemy.dialects.postgresql import UUID

from src.models import Base
from src.extensions import DB


class Person(Base):
    __tablename__ = "people"
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    phone_number = DB.Column(DB.String)
    email = DB.Column(DB.String)
    name = DB.Column(DB.String)

    def serialize(self):
        return {
            "identifier": str(self.identifier),
            "phone_number": self.phone_number,
            "email": self.email,
            "name": self.name
        }
