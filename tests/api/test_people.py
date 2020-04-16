from http import HTTPStatus

from tests.base_test import BaseTestCase


class PeopleTest(BaseTestCase):

    def test_all(self):
        self.get_people()
        post_response = self.post_person()
        person_id = post_response.json.get("identifier")
        self.patch_person(person_id=person_id)
        self.put_person(person_id=person_id)
        self.get_person(person_id=person_id)
        self.delete_person(person_id=person_id)

    def test_post(self):
        post_response = self.post_person()
        return post_response.json.get("identifier")

    def get_people(self):
        response = self.get(path="/people/")
        self.assertTrue(response.status_code == HTTPStatus.OK)
        return response

    def get_person(self, person_id):
        response = self.get(path=f"/people/{person_id}")
        self.assertTrue(response.status_code == HTTPStatus.OK)
        return response

    def post_person(self):
        response = self.post(path="/people/",
                             json={"phone": "+45 88 88 88 88",
                                   "email": "test@creditoro.nymann.dev",
                                   "name": "test"})
        self.assertTrue(response.status_code == HTTPStatus.CREATED)
        return response

    def patch_person(self, person_id: str):
        response = self.patch(path=f"/people/{person_id}", json={"phone": "+45 88 88 88 44"})
        self.assertTrue(response.status_code == HTTPStatus.OK)
        return response

    def put_person(self, person_id: str):
        response = self.put(path=f"/people/{person_id}",
                            json={"phone": "+45 88 88 88 83",
                                  "email": "test-put@creditoro.nymann.dev",
                                  "name": "test-put"})
        self.assertTrue(response.status_code == HTTPStatus.OK)
        return response

    def delete_person(self, person_id: str):
        response = self.delete(f"/people/{person_id}")
        self.assertTrue(response.status_code == HTTPStatus.NO_CONTENT)

        return response
