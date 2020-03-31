from sqlalchemy.dialects.postgresql import UUID

from src.models import Base
from src.extensions import DB


class UserRole(Base):
    __tablename__ = "user_roles"
    user_id = DB.Column(UUID(as_uuid=True), DB.ForeignKey("users.identifier"), primary_key=True)
    role_id = DB.Column(UUID(as_uuid=True), DB.ForeignKey("roles.identifier"), primary_key=True)

    user = DB.relationship("User")
    role = DB.relationship("Role")
