import json
import pytest
from unittest.mock import Mock, patch
from http_client import HttpClient
from integrations.dtrack import Dtrack
from models.dtrack import Project, ProjectProperty
from models.config import Config


@pytest.fixture
def mock_http_client():
    client = Mock(spec=HttpClient)
    client.url = "https://dtrack.example.com"
    client.logger = Mock()
    client.headers = {}
    return client


@pytest.fixture
def dtrack_client(mock_http_client):
    return Dtrack(mock_http_client, "test-api-key")


@pytest.fixture
def sample_config():
    return Config(
        api_url="https://defectdojo.example.com",
        api_key="dd-api-key",
        product_name="Test Product",
        product_type_name="Test Product Type",
    )


@pytest.fixture
def sample_project():
    return Project(name="test-project", version="1.0.0")


@pytest.fixture
def sample_project_property():
    return ProjectProperty(uuid="test-uuid-123", engagement=456, reimport=True, reactivate=True)


class TestDtrack:
    """Test cases for the Dtrack class."""

    def test_init(self, mock_http_client):
        """Test Dtrack initialization."""
        api_key = "test-api-key"
        dtrack = Dtrack(mock_http_client, api_key)

        assert dtrack.client == mock_http_client
        assert dtrack.logger == mock_http_client.logger
        expected_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Api-Key": api_key,
        }
        assert mock_http_client.headers == expected_headers

    def test_get_integration_enabled(self, dtrack_client, mock_http_client):
        """Test get_integration when integration is enabled."""
        mock_response = json.dumps(
            [
                {
                    "groupName": "integrations",
                    "propertyName": "defectdojo.enabled",
                    "propertyValue": "true",
                }
            ]
        )
        mock_http_client.request.return_value = mock_response

        result = dtrack_client.get_integration()

        assert result is True
        mock_http_client.request.assert_called_once_with(
            "GET", "https://dtrack.example.com/api/v1/configProperty"
        )
        mock_http_client.logger.info.assert_called_with("Dependency Track integration is enabled.")

    def test_get_integration_disabled(self, dtrack_client, mock_http_client):
        """Test get_integration when integration is disabled."""
        mock_response = json.dumps(
            [
                {
                    "groupName": "integrations",
                    "propertyName": "defectdojo.enabled",
                    "propertyValue": "false",
                }
            ]
        )
        mock_http_client.request.return_value = mock_response

        result = dtrack_client.get_integration()

        assert result is False
        mock_http_client.logger.warning.assert_called_with(
            "Dependency Track integration is not enabled."
        )

    def test_get_integration_not_found(self, dtrack_client, mock_http_client):
        """Test get_integration when defectdojo.enabled property is not found."""
        mock_response = json.dumps(
            [{"groupName": "other", "propertyName": "other.property", "propertyValue": "value"}]
        )
        mock_http_client.request.return_value = mock_response

        result = dtrack_client.get_integration()

        assert result is False
        mock_http_client.logger.warning.assert_called_with(
            "Dependency Track integration is not enabled."
        )

    def test_get_integration_json_error(self, dtrack_client, mock_http_client):
        """Test get_integration when JSON parsing fails."""
        mock_http_client.request.return_value = "invalid json"

        with pytest.raises(Exception):
            dtrack_client.get_integration()

        mock_http_client.logger.error.assert_called_with(
            "An error occured while checking the integration status."
        )

    def test_update_integration_success(self, dtrack_client, mock_http_client, sample_config):
        """Test update_integration successful update."""
        mock_http_client.request.return_value = "{}"

        result = dtrack_client.update_integration(sample_config)

        assert result is True
        mock_http_client.request.assert_called_once()
        args, kwargs = mock_http_client.request.call_args
        assert args[0] == "POST"
        assert args[1] == "https://dtrack.example.com/api/v1/configProperty/aggregate"

        # Verify payload
        payload = json.loads(kwargs["data"])
        expected_payload = [
            {
                "groupName": "integrations",
                "propertyName": "defectdojo.apiKey",
                "propertyValue": sample_config.api_key,
                "propertyType": "STRING",
            },
            {
                "groupName": "integrations",
                "propertyName": "defectdojo.enabled",
                "propertyValue": "true",
                "propertyType": "BOOLEAN",
            },
            {
                "groupName": "integrations",
                "propertyName": "defectdojo.reimport.enabled",
                "propertyValue": "true",
                "propertyType": "BOOLEAN",
            },
            {
                "groupName": "integrations",
                "propertyName": "defectdojo.url",
                "propertyValue": sample_config.api_url,
                "propertyType": "URL",
            },
        ]
        assert payload == expected_payload
        mock_http_client.logger.info.assert_called_with(
            "Dependency Track integration has been enabled."
        )

    def test_update_integration_error(self, dtrack_client, mock_http_client, sample_config):
        """Test update_integration when request fails."""
        mock_http_client.request.side_effect = Exception("API Error")

        with pytest.raises(Exception):
            dtrack_client.update_integration(sample_config)

        mock_http_client.logger.error.assert_called_with(
            "An error occured while updating the integration config. Check API key permissions or enable the integration manually"
        )

    def test_get_project_uuid_success(self, dtrack_client, mock_http_client, sample_project):
        """Test get_project_uuid successful retrieval."""
        mock_response = json.dumps({"uuid": "test-uuid-123"})
        mock_http_client.request.return_value = mock_response

        result = dtrack_client.get_project_uuid(sample_project)

        assert result == "test-uuid-123"
        mock_http_client.request.assert_called_once_with(
            "GET",
            "https://dtrack.example.com/api/v1/project/lookup",
            params=sample_project.to_dict(),
        )
        mock_http_client.logger.info.assert_called_with(
            "Dependency Track project found, uuid: %s", "test-uuid-123"
        )

    def test_get_project_uuid_error(self, dtrack_client, mock_http_client, sample_project):
        """Test get_project_uuid when request fails."""
        mock_http_client.request.return_value = "invalid json"

        with pytest.raises(Exception):
            dtrack_client.get_project_uuid(sample_project)

        mock_http_client.logger.error.assert_called_with(
            "An error occured while getting the dependency track project %s.", sample_project.name
        )

    def test_get_project_properties_success(
        self, dtrack_client, mock_http_client, sample_project_property
    ):
        """Test get_project_properties successful retrieval."""
        mock_response = json.dumps(
            [{"propertyName": "defectdojo.engagementId", "propertyValue": "123"}]
        )
        mock_http_client.request.return_value = mock_response

        result = dtrack_client.get_project_properties(sample_project_property)

        expected_result = [{"propertyName": "defectdojo.engagementId", "propertyValue": "123"}]
        assert result == expected_result
        mock_http_client.request.assert_called_once_with(
            "GET",
            f"https://dtrack.example.com/api/v1/project/{sample_project_property.uuid}/property",
        )

    def test_get_project_properties_error(
        self, dtrack_client, mock_http_client, sample_project_property
    ):
        """Test get_project_properties when request fails."""
        mock_http_client.request.return_value = "invalid json"

        with pytest.raises(Exception):
            dtrack_client.get_project_properties(sample_project_property)

        mock_http_client.logger.error.assert_called_with(
            "An error occured while getting the dependency track properties for project %s.",
            sample_project_property.uuid,
        )

    def test_update_project_properties_new_properties(
        self, dtrack_client, mock_http_client, sample_project_property
    ):
        """Test update_project_properties when creating new properties."""
        # Mock existing properties (empty)
        mock_http_client.request.side_effect = [
            json.dumps([]),  # get_project_properties response
            "{}",  # PUT response for engagementId
            "{}",  # PUT response for reimport
            "{}",  # PUT response for doNotReactivate
        ]

        result = dtrack_client.update_project_properties(sample_project_property)

        # Verify 4 calls: 1 GET + 3 PUT
        assert mock_http_client.request.call_count == 4

        # Verify GET call for existing properties
        first_call = mock_http_client.request.call_args_list[0]
        assert first_call[0][0] == "GET"

        # Verify PUT calls for new properties
        for i in range(1, 4):
            call = mock_http_client.request.call_args_list[i]
            assert call[0][0] == "PUT"
            assert call[1]["data"] is not None

    def test_update_project_properties_existing_properties(
        self, dtrack_client, mock_http_client, sample_project_property
    ):
        """Test update_project_properties when updating existing properties."""
        # Mock existing properties
        existing_properties = [
            {"propertyName": "defectdojo.engagementId", "propertyValue": "old-value"},
            {"propertyName": "defectdojo.reimport", "propertyValue": "false"},
            {"propertyName": "defectdojo.doNotReactivate", "propertyValue": "true"},
        ]
        mock_http_client.request.side_effect = [
            json.dumps(existing_properties),  # get_project_properties response
            "{}",  # POST response for engagementId
            "{}",  # POST response for reimport
            "{}",  # POST response for doNotReactivate
        ]

        result = dtrack_client.update_project_properties(sample_project_property)

        # Verify 4 calls: 1 GET + 3 POST
        assert mock_http_client.request.call_count == 4

        # Verify GET call for existing properties
        first_call = mock_http_client.request.call_args_list[0]
        assert first_call[0][0] == "GET"

        # Verify POST calls for updating existing properties
        for i in range(1, 4):
            call = mock_http_client.request.call_args_list[i]
            assert call[0][0] == "POST"
            assert call[1]["data"] is not None

    def test_update_project_properties_reactivate_false(self, dtrack_client, mock_http_client):
        """Test update_project_properties when reactivate is False."""
        project_property = ProjectProperty(
            uuid="test-uuid",
            engagement=456,
            reimport=True,
            reactivate=False,  # This should set doNotReactivate to True
        )

        mock_http_client.request.side_effect = [
            json.dumps([]),  # get_project_properties response
            "{}",  # PUT responses
            "{}",
            "{}",
        ]

        dtrack_client.update_project_properties(project_property)

        # Check the doNotReactivate payload
        do_not_reactivate_call = None
        for call in mock_http_client.request.call_args_list[1:]:
            payload = json.loads(call[1]["data"])
            if payload["propertyName"] == "defectdojo.doNotReactivate":
                do_not_reactivate_call = payload
                break

        assert do_not_reactivate_call is not None
        assert do_not_reactivate_call["propertyValue"] == "true"
