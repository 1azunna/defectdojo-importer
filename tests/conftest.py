import os
import pytest
from dotenv import dotenv_values


@pytest.fixture
def mock_env():
    """Patch env_config to use the test env dict as in config.py's test block."""

    test_env = {
        **os.environ,
        **dotenv_values(".env.sample"),
    }
    return test_env


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
