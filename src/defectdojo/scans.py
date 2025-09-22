from models.scan import Scan
from http_client import HttpClient


class Scans:
    def __init__(self, client: HttpClient):
        self.client = client
        self.logger = self.client.logger
        self.headers = {**(self.client.headers or {})}
        if "Content-Type" in self.headers:
            del self.headers["Content-Type"]
        self.client.headers = self.headers

    def upload(self, scan: Scan, files: list):
        """Import scan findings."""
        endpoint = self.client.url + "/api/v2/import-scan/"
        try:
            self.client.request("POST", endpoint, data=scan.to_dict(), files=files)
            self.logger.info("Scan report imported successfully")
        except Exception:
            self.logger.error("Import Failed!", exc_info=True)

    def reupload(self, scan: Scan, files: list):
        """Re-imports scan findings."""
        endpoint = self.client.url + "/api/v2/reimport-scan/"
        try:
            self.client.request("POST", endpoint, data=scan.to_dict(), files=files)
            self.logger.info("Scan report re-imported successfully")
        except Exception:
            self.logger.error("Re-import Failed!", exc_info=True)
