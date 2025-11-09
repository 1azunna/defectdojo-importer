import json
from models.tests import Test
from http_client import HttpClient


class Tests:
    def __init__(self, client: HttpClient):
        self.client = client
        self.logger = self.client.logger
        self.endpoint = self.client.url + "/api/v2/tests/"

    def get(self, test: Test, metadata: dict = {}) -> int | None:
        """Get a test."""

        response = self.client.request(
            "GET",
            self.endpoint,
            params={
                "title": test.title,
                "engagement": test.engagement,
                "test_type": test.test_type,
                "tags__and": ",".join(test.tags),
                **metadata,
            },
        )
        try:
            test_data = json.loads(response)
            count = test_data["count"]
        except Exception as err:
            self.logger.error(f"An error occured while getting test {test.title}.", exc_info=True)
            raise err
        if count < 1:
            self.logger.warning(f"Test {test.title} not found. Will be created")
            return None
        result = max(test_data["results"], key=lambda ev: ev["id"])
        test_id = result["id"]
        self.logger.info("Test found, id: %s", test_id)
        return test_id
