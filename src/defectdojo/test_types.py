"""Test types are required when importing findings."""

import json
from models.tests import TestType
from http_client import HttpClient


class TestTypes:
    def __init__(self, client: HttpClient):
        self.client = client
        self.logger = self.client.logger
        self.endpoint = self.client.url + "/api/v2/test_types/"

    def get(self, test_type: TestType) -> int | None:
        """Get a test type."""

        response = self.client.request("GET", self.endpoint, params={"name": test_type.name})
        try:
            test_type_data = json.loads(response)
            count = test_type_data["count"]
        except Exception as err:
            self.logger.error(
                f"An error occured while getting test type {test_type.name}.", exc_info=True
            )
            raise err
        if count < 1:
            self.logger.warning(f"Test type {test_type.name} not found")
            return None
        result = max(test_type_data["results"], key=lambda ev: ev["id"])
        test_type_id = result["id"]
        self.logger.info(f"Test type found, id: {test_type_id}")
        return test_type_id

    def create(self, test_type: TestType) -> int:
        """Create a test type."""
        response = self.client.request("POST", self.endpoint, data=test_type.to_json())
        try:
            test_type_data = json.loads(response)
            test_type_id = test_type_data["id"]
        except Exception as err:
            self.logger.error(
                f"An error occured while creating test type {test_type.name}.", exc_info=True
            )
            raise err
        self.logger.info(f"Test type successfully created, id: {test_type_id}")
        return test_type_id

    def get_or_create(self, test_type: TestType) -> int:
        """Get or create a test type."""
        test_type_id = self.get(test_type)
        if test_type_id is None:
            test_type_id = self.create(test_type)
        return test_type_id
