from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID

from src.extensions import DB
from src.models import Base


class Channel(Base):
    __tablename__ = "channels"
    name = DB.Column(DB.String)
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    contact_id = DB.Column(UUID(as_uuid=True), DB.Column(DB.ForeignKey("users.identifier")))
    contact = DB.relationship("Contact")

    created_at = DB.Column(DB.DateTime(timezone=True), server_default=func.now())
    updated_at = DB.Column(DB.DateTime(timezone=True), onupdate=func.now())
