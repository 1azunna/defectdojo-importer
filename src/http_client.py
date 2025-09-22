from logging import Logger
import requests
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

# Disable SSL Warnings
disable_warnings(InsecureRequestWarning)


class HttpClient:
    """This class handles http requests"""

    def __init__(
        self,
        url: str,
        headers: dict | None = None,
        ssl_verify: bool = True,
        logger: Logger = Logger(__name__),
    ):
        self.url = url
        self.headers = headers
        self.ssl_verify = ssl_verify
        self.logger = logger

    def request(self, method: str, url: str, **kwargs) -> str:
        """Handle HTTP requests for different methods."""
        headers = self.headers
        if "headers" in kwargs:
            headers = {**(self.headers or {}), **(kwargs.get("headers") or {})}
            del kwargs["headers"]

        # Set default timeout based on method
        timeout = 300 if method.upper() == "POST" else 120
        if "timeout" not in kwargs:
            kwargs["timeout"] = timeout

        try:
            response = requests.request(
                method, url, headers=headers, verify=self.ssl_verify, **kwargs
            )
            response.raise_for_status()
        except HTTPError as http_err:
            raise http_err
        except Exception as err:
            self.logger.exception("Could not make request.")
            raise err
        self.logger.debug(response.text)
        return response.text
