import json
from http_client import HttpClient
from models.product import ProductType


class ProductTypes:

    def __init__(self, client: HttpClient):
        self.client = client
        self.logger = self.client.logger
        self.endpoint = self.client.url + "/api/v2/product_types/"

    def get(self, product_type: ProductType) -> int | None:
        """Fetch a product type by name."""
        response = self.client.request("GET", self.endpoint, params={"name": product_type.name})
        try:
            product_type_data = json.loads(response)
            count = product_type_data["count"]
        except Exception as err:
            self.logger.error(
                f"An error occured while getting product type for name {product_type.name}.",
                exc_info=True,
            )
            raise err
        if count < 1:
            self.logger.warning(f"Product type not found for name {product_type.name}")
            return None
        result = max(product_type_data["results"], key=lambda ev: ev["id"])
        product_type_id = result["id"]
        self.logger.info(f"Product type found, id: {product_type_id}")
        return product_type_id

    def create(self, product_type: ProductType) -> int:
        """Create a product type."""
        response = self.client.request("POST", self.endpoint, data=product_type.to_json())
        try:
            product_type_data = json.loads(response)
            product_type_id = product_type_data["id"]
        except Exception as err:
            self.logger.error(
                f"An error occured while creating product type for name {product_type.name}.",
                exc_info=True,
            )
            raise err
        self.logger.info(f"Product type created, id: {product_type_id}")
        return product_type_id

    def get_or_create(self, product_type: ProductType) -> int:
        """Get or create a product type."""
        product_type_id = self.get(product_type)
        if product_type_id is None:
            product_type_id = self.create(product_type)
        return product_type_id
