import uuid

from sqlalchemy.dialects.postgresql import UUID

from src.extensions import DB
from src.models import Base


class Channel(Base):
    __tablename__ = "channels"
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    name = DB.Column(DB.String, unique=True)

    def __init__(self, name: str, *_, **__):
        self.name = name
        self.identifier = uuid.uuid4()

    def serialize(self):
        return {
            "identifier": str(self.identifier),
            "name": self.name
        }