import unittest

import config
from src import create_app
from src.models.productions import Production
from src.models.users import User


class BaseTestCase(unittest.TestCase):
    testing_email = "test@creditoro.nymann.dev"

    def setUp(self) -> None:
        self.app = create_app(config.CONFIG_DICT["TEST"])
        self.client = self.app.test_client()
        self.login()

    def login(self):
        with self.app.app_context():
            self.test_user = User.query.filter_by(email=self.testing_email).one_or_none()
            if not self.test_user:
                self.test_user = User(name="test", email=self.testing_email, phone="42424242", password="test")
                self.test_user.store()
            response = self.client.post("/users/login", json={"email": self.testing_email, "password": "test"})
            self.token = response.json["token"]

    def tearDown(self) -> None:
        # remove created user
        with self.app.app_context():
            self.test_user = User.query.filter_by(email=self.testing_email).one_or_none()
            productions = Production.query.filter_by(producer_id=self.test_user.identifier).all()
            for production in productions:
                production.remove()
            self.test_user.remove()

    def post(self, path: str, data: dict = None, json: dict = None):
        return self.client.post(path, headers={"Authorization": self.token}, json=json, data=data)

    def patch(self, path: str, data: dict = None, json: dict = None):
        return self.client.patch(path, headers={"Authorization": self.token}, json=json, data=data)

    def put(self, path: str, data: dict = None, json: dict = None):
        return self.client.put(path, headers={"Authorization": self.token}, json=json, data=data)

    def get(self, path: str, data: dict = None, json: dict = None):
        return self.client.get(path, headers={"Authorization": self.token}, json=json, data=data)

    def delete(self, path: str, data: dict = None, json: dict = None):
        return self.client.delete(path, headers={"Authorization": self.token}, json=json, data=data)
