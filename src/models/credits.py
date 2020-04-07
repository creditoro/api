from sqlalchemy.dialects.postgresql import UUID

from src.models import Base
from src.extensions import DB


class Credit(Base):
    __tablename__ = "credits"
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    job = DB.Column(DB.String)

    production_id = DB.Column(UUID(as_uuid=True), DB.ForeignKey("productions.identifier"))
    person_id = DB.Column(UUID(as_uuid=True), DB.ForeignKey("users.identifier"))

    person = DB.relationship("User")
    production = DB.relationship("User")
