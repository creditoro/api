from sqlalchemy.dialects.postgresql import UUID

from src.models import Base
from src.extensions import DB


class ChannelAdmin(Base):
    __tablename__ = "channel_admins"
    user_uuid = DB.Column(UUID(as_uuid=True), DB.ForeignKey("users.identifier"), primary_key=True)
    channel_uuid = DB.Column(UUID(as_uuid=True), DB.ForeignKey("channels.identifier"), primary_key=True)

    user = DB.relationship("User")
    channel = DB.relationship("Channel")

    def __init__(self, user_uuid: str, channel_uuid: str, *_, **__):
        self.user_uuid = user_uuid
        self.channel_uuid = channel_uuid

    def serialize(self):
        return {
            "user_uuid": str(self.user_uuid),
            "channel_uuid": str(self.channel_uuid)
        }