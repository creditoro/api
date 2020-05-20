from http import HTTPStatus

from flask import request
from flask_restplus import Namespace, Resource

from creditoro_api.api.auth_resource import AuthResource
from creditoro_api.api.people.decorators import id_to_person, create_person, update_person
from creditoro_api.api.people.fields import SERIALIZE_FIELDS, EXPECT_FIELDS, PATCH_FIELDS
from creditoro_api.models.people import Person

PEOPLE = Namespace(name="people", description="Endpoints for people.")

SERIALIZE_MODEL = PEOPLE.model(name="person_model", model=SERIALIZE_FIELDS)
EXPECT_MODEL = PEOPLE.model(name="people_except_model", model=EXPECT_FIELDS)
PATCH_MODEL = PEOPLE.model(name="people_patch_model", model=PATCH_FIELDS)


@PEOPLE.route("/")
class ListPeople(Resource):
    @PEOPLE.marshal_list_with(SERIALIZE_MODEL)
    @PEOPLE.param(name="name", description="search for people with this name.")
    def get(self):
        name = request.args.get("name", None)
        if name is None:
            results = Person.query.all()
        else:
            q = f"%{name}%"
            query = Person.query.filter(
                Person.name.ilike(q),
            )
            results = query.all()
        return Person.serialize_list(results), HTTPStatus.OK

    @PEOPLE.expect(EXPECT_MODEL)
    @PEOPLE.marshal_with(SERIALIZE_MODEL)
    @create_person
    def post(self, person: Person):
        return person.serialize(), HTTPStatus.CREATED


@PEOPLE.route("/<string:person_id>")
class PersonById(AuthResource):
    @PEOPLE.marshal_with(SERIALIZE_MODEL)
    @id_to_person
    def get(self, person: Person):
        return person.serialize(), HTTPStatus.OK

    @PEOPLE.expect(EXPECT_MODEL)
    @PEOPLE.marshal_with(SERIALIZE_MODEL)
    @update_person
    def put(self, person):
        return person.serialize(), HTTPStatus.OK

    @PEOPLE.marshal_with(SERIALIZE_MODEL)
    @PEOPLE.expect(PATCH_MODEL)
    @update_person
    def patch(self, person):
        return person.serialize(), HTTPStatus.OK

    @PEOPLE.marshal_with(SERIALIZE_MODEL)
    @id_to_person
    def delete(self, person):
        person.remove()
        return "", HTTPStatus.NO_CONTENT
