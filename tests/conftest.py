import pytest


@pytest.fixture
def mock_http_client(mocker):
    client = mocker.patch("http_client.HttpClient")
    return client.return_value
