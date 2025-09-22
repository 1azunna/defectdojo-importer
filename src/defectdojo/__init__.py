from http_client import HttpClient
from .product_api_scan import ProductApiScan
from .product_types import ProductTypes
from .products import Products
from .engagements import Engagements
from .test_types import TestTypes
from .tests import Tests
from .scans import Scans
from .languages import Languages
from .tool_configurations import ToolConfigurations


class DefectDojo:
    def __init__(self, client: HttpClient, api_key: str):
        self.defectdojo_client = client
        self.defectdojo_client.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Token " + api_key,
        }

        self.product_api_scan_configuration = ProductApiScan(self.defectdojo_client)
        self.product_types = ProductTypes(self.defectdojo_client)
        self.products = Products(self.defectdojo_client)
        self.engagements = Engagements(self.defectdojo_client)
        self.test_types = TestTypes(self.defectdojo_client)
        self.tests = Tests(self.defectdojo_client)
        self.scans = Scans(self.defectdojo_client)
        self.languages = Languages(self.defectdojo_client)
        self.tool_configurations = ToolConfigurations(self.defectdojo_client)
