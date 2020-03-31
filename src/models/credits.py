from sqlalchemy.dialects.postgresql import UUID

from src.models import Base
from src.extensions import DB


class Credit(Base):
    __tablename__ = "credits"
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    program_id = DB.Column(UUID(as_uuid=True), DB.ForeignKey("programs.identifier"))
    user_id = DB.Column(UUID(as_uuid=True), DB.ForeignKey("users.identifier"))
    role = DB.Column(DB.String)

    user = DB.relationship("User")
