import pytest
from unittest.mock import Mock, patch
from argparse import Namespace
from importer.validations import validate_config
from models.config import Config
from models.common import SeverityLevel, ReimportConditions
from models.exceptions import ConfigurationError


class TestValidateConfig:
    """Test cases for the validate_config function."""

    @pytest.fixture
    def base_args(self):
        """Base arguments for testing."""
        args = Namespace()
        args.sub_command = None
        args.integration_type = None
        args.file = "test.xml"
        return args

    @pytest.fixture
    def base_env_config(self):
        """Base environment configuration."""
        return {
            "api_url": "https://defectdojo.example.com",
            "api_key": "test-api-key",
            "product_name": "Test Product",
            "product_type_name": "Test Product Type",
            "test_type_name": "Test Type",
            "engagement_name": "CI/CD Engagement",
            "debug": True,
        }

    @patch("importer.validations.env_config")
    @patch("importer.validations.get_build_id")
    @patch("importer.validations.get_commit_hash")
    @patch("importer.validations.get_branch_tag")
    @patch("importer.validations.get_scm_uri")
    def test_validate_config_success(
        self,
        mock_scm_uri,
        mock_branch_tag,
        mock_commit_hash,
        mock_build_id,
        mock_env_config,
        base_args,
        base_env_config,
    ):
        """Test successful configuration validation."""
        mock_env_config.return_value = base_env_config
        mock_build_id.return_value = "123"
        mock_commit_hash.return_value = "abc123"
        mock_branch_tag.return_value = "main"
        mock_scm_uri.return_value = "https://github.com/test/repo"

        result = validate_config(base_args)

        assert isinstance(result, Config)
        assert result.api_url == "https://defectdojo.example.com"
        assert result.api_key == "test-api-key"
        assert result.product_name == "Test Product"
        assert result.product_type_name == "Test Product Type"
        assert result.test_type_name == "Test Type"
        assert result.test_name == "Test Type"  # Should default to test_type_name

    @patch("importer.validations.env_config")
    def test_validate_config_missing_api_url(self, mock_env_config, base_args, base_env_config):
        """Test validation fails when API URL is missing."""
        base_env_config.pop("api_url")
        mock_env_config.return_value = base_env_config

        with pytest.raises(ConfigurationError, match="DefectDojo API URL is required"):
            validate_config(base_args)

    @patch("importer.validations.env_config")
    def test_validate_config_missing_api_key(self, mock_env_config, base_args, base_env_config):
        """Test validation fails when API key is missing."""
        base_env_config.pop("api_key")
        mock_env_config.return_value = base_env_config

        with pytest.raises(ConfigurationError, match="DefectDojo API Key is required"):
            validate_config(base_args)

    @patch("importer.validations.env_config")
    def test_validate_config_missing_product_name(
        self, mock_env_config, base_args, base_env_config
    ):
        """Test validation fails when product name is missing."""
        base_env_config.pop("product_name")
        mock_env_config.return_value = base_env_config

        with pytest.raises(ConfigurationError, match="Product name is required"):
            validate_config(base_args)

    @patch("importer.validations.env_config")
    def test_validate_config_missing_product_type_name(
        self, mock_env_config, base_args, base_env_config
    ):
        """Test validation fails when product type name is missing."""
        base_env_config.pop("product_type_name")
        mock_env_config.return_value = base_env_config

        with pytest.raises(ConfigurationError, match="Product type name is required"):
            validate_config(base_args)

    @patch("importer.validations.env_config")
    def test_validate_config_missing_test_type_name(
        self, mock_env_config, base_args, base_env_config
    ):
        """Test validation fails when test type name is missing."""
        base_env_config.pop("test_type_name")
        mock_env_config.return_value = base_env_config

        with pytest.raises(ConfigurationError, match="Test type name is required"):
            validate_config(base_args)

    @patch("importer.validations.env_config")
    def test_validate_config_missing_file(self, mock_env_config, base_env_config):
        """Test validation fails when file is missing for regular import."""
        args = Namespace()
        args.sub_command = None
        args.integration_type = None
        args.file = None
        args.tool_configuration_name = None

        mock_env_config.return_value = base_env_config

        with pytest.raises(ConfigurationError, match="File is required for import"):
            validate_config(args)

    @patch("importer.validations.env_config")
    def test_validate_config_dtrack_integration_success(
        self, mock_env_config, base_env_config, caplog
    ):
        """Test successful dtrack integration validation."""
        args = Namespace()
        args.sub_command = "integration"
        args.integration_type = "dtrack"
        args.file = None

        dtrack_config = {
            **base_env_config,
            "dtrack_api_url": "https://dtrack.example.com",
            "dtrack_api_key": "dtrack-key",
            "dtrack_project_name": "Test Project",
            "dtrack_project_version": "1.0.0",
        }
        mock_env_config.return_value = dtrack_config

        result = validate_config(args)

        assert result.dtrack_api_url == "https://dtrack.example.com"
        assert result.dtrack_api_key == "dtrack-key"
        assert result.dtrack_project_name == "Test Project"
        assert result.dtrack_project_version == "1.0.0"

    @patch("importer.validations.env_config")
    def test_validate_config_dtrack_missing_api_url(self, mock_env_config, base_env_config):
        """Test dtrack integration fails when API URL is missing."""
        args = Namespace()
        args.sub_command = "integration"
        args.integration_type = "dtrack"
        args.file = None

        mock_env_config.return_value = base_env_config

        with pytest.raises(ConfigurationError, match="Dependency Track API URL is required"):
            validate_config(args)

    @patch("importer.validations.env_config")
    def test_validate_config_dtrack_missing_api_key(self, mock_env_config, base_env_config):
        """Test dtrack integration fails when API key is missing."""
        args = Namespace()
        args.sub_command = "integration"
        args.integration_type = "dtrack"
        args.file = None

        dtrack_config = {
            **base_env_config,
            "dtrack_api_url": "https://dtrack.example.com",
        }
        mock_env_config.return_value = dtrack_config

        with pytest.raises(ConfigurationError, match="Dependency Track API Key is required"):
            validate_config(args)

    @patch("importer.validations.env_config")
    def test_validate_config_dtrack_default_project_name(
        self, mock_env_config, base_env_config, caplog
    ):
        """Test dtrack integration uses product name as default project name."""
        args = Namespace()
        args.sub_command = "integration"
        args.integration_type = "dtrack"
        args.file = None

        dtrack_config = {
            **base_env_config,
            "dtrack_api_url": "https://dtrack.example.com",
            "dtrack_api_key": "dtrack-key",
        }
        mock_env_config.return_value = dtrack_config

        result = validate_config(args)

        assert result.dtrack_project_name == "Test Product"
        assert (
            "If --dtrack-project-name or DD_DTRACK_PROJECT_NAME is not explicitly set"
            in caplog.text
        )

    @patch("importer.validations.env_config")
    @patch("importer.validations.get_branch_tag")
    @patch("importer.validations.get_build_id")
    def test_validate_config_dtrack_default_project_version(
        self, mock_build_id, mock_branch_tag, mock_env_config, base_env_config, caplog
    ):
        """Test dtrack integration uses branch_tag or build_id as default project version."""
        args = Namespace()
        args.sub_command = "integration"
        args.integration_type = "dtrack"
        args.file = None

        dtrack_config = {
            **base_env_config,
            "dtrack_api_url": "https://dtrack.example.com",
            "dtrack_api_key": "dtrack-key",
            "dtrack_project_name": "Test Project",
        }
        mock_env_config.return_value = dtrack_config
        mock_branch_tag.return_value = "main"
        mock_build_id.return_value = "123"

        result = validate_config(args)

        assert result.dtrack_project_version == "main"  # branch_tag takes precedence
        assert (
            "If --dtrack-project-version or DD_DTRACK_PROJECT_VERSION is not explicitly set"
            in caplog.text
        )

    @patch("importer.validations.env_config")
    def test_validate_config_tool_configuration_success(self, mock_env_config, base_env_config):
        """Test successful tool configuration validation."""
        args = Namespace()
        args.sub_command = None
        args.integration_type = None
        args.file = None

        tool_config = {
            **base_env_config,
            "tool_configuration_name": "SonarQube",
            "tool_configuration_params": "project-key",
        }
        mock_env_config.return_value = tool_config

        result = validate_config(args)

        assert result.tool_configuration_name == "SonarQube"
        assert result.tool_configuration_params == "project-key"

    @patch("importer.validations.env_config")
    def test_validate_config_tool_configuration_missing_params(
        self, mock_env_config, base_env_config
    ):
        """Test tool configuration fails when parameters are missing."""
        args = Namespace()
        args.sub_command = None
        args.integration_type = None
        args.file = None

        tool_config = {
            **base_env_config,
            "tool_configuration_name": "SonarQube",
        }
        mock_env_config.return_value = tool_config

        with pytest.raises(ConfigurationError, match="Tool configuration parameters are required"):
            validate_config(args)

    @patch("importer.validations.env_config")
    def test_validate_config_severity_levels(self, mock_env_config, base_args, base_env_config):
        """Test different severity levels are handled correctly."""
        severity_config = {
            **base_env_config,
            "minimum_severity": "High",
        }
        mock_env_config.return_value = severity_config

        result = validate_config(base_args)

        assert result.minimum_severity == SeverityLevel.HIGH

    @patch("importer.validations.env_config")
    def test_validate_config_reimport_conditions(self, mock_env_config, base_args, base_env_config):
        """Test different reimport conditions are handled correctly."""
        reimport_config = {
            **base_env_config,
            "reimport_condition": "branch",
        }
        mock_env_config.return_value = reimport_config

        result = validate_config(base_args)

        assert result.reimport_condition == ReimportConditions.BRANCH

    @patch("importer.validations.env_config")
    def test_validate_config_boolean_fields(self, mock_env_config, base_args, base_env_config):
        """Test boolean fields are converted correctly."""
        bool_config = {
            **base_env_config,
            "critical_product": True,
            "static_tool": True,
            "dynamic_tool": False,
            "push_to_jira": True,
            "reimport": False,
            "debug": True,
            "dtrack_reimport": False,
            "dtrack_reactivate": True,
        }
        mock_env_config.return_value = bool_config

        result = validate_config(base_args)

        assert result.critical_product is True
        assert result.static_tool is True
        assert result.dynamic_tool is False
        assert result.push_to_jira is True
        assert result.reimport is False
        assert result.debug is True
        assert result.dtrack_reimport is False
        assert result.dtrack_reactivate is True

    @patch("importer.validations.env_config")
    def test_validate_config_test_name_fallback(self, mock_env_config, base_args, base_env_config):
        """Test that test_name falls back to test_type_name when not provided."""
        mock_env_config.return_value = base_env_config

        result = validate_config(base_args)

        # test_name should default to test_type_name
        assert result.test_name == result.test_type_name

    @patch("importer.validations.env_config")
    def test_validate_config_custom_test_name(self, mock_env_config, base_args, base_env_config):
        """Test that custom test_name is preserved."""
        custom_config = {
            **base_env_config,
            "test_name": "Custom Test Name",
        }
        mock_env_config.return_value = custom_config

        result = validate_config(base_args)

        assert result.test_name == "Custom Test Name"
        assert result.test_name != result.test_type_name

    @patch("importer.validations.logger")
    @patch("importer.validations.env_config")
    def test_validate_config_logs_final_config(
        self, mock_env_config, mock_logger, base_args, base_env_config
    ):
        """Test that the final configuration is logged."""
        mock_env_config.return_value = base_env_config

        result = validate_config(base_args)

        # Verify that logger.info was called with the config JSON
        mock_logger.info.assert_called_once()
        # The call should be with result.to_json(), but we can't easily test the exact value
        assert mock_logger.info.call_count == 1
