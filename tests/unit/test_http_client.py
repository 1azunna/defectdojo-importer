import responses
import pytest
from unittest.mock import MagicMock
from requests.exceptions import HTTPError
from src.http_client import HttpClient

default_headers = {
    "Content-Type": "application/text",
    "Accept": "application/text",
}
client = HttpClient("http://localhost", default_headers, False, MagicMock())
url = client.url


class TestHttpClient:

    @responses.activate
    def test_http_client_requests(self):
        responses.add(responses.GET, url=url, status=200)
        responses.add(responses.POST, url=url, status=200)
        responses.add(responses.PUT, url=url, status=200)
        responses.add(responses.PATCH, url=url, status=200)

        client.request("POST", url)
        client.request("GET", url)
        client.request("PATCH", url)
        client.request("PUT", url)

    @responses.activate
    def test_http_client_with_headers(self):
        responses.add(responses.GET, url=url, status=200)
        responses.add(responses.POST, url=url, status=200)
        responses.add(responses.PUT, url=url, status=200)
        responses.add(responses.PATCH, url=url, status=200)

        headers = {
            "X-API-Key": "my-api-key",
        }

        client.request("POST", url, headers=headers)

        # Assert that the X-API-Key header is present in the request
        for call in responses.calls:
            assert call.request.headers.get("X-API-Key") == "my-api-key"

    @responses.activate
    def test_http_client_http_error(self):
        responses.add(responses.GET, url=url, status=404)
        responses.add(responses.POST, url=url, status=404)
        responses.add(responses.PUT, url=url, status=404)
        responses.add(responses.PATCH, url=url, status=404)

        with pytest.raises(HTTPError):
            client.request("POST", url)

        with pytest.raises(HTTPError):
            client.request("GET", url)

        with pytest.raises(HTTPError):
            client.request("PATCH", url)

        with pytest.raises(HTTPError):
            client.request("PUT", url)

    def test_http_client_exception(self):
        with pytest.raises(Exception):
            client.request("POST", url)

        with pytest.raises(Exception):
            client.request("GET", url)

        with pytest.raises(Exception):
            client.request("PATCH", url)

        with pytest.raises(Exception):
            client.request("PUT", url)
