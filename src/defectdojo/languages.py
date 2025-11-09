from http_client import HttpClient


class Languages:

    def __init__(self, client: HttpClient):
        self.client = client
        self.logger = self.client.logger
        self.headers = {**(self.client.headers or {})}

    def upload(self, product: int, files: list):
        """Import a language and lines of code report."""
        endpoint = self.client.url + "/api/v2/import-languages/"
        if "Content-Type" in self.headers:
            del self.headers["Content-Type"]
        self.client.headers = self.headers
        try:
            self.client.request("POST", endpoint, data={"product": product}, files=files)
            self.logger.info("Language report imported successfully")
        except Exception as err:
            self.logger.error("Import Failed!", exc_info=True)
