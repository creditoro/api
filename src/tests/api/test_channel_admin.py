"""
Test channel admins.
"""
from http import HTTPStatus

from tests.api.test_channels import ChannelsTest
from tests.base_test import BaseTestCase


class ChannelAdminTest(BaseTestCase):
    """ChannelsTest.
    """

    path = "channel_admins"

    def test_all(self):
        self.get_list()
        user_id = self.test_user.identifier
        channel = ChannelsTest(methodName="post")
        channel.setUp()
        channel_response = channel.post(json=channel.json())
        channel_id = channel_response.json.get("identifier")
        self.post(
            json=self.json(user_id=user_id, channel_id=channel_id))
        self.get_channel_admin(user_id=user_id, channel_id=channel_id)
        self.get_channel_admins()
        self.get_channel_admins_for_user(user_id=user_id)
        # self.delete_channel_admin(user_id=user_id, channel_id=channel_id)

    def delete_channel_admin(self, user_id: str, channel_id: str):
        response = self._delete(f"/{self.path}/{user_id}/{channel_id}")
        self.assertTrue(response.status_code == HTTPStatus.NO_CONTENT)
        return response

    def json(self, user_id: str = None, channel_id: str = None):
        return {"user_id": user_id, "channel_id": channel_id}

    def get_channel_admins(self):
        response = self._get(path=f"/{self.path}/")
        self.assertTrue(response.status_code == HTTPStatus.OK)
        return response

    def get_channel_admins_for_user(self, user_id: str):
        response = self._get(path=f"/{self.path}/{user_id}")
        self.assertTrue(response.status_code == HTTPStatus.OK)
        return response

    def get_channel_admin(self, user_id: str, channel_id: str):
        response = self._get(path=f"/{self.path}/{user_id}/{channel_id}")
        self.assertTrue(response.status_code == HTTPStatus.OK)
        return response

    def post(self, data: dict = None, json: dict = None):
        response = self._post(path=f"/{self.path}/", data=data, json=json)
        self.assertTrue(response.status_code == HTTPStatus.CREATED)
        return response
