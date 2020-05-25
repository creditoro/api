"""
This module is for routes in the /people endpoint.
"""
from http import HTTPStatus

from flask import request, g
from flask_restplus import Namespace, Resource

from creditoro_api.api.auth_resource import AuthResource
from creditoro_api.api.decorators import is_sys_admin, token_required
from creditoro_api.api.people.decorators import (
    id_to_person,
    create_person,
    update_person,
)
from creditoro_api.api.people.fields import (
    SERIALIZE_FIELDS,
    EXPECT_FIELDS,
    PATCH_FIELDS,
)
from creditoro_api.models.people import Person

PEOPLE = Namespace(name="people", description="Endpoints for people.")

SERIALIZE_MODEL = PEOPLE.model(name="person_model", model=SERIALIZE_FIELDS)
EXPECT_MODEL = PEOPLE.model(name="people_except_model", model=EXPECT_FIELDS)
PATCH_MODEL = PEOPLE.model(name="people_patch_model", model=PATCH_FIELDS)


@PEOPLE.route("/")
class ListPeople(Resource):
    """ListPeople.
    """
    @PEOPLE.param(name="name", description="search for people with this name.")
    @PEOPLE.param(name="email", description="search for people by email.")
    def get(self):
        """get.
        """
        name = request.args.get("name", None)
        email = request.args.get("email", None)
        if name is None and email is None:
            # user provid no parameters, query it all.
            results = Person.query.all()
        elif email is None:
            # user provided name
            query = Person.query.filter(Person.name.ilike(f"%{name}%"), )
            results = query.all()
        elif name is None:
            # user provided email
            results = Person.query.filter(Person.email == email).all()
        else:
            # user provided both name and email
            results = Person.query.filter(
                Person.name.ilike(f"%{name}%"),
                Person.email == email,
            ).all()
        authenticated = "current_user" in g
        return Person.serialize_auth_list(
            list_to_serialize=results,
            authenticated=authenticated), HTTPStatus.OK

    @PEOPLE.expect(EXPECT_MODEL)
    @PEOPLE.marshal_with(SERIALIZE_MODEL)
    @token_required
    @create_person
    def post(self, person: Person):
        """post.

        Args:
            person (Person): The person to serialize.
        """
        return person.serialize(), HTTPStatus.CREATED


@PEOPLE.route("/<string:person_id>")
class PersonById(AuthResource):
    """PersonById.
    """
    @id_to_person
    def get(self, person: Person):
        """get.

        Args:
            person (Person): person
        """
        authenticated = "current_user" in g
        return person.serialize_auth(authenticated), HTTPStatus.OK

    @PEOPLE.expect(EXPECT_MODEL)
    @PEOPLE.marshal_with(SERIALIZE_MODEL)
    @update_person
    def put(self, person):
        """put.

        Args:
            person: The person to serialize.
        """
        return person.serialize(), HTTPStatus.OK

    @PEOPLE.marshal_with(SERIALIZE_MODEL)
    @PEOPLE.expect(PATCH_MODEL)
    @update_person
    def patch(self, person):
        """patch.

        Args:
            person: The person to serialize.
        """
        return person.serialize(), HTTPStatus.OK

    @PEOPLE.marshal_with(SERIALIZE_MODEL)
    @is_sys_admin
    @id_to_person
    def delete(self, person):
        """delete.

        Args:
            person: The person to delete.
        """
        person.remove()
        return "", HTTPStatus.NO_CONTENT
