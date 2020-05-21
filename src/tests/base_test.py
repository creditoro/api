import string
import unittest
from http import HTTPStatus
import random

import config
from creditoro_api import create_app
from creditoro_api.models.productions import Production
from creditoro_api.models.users import User


class BaseTestCase(unittest.TestCase):
    testing_email = "test@creditoro.nymann.dev"
    path = ""

    def setUp(self) -> None:
        self.app = create_app(config.CONFIG_DICT["TEST"])
        self.client = self.app.test_client()
        self.login()

    def login(self):
        with self.app.app_context():
            self.test_user = User.query.filter_by(
                email=self.testing_email).one_or_none()
            if not self.test_user:
                self.test_user = User(name="test",
                                      email=self.testing_email,
                                      phone="42424242",
                                      password="test")
                self.test_user.store()
            response = self.client.post("/users/login",
                                        json={
                                            "email": self.testing_email,
                                            "password": "test"
                                        })
            self.token = response.headers["token"]
            self.headers = {"Authorization": self.token}

    def tearDown(self) -> None:
        # remove created user
        with self.app.app_context():
            self.test_user = User.query.filter_by(
                email=self.testing_email).one_or_none()
            productions = Production.query.filter_by(
                producer_id=self.test_user.identifier).all()
            for production in productions:
                production.remove()
            self.test_user.remove()

    def _post(self, path: str, data: dict = None, json: dict = None):
        return self.client.post(path,
                                headers=self.headers,
                                json=json,
                                data=data)

    def _patch(self, path: str, data: dict = None, json: dict = None):
        return self.client.patch(path,
                                 headers=self.headers,
                                 json=json,
                                 data=data)

    def _put(self, path: str, data: dict = None, json: dict = None):
        return self.client.put(path,
                               headers=self.headers,
                               json=json,
                               data=data)

    def _get(self, path: str, data: dict = None, json: dict = None):
        return self.client.get(path,
                               headers=self.headers,
                               json=json,
                               data=data)

    def _delete(self, path: str, data: dict = None, json: dict = None):
        return self.client.delete(path,
                                  headers=self.headers,
                                  json=json,
                                  data=data)

    def get_list(self):
        response = self._get(path=f"/{self.path}/")
        self.assertTrue(response.status_code == HTTPStatus.OK)
        return response

    def get(self, identifier):
        response = self._get(path=f"/{self.path}/{identifier}")
        self.assertTrue(response.status_code == HTTPStatus.OK)
        return response

    def post(self, data: dict = None, json: dict = None):
        response = self._post(path=f"/{self.path}/", data=data, json=json)
        self.assertTrue(response.status_code == HTTPStatus.CREATED)
        return response

    def patch(self, identifier: str, data: dict = None, json: dict = None):
        response = self._patch(path=f"/{self.path}/{identifier}",
                               data=data,
                               json=json)
        self.assertTrue(response.status_code == HTTPStatus.OK)
        return response

    def put(self, identifier: str, data: dict = None, json: dict = None):
        response = self._put(path=f"/{self.path}/{identifier}",
                             data=data,
                             json=json)
        self.assertTrue(response.status_code == HTTPStatus.OK)
        return response

    def delete(self, identifier: str):
        response = self._delete(f"/{self.path}/{identifier}")
        self.assertTrue(response.status_code == HTTPStatus.NO_CONTENT)
        return response

    @staticmethod
    def random_string(length: int = 7):
        return "".join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(length))
