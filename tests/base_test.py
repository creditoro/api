import unittest

import config
from src import create_app
from src.models.users import User


class BaseTestCase(unittest.TestCase):
    testing_email = "test@creditoro.nymann.dev"

    def setUp(self) -> None:
        self.app = create_app(config.CONFIG_DICT["TEST"])
        self.client = self.app.test_client()
        self.login()

    def login(self):
        with self.app.app_context():
            test_user = User.query.filter_by(email=self.testing_email).one_or_none()
            if not test_user:
                test_user = User(name="test", email=self.testing_email, phone="42424242", password="test")
                test_user.store()
            response = self.client.post("/users/login", json={"email": self.testing_email, "password": "test"})
            self.token = response.json["token"]

    def tearDown(self) -> None:
        # remove created user
        with self.app.app_context():
            test_user = User.query.filter_by(email="test@creditoro.nymann.dev").one_or_none()
            test_user.remove()
