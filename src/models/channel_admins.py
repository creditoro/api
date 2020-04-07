from sqlalchemy.dialects.postgresql import UUID

from src.models import Base
from src.extensions import DB


class ChannelAdmin(Base):
    __tablename__ = "channel_admins"
    user_uuid = DB.Column(UUID(as_uuid=True), primary_key=True)
    channel_uuid = DB.Column(UUID(as_uuid=True), primary_key=True)

    user = DB.relationship("User")
    channel = DB.relationship("Channel")
