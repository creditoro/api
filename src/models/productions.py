from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID

from src.models import Base
from src.extensions import DB


class Production(Base):
    __tablename__ = "productions"
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    title = DB.Column(DB.String)
    description = DB.Column(DB.TEXT)

    producer_id = DB.Column(UUID(as_uuid=True), DB.ForeignKey("users.identifier"))
    channel_id = DB.Column(DB.String, DB.ForeignKey("channels.identifier"))

    producer = DB.relationship("User")
    channel = DB.relationship("Channel")

    created_at = DB.Column(DB.DateTime(timezone=True), server_default=func.now())

    def __init__(self, title: str, producer_id, channel_id, description: str):
        self.identifier = uuid4()
        self.title = title
        self.producer_id = producer_id
        self.channel_id = channel_id
        self.description = description

    def update(self, title: str = None, producer_id=None, channel_id=None, description: str = None, *_, **__) -> bool:
        if title is not None:
            self.title = title

        if producer_id is not None:
            self.producer_id = producer_id

        if channel_id is not None:
            self.channel_id = channel_id
        
        if description is not None:
            self.description = description

        return self.store()

    def serialize(self):
        return {
            "identifier": str(self.identifier),
            "title": self.title,
            "producer": self.producer.serialize(),
            "channel": self.channel.serialize(),
            "description": self.description
        }
