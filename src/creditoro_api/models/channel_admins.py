from sqlalchemy.dialects.postgresql import UUID

from creditoro_api.models import Base
from creditoro_api.extensions import DB


class ChannelAdmin(Base):
    __tablename__ = "channel_admins"
    user_uuid = DB.Column(UUID(as_uuid=True), primary_key=True)
    channel_uuid = DB.Column(UUID(as_uuid=True), primary_key=True)

    user = DB.relationship("User")
    channel = DB.relationship("Channel")
