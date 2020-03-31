from sqlalchemy.dialects.postgresql import UUID

from src.models import Base
from src.extensions import DB


class Permission(Base):
    __tablename__ = "permissions"
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    name = DB.Column(DB.String, unique=True)
