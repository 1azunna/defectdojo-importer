import pytest


@pytest.fixture
def mock_http_client(mocker):
    """Create a mock HttpClient for testing using pytest-mock."""
    # Create a mock instance directly instead of patching the class
    client = mocker.Mock()
    client.url = "https://example.com"
    client.logger = mocker.Mock()
    client.headers = {}
    return client
