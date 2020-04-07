from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID

from src.models import Base
from src.extensions import DB


class Production(Base):
    __tablename__ = "productions"
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    title = DB.Column(DB.String)

    producer_id = DB.Column(UUID(as_uuid=True), DB.ForeignKey("users.identifier"))
    channel_id = DB.Column(DB.String, DB.ForeignKey("channels.identifier"))

    producer = DB.relationship("User")
    channel = DB.relationship("Channel")

    created_at = DB.Column(DB.DateTime(timezone=True), server_default=func.now())
