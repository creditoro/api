"""
This class is the ORM for channels.
"""
import uuid

from sqlalchemy.dialects.postgresql import UUID

from creditoro_api.extensions import DB
from creditoro_api.models import Base


class Channel(Base):
    """Channel.
    """

    __tablename__ = "channels"
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    name = DB.Column(DB.String, unique=True)
    icon_url = DB.Column(DB.String)

    def __init__(self, name: str, icon_url: str, *_, **__):
        """__init__.

        Args:
            name (str): name
            icon_url (str): icon_url
            _:
            __:
        """
        self.name = name
        self.identifier = uuid.uuid4()
        self.icon_url = icon_url

    def serialize(self):
        """serialize.
        """
        return {
            "identifier": str(self.identifier),
            "name": self.name,
            "icon_url": self.icon_url,
        }
