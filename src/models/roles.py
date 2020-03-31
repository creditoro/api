from sqlalchemy.dialects.postgresql import UUID

from src.models import Base
from src.extensions import DB


class Role(Base):
    __tablename__ = "roles"
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    name = DB.Column(DB.String, unique=True)
    description = DB.Column(DB.Text)
