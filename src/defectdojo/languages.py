from http_client import HttpClient


class Languages:
    def __init__(self, client: HttpClient):
        self.client = client
        self.logger = self.client.logger
        self.headers = {**(self.client.headers or {})}

    def upload(self, product: int, files: list):
        """Import a language and lines of code report."""
        endpoint = self.client.url + "/api/v2/import-languages/"
        headers = self.headers.copy()
        if "Content-Type" in headers:
            headers["Content-Type"] = None
        try:
            self.client.request(
                "POST",
                endpoint,
                data={"product": product},
                files=files,
                headers=headers,
            )
            self.logger.info("Language report imported successfully")
        except Exception:
            self.logger.error("Import Failed!", exc_info=True)
