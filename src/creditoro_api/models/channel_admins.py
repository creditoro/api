"""
This module is for mapping a User to a channel, and thereby becoming a channel
admin.
"""
from sqlalchemy.dialects.postgresql import UUID

from creditoro_api.extensions import DB
from creditoro_api.models import Base


class ChannelAdmin(Base):
    """ChannelAdmin.
    """

    __tablename__ = "channel_admins"
    user_id = DB.Column(UUID(as_uuid=True),
                        DB.ForeignKey("users.identifier"),
                        primary_key=True)
    channel_id = DB.Column(UUID(as_uuid=True),
                           DB.ForeignKey("channels.identifier"),
                           primary_key=True)

    user = DB.relationship("User")
    channel = DB.relationship("Channel")

    def serialize(self):
        return {
            "channel": self.channel.serialize(),
            "user": self.user.serialize()
        }
