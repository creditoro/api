"""
This module is for testing production
"""
from http import HTTPStatus

from tests.api.test_channels import ChannelsTest
from tests.base_test import BaseTestCase


class ProductionsTest(BaseTestCase):
    """ProductionsTest.
    """

    path = "productions"

    def test_all(self):
        """test_all.
        """
        self.get_list()
        channel = ChannelsTest(methodName="post")
        channel.setUp()

        channel_response = channel.post(json=channel.json())
        channel_id = channel_response.json.get("identifier")

        response = self.post(json=self.json(channel_id=channel_id))
        identifier = response.json.get("identifier")
        self.patch(identifier=identifier, json=self.patch_json())
        self.get(identifier=identifier)
        self.put(identifier=identifier, json=self.json(channel_id=channel_id))
        self.delete(identifier=identifier)
        channel.delete(channel_id)

    def json(self,
             channel_id: str,
             title: str = None,
             producer_id: str = None,
             description: str = None):
        """json.

        Args:
            channel_id (str): channel_id
            title (str): title
            producer_id (str): producer_id
            description (str): description
        """
        return {
            "channel_id": channel_id,
            "producer_id": producer_id or self.test_user.identifier,
            "title": title or self.random_string(),
            "description": description or self.random_string()
        }

    def patch_json(self, title: str = None):
        return {"title": title or self.random_string()}
