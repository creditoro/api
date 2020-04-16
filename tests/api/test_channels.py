from http import HTTPStatus

from tests.base_test import BaseTestCase


class ChannelsTest(BaseTestCase):
    path = "/channels/"

    def test_get_channels(self):
        with self.client:
            response = self.client.get(path=self.path, data={"q": "TV2"})
            self.assertTrue(response.status_code == HTTPStatus.OK)

    def test_post_channels(self):
        with self.client:
            response = self.post(path=self.path, json={"name": "test_channel"})
            self.assertTrue(response.status_code == HTTPStatus.CREATED)
            identifier = response.json["identifier"]
            delete_response = self.delete(f"{self.path}{identifier}")
            self.assertTrue(delete_response.status_code == HTTPStatus.NO_CONTENT)
