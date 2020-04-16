from http import HTTPStatus

from tests.base_test import BaseTestCase


class UsersTest(BaseTestCase):
    def test_get_users(self):
        with self.client:
            response = self.client.get("/users/", headers={"Authorization": self.token}, data={"q": "test"})
            self.assertTrue(response.status_code == HTTPStatus.OK)

    def test_patch_users(self):
        with self.client:
            response = self.client.patch(f"/users/{self.test_user.identifier}", headers={"Authorization": self.token},
                                         json={"name": "patched"})
            self.assertTrue(response.status_code == HTTPStatus.OK)
