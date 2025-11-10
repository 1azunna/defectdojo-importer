from http_client import HttpClient
from models.config import Config
from models.product import Product, ProductType
from models.engagement import Engagement
from models.tests import Test, TestType
from models.scan import Scan
from models.dtrack import Project, ProjectProperty
from models.common import ReimportConditions
from models.api_scan_configuration import ApiScanConfig
from models.exceptions import InvalidScanType, ConfigurationError
from defectdojo import DefectDojo
from integrations.dtrack import Dtrack
from common import utils


def setup_product_engagement(defectdojo: DefectDojo, config: Config) -> dict:
    """Setup and validate engagement, product, test type, and API scan configuration."""

    # Get Product type and Product
    product_type = ProductType(
        config.product_type_name, critical_product=config.critical_product
    )
    product_type_id = defectdojo.product_types.get_or_create(product_type)
    product = Product(config.product_name, product_type_id)
    product_id = defectdojo.products.get_or_create(product)

    # Get Engagement
    engagement = Engagement(
        str(config.engagement_name),
        product_id,
        build_id=config.build_id,
        commit_hash=config.commit_hash,
        branch_tag=config.branch_tag,
    )
    engagement_id = defectdojo.engagements.get_or_create(engagement)

    return {
        "product_id": product_id,
        "product_type_id": product_type_id,
        "engagement_id": engagement_id,
    }


def setup_test(defectdojo: DefectDojo, config: Config, engagement_config: dict) -> dict:
    """Setup and validate test type and test."""

    test_type = TestType(
        str(config.test_type_name),
        static_tool=config.static_tool,
        dynamic_tool=config.dynamic_tool,
    )
    valid_test_type = defectdojo.test_types.get(test_type)

    if not valid_test_type:
        raise InvalidScanType(f"Test type '{config.test_type_name}' is not valid.")

    # Get Test
    test = Test(
        str(config.test_name),
        engagement_config["engagement_id"],
        valid_test_type,
        build_id=config.build_id,
        commit_hash=config.commit_hash,
        branch_tag=config.branch_tag,
    )
    test_metadata = {}
    if config.reimport:
        match config.reimport_condition:
            case ReimportConditions.PULL_REQUEST:
                pull_request_id = utils.get_pull_request_id()
                if pull_request_id:
                    test.tags.append(f"pull_request:{pull_request_id}")
            case ReimportConditions.BRANCH:
                test_metadata["branch_tag"] = config.branch_tag
            case ReimportConditions.COMMIT:
                test_metadata["commit_hash"] = config.commit_hash
            case ReimportConditions.BUILD:
                test_metadata["build_id"] = config.build_id
            case _:
                pass

    test_id = defectdojo.tests.get(test, test_metadata)

    return {
        "test_id": test_id,
        "test_type_id": valid_test_type,
    }


def import_findings(
    defectdojo: DefectDojo,
    config: Config,
    filename: str | None,
    test_config: dict,
    engagement_config: dict,
):
    """Import test findings into defectdojo API using the client."""

    files = utils.get_files(filename)
    api_scan_id = None
    if config.tool_configuration_name:
        tool_configuration = defectdojo.tool_configurations.get(
            config.tool_configuration_name
        )
        if not tool_configuration:
            raise ConfigurationError(
                f"Tool configuration '{config.tool_configuration_name}' not found."
            )
        api_scan = ApiScanConfig(
            engagement_config["product_id"],
            tool_configuration,
            service_key_1=utils.get_service_keys(
                str(config.tool_configuration_params), 0
            ),
            service_key_2=utils.get_service_keys(
                str(config.tool_configuration_params), 1
            ),
            service_key_3=utils.get_service_keys(
                str(config.tool_configuration_params), 2
            ),
        )
        api_scan_id = defectdojo.product_api_scan_configuration.get_or_create(api_scan)

    scan = Scan(
        config.test_type_name,
        config.product_name,
        str(config.test_name),
        engagement_config["engagement_id"],
        str(config.engagement_name),
        test=test_config["test_id"],
        api_scan_id=api_scan_id,
        push_to_jira=config.push_to_jira,
        build_id=config.build_id,
        commit_hash=config.commit_hash,
        branch_tag=config.branch_tag,
        source_code_management_uri=config.scm_uri,
    )

    if test_config["test_id"] is None:
        defectdojo.scans.upload(scan, files)
    else:
        defectdojo.scans.reupload(scan, files)


def integration_findings(
    client: HttpClient, config: Config, engagement_id: int, type: str
):
    """Integrate external tool findings into defectdojo API."""

    match type:
        case "dtrack":
            dtrack = Dtrack(client, str(config.dtrack_api_key))
            integration_is_enabled = dtrack.get_integration()
            if not integration_is_enabled:
                client.logger.warning(
                    "Dependency Track - DefectDojo integration is not enabled. Attempting to enable it."
                )
                integration_is_enabled = dtrack.update_integration(config)

            if integration_is_enabled:
                dtrack_project = Project(
                    str(config.dtrack_project_name), str(config.dtrack_project_version)
                )
                dtrack_project_uuid = dtrack.get_project_uuid(dtrack_project)
                dtrack_project_properties = ProjectProperty(
                    dtrack_project_uuid,
                    engagement_id,
                    config.dtrack_reimport,
                    config.dtrack_reactivate,
                )
                dtrack.update_project_properties(dtrack_project_properties)

            else:
                client.logger.error(
                    "Skipping Dependency Track integration due to missing configuration."
                )
                return
