from sqlalchemy.dialects.postgresql import UUID

from src.models import Base
from src.extensions import DB


class RolePermission(Base):
    __tablename__ = "role_permissions"
    role_id = DB.Column(UUID(as_uuid=True), DB.ForeignKey("roles.identifier"), primary_key=True)
    permission_id = DB.Column(UUID(as_uuid=True), DB.ForeignKey("permissions.identifier"), primary_key=True)

    role = DB.relationship("Role")
    permission = DB.relationship("Permission")
