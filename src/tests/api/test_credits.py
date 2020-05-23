from uuid import UUID

from tests.api.test_channels import ChannelsTest
from tests.api.test_productions import ProductionsTest
from tests.base_test import BaseTestCase


class CreditsTest(BaseTestCase):
    path = "credits"

    def test_all(self):
        self.get_list()

        person = PeopleTest(methodName="post")
        person.setUp()

        person_response = person.post(json=person.json())
        person_id = person_response.json.get("identifier")

        channel = ChannelsTest(methodName="post")
        channel.setUp()

        channel_response = channel.post(json=channel.json())
        channel_id = channel_response.json.get("identifier")

        production = ProductionsTest(methodName="post")
        production.setUp()

        prod_response = production.post(json=production.json(channel_id=channel_id))
        production_id = prod_response.json.get("identifier")

        post_response = self.post(json=self.json(production_id=production_id, person_id=person_id))
        identifier = post_response.json.get("identifier")

        self.patch(identifier=identifier, json=self.patch_json())
        self.put(identifier=identifier, json=self.json(production_id=production_id))
        self.get(identifier=identifier)
        self.delete(identifier=identifier)
        production.delete(identifier=production_id)
        channel.delete(identifier=channel_id)

    def json(self, production_id: UUID, person_id: UUID = None, job: str = None):
        return {
            "person_id": person_id,
            "production_id": production_id,
            "job": job or self.random_string()
        }

    def patch_json(self, job: str = None):
        return {
            "job": job or self.random_string()
        }
