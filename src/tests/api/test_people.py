from tests.base_test import BaseTestCase


class PeopleTest(BaseTestCase):
    path = "people"

    def test_all(self):
        self.get_list()
        response = self.post(json=self.json())
        identifier = response.json.get("identifier")
        self.patch(identifier=identifier, json=self.patch_json())
        self.get(identifier=identifier)
        self.put(identifier=identifier, json=self.json())
        self.delete(identifier=identifier)

    def json(self, phone: str = None, email: str = None, name: str = None):
        return {
            "phone": phone or "+45 12 12 12 12",
            "email": email or f"{self.random_string()}@creditoro.nymann.dev",
            "name": name or self.random_string()
        }

    def patch_json(self, name: str = None):
        return {
            "name": name or self.random_string()
        }
