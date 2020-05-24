"""
Test channels.
"""
from tests.base_test import BaseTestCase


class ChannelsTest(BaseTestCase):
    """ChannelsTest.
    """

    path = "channels"

    def test_all(self):
        """test_all.
        """
        with self.app.test_request_context():
            self.get_list()

            response = self.post(json=self.json())
            identifier = response.json.get("identifier")
            self.patch(identifier=identifier, json=self.patch_json())
            self.get(identifier=identifier)
            self.delete(identifier=identifier)

    def json(self, name: str = None, url: str = None):
        """json.

        Args:
            name (str): name
            url (str): url
        """
        return {
            "name": name or self.random_string(),
            "icon_url": url or f"https://{self.random_string()}.png"
        }

    def patch_json(self, name: str = None):
        """patch_json.

        Args:
            name (str): name
        """
        return self.json(name=name)
