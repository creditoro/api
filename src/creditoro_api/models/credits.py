from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from creditoro_api.extensions import DB
from creditoro_api.models import Base


class Credit(Base):
    __tablename__ = "credits"
    identifier = DB.Column(UUID(as_uuid=True), primary_key=True)
    job = DB.Column(DB.String)

    production_id = DB.Column(UUID(as_uuid=True), DB.ForeignKey("productions.identifier"))
    person_id = DB.Column(UUID(as_uuid=True), DB.ForeignKey("users.identifier"))

    person = DB.relationship("User")
    production = DB.relationship("User")

    def __init__(self, production_id: UUID, person_id: UUID, job: str):
        self.identifier = uuid4()
        self.production_id = production_id
        self.person_id = person_id
        self.job = job

    def update(self, production_id: UUID = None, person_id: UUID = None, job: str = None, *_, **__) -> bool:
        if production_id is not None:
            self.production_id = production_id

        if person_id is not None:
            self.person_id = person_id

        if job is not None:
            self.job = job

        return self.store()

    def serialize(self):
        return {
            "identifier": str(self.identifier),
            "production": self.production.serialize(),
            "person": self.person.serialize(),
            "job": self.job,
        }
