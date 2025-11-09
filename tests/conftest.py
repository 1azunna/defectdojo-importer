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


@pytest.fixture
def mock_config(mocker):
    config = mocker.Mock()
    config.api_url = "https://defectdojo.example.com"
    config.api_key = "dd-api-key"
    config.product_name = "Test Product"
    config.product_type_name = "Test Product Type"
    return config
