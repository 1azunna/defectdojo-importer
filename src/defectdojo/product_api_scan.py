import json
from http_client import HttpClient
from models.api_scan_configuration import ApiScanConfig


class ProductApiScan:
    def __init__(self, client: HttpClient):
        self.client = client
        self.logger = self.client.logger
        self.endpoint = self.client.url + "/api/v2/product_api_scan_configurations/"

    def get(self, api_scan_config: ApiScanConfig) -> int | None:
        """Fetch an api scan configuration by product id."""
        response = self.client.request("GET", self.endpoint, params=api_scan_config.to_dict())
        try:
            api_scan_data = json.loads(response)
            count = api_scan_data["count"]
        except Exception as err:
            self.logger.error(
                f"An error occured while getting api scan configuration for product ID {api_scan_config.product}.",
                exc_info=True,
            )
            raise err
        if count < 1:
            self.logger.warning(
                f"API scan configuration not found for product ID {api_scan_config.product}.",
            )
            return None
        result = max(api_scan_data["results"], key=lambda ev: ev["id"])
        api_scan_id = result["id"]
        self.logger.info(f"API scan configuration, id: {api_scan_id}")
        return api_scan_id

    def create(self, api_scan_config: ApiScanConfig) -> int:
        """Create an api scan configuration for a product."""
        response = self.client.request("POST", self.endpoint, data=api_scan_config.to_json())
        try:
            api_scan_data = json.loads(response)
            api_scan_id = api_scan_data["id"]
        except Exception as err:
            self.logger.error(
                f"An error occured while creating api scan configuration for product ID {api_scan_config.product}.",
                exc_info=True,
            )
            raise err
        self.logger.info(f"API scan configuration created, id: {api_scan_id}")
        return api_scan_id

    def get_or_create(self, api_scan_config: ApiScanConfig) -> int:
        """Get or create an api scan configuration for a product."""
        api_scan_id = self.get(api_scan_config)
        if api_scan_id is None:
            api_scan_id = self.create(api_scan_config)
        return api_scan_id
