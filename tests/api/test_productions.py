from http import HTTPStatus

from tests.base_test import BaseTestCase


class ProductionsTest(BaseTestCase):
    path = "/productions/"

    def test_get(self):
        with self.client:
            response = self.client.get("/productions/", headers={"Authorization": self.token}, data={"q": "test"})
            self.assertTrue(response.status_code == HTTPStatus.OK)

    def test_post_patch_delete(self):
        with self.client:
            channel_id = self.create_channel()
            production_id = self.post_production(channel_id=channel_id)
            self.assertTrue(self.patch_production(production_id=production_id))
            self.assertTrue(self.put_production(production_id=production_id, channel_id=channel_id))
            self.assertTrue(self.delete_production(production_id=production_id))
            self.assertTrue(self.delete_channel(channel_id=channel_id))

    def create_channel(self):
        channel_response = self.post(path="/channels/", json={"name": "test-channel"})
        channel_id = channel_response.json["identifier"]
        self.assertTrue(channel_response.status_code == HTTPStatus.CREATED)
        return channel_id

    def delete_channel(self, channel_id):
        delete_response = self.delete(f"/channels/{channel_id}")
        return delete_response.status_code == HTTPStatus.NO_CONTENT

    def post_production(self, channel_id):
        response = self.post(path=self.path,
                             json={"title": "test-production",
                                   "producer_id": str(self.test_user.identifier),
                                   "channel_id": str(channel_id)})
        self.assertTrue(response.status_code == HTTPStatus.CREATED)
        return response.json["identifier"]

    def patch_production(self, production_id):
        response = self.patch(path=f"{self.path}{production_id}", json={"title": "test-production-patched"})
        return response.status_code == HTTPStatus.OK

    def put_production(self, production_id, channel_id):
        response = self.put(path=f"{self.path}{production_id}", json={"title": "test-production-put",
                                                                      "producer_id": str(self.test_user.identifier),
                                                                      "channel_id": str(channel_id)})
        return response.status_code == HTTPStatus.OK

    def delete_production(self, production_id) -> bool:
        delete_response = self.delete(f"{self.path}{production_id}")
        return delete_response.status_code == HTTPStatus.NO_CONTENT
