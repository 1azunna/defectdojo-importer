import json
from http_client import HttpClient
from models.product import Product


class Products:

    def __init__(self, client: HttpClient):
        self.client = client
        self.logger = self.client.logger
        self.endpoint = self.client.url + "/api/v2/products/"

    def get(self, product: Product) -> int | None:
        """Fetch a product by name."""
        response = self.client.request("GET", self.endpoint, params={"name": product.name})
        try:
            product_data = json.loads(response)
            count = product_data["count"]
        except Exception as err:
            self.logger.error(
                f"An error occured while getting product for name {product.name}.", exc_info=True
            )
            raise err
        if count < 1:
            self.logger.warning(f"Product not found for name {product.name}.")
            return None
        result = max(product_data["results"], key=lambda ev: ev["id"])
        product_id = result["id"]
        self.logger.info("Product found, id: %s", product_id)
        return product_id

    def create(self, product: Product) -> int:
        """Create a product."""
        response = self.client.request("POST", self.endpoint, data=product.to_json())
        try:
            product_data = json.loads(response)
            product_id = product_data["id"]
        except Exception:
            self.logger.error(
                f"An error occured while creating product for name {product.name}.", exc_info=True
            )
        self.logger.info(f"Product created, id: {product_id}")
        return product_id

    def get_or_create(self, product: Product) -> int:
        """Get or create a product."""
        product_id = self.get(product)
        if product_id is None:
            product_id = self.create(product)
        return product_id
