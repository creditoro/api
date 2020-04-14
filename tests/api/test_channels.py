from http import HTTPStatus

from tests.base_test import BaseTestCase


class ChannelsTest(BaseTestCase):
    def test_get_channels(self):
        with self.client:
            response = self.client.get("/channels/", headers={"Authorization": self.token}, data={"q": "TV2"})
            status_code = response.status_code
            self.assertTrue(status_code == HTTPStatus.OK)

