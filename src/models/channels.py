from sqlalchemy.dialects.postgresql import UUID

from src.extensions import DB
from src.models import Base


class Channel(Base):
    __tablename__ = "channels"
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    name = DB.Column(DB.String, unique=True)
