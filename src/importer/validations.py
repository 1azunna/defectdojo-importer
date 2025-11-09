import logging
from argparse import Namespace
from config import env_config
from models.config import Config
from models.common import SeverityLevel, ReimportConditions
from models.exceptions import ConfigurationError
from common.utils import get_branch_tag, get_build_id, get_commit_hash, get_scm_uri

logger = logging.getLogger("defectdojo_importer")


def validate_config(args: Namespace) -> Config:

    merged_config = env_config(args)
    # merged_config_output = {key: value for key, value in merged_config.items() if key not in ["api_key", "dtrack_api_key"]}

    if not merged_config.get("api_url"):
        raise ConfigurationError("DefectDojo API URL is required.")
    if not merged_config.get("api_key"):
        raise ConfigurationError("DefectDojo API Key is required.")
    if not merged_config.get("product_name"):
        raise ConfigurationError("Product name is required.")
    if not merged_config.get("product_type_name"):
        raise ConfigurationError("Product type name is required.")
    if not merged_config.get("test_type_name"):
        raise ConfigurationError("Test type name is required.")

    config_obj = Config(
        api_url=str(merged_config.get("api_url")),
        api_key=str(merged_config.get("api_key")),
        product_name=str(merged_config.get("product_name")),
        product_type_name=str(merged_config.get("product_type_name")),
        engagement_name=merged_config.get("engagement_name", "CI/CD Engagement"),
        critical_product=bool(merged_config.get("critical_product")),
        product_platform=merged_config.get("product_platform"),
        test_name=merged_config.get("test_name"),
        test_type_name=str(merged_config.get("test_type_name")),
        tool_configuration_name=merged_config.get("tool_configuration_name"),
        tool_configuration_params=merged_config.get("tool_configuration_params"),
        static_tool=bool(merged_config.get("static_tool")),
        dynamic_tool=bool(merged_config.get("dynamic_tool")),
        minimum_severity=SeverityLevel(merged_config.get("minimum_severity", "Info")),
        push_to_jira=bool(merged_config.get("push_to_jira")),
        close_old_findings=merged_config.get("close_old_findings", True),
        build_id=merged_config.get("build_id", get_build_id()),
        commit_hash=merged_config.get("commit_hash", get_commit_hash()),
        branch_tag=merged_config.get("branch_tag", get_branch_tag()),
        scm_uri=merged_config.get("scm_uri", get_scm_uri()),
        reimport=bool(merged_config.get("reimport")),
        reimport_condition=ReimportConditions(merged_config.get("reimport_condition", "default")),
        debug=bool(merged_config.get("debug")),
        dtrack_api_url=merged_config.get("dtrack_api_url"),
        dtrack_api_key=merged_config.get("dtrack_api_key"),
        dtrack_project_name=merged_config.get("dtrack_project_name"),
        dtrack_project_version=merged_config.get("dtrack_project_version"),
        dtrack_reimport=bool(merged_config.get("dtrack_reimport")),
        dtrack_reactivate=bool(merged_config.get("dtrack_reactivate")),
    )

    config_obj.test_name = config_obj.test_name or config_obj.test_type_name

    if config_obj.debug:
        logger.setLevel(logging.DEBUG)

    if args.sub_command == "integration":

        match args.integration_type:
            case "dtrack":
                if not config_obj.dtrack_api_url:
                    raise ConfigurationError("Dependency Track API URL is required.")
                if not config_obj.dtrack_api_key:
                    raise ConfigurationError("Dependency Track API Key is required.")

                if not config_obj.dtrack_project_name:
                    logger.warning(
                        "If --dtrack-project-name or DD_DTRACK_PROJECT_NAME is not explicitly set, there may be errors."
                    )
                    config_obj.dtrack_project_name = config_obj.product_name
                if not config_obj.dtrack_project_version:
                    logger.warning(
                        "If --dtrack-project-version or DD_DTRACK_PROJECT_VERSION is not explicitly set, there may be errors."
                    )
                    config_obj.dtrack_project_version = config_obj.branch_tag or config_obj.build_id

    elif config_obj.tool_configuration_name:
        if not config_obj.tool_configuration_params:
            raise ConfigurationError(
                "Tool configuration parameters are required for the specified tool configuration."
            )
    elif not args.file:
        raise ConfigurationError("File is required for import.")

    logger.info(config_obj.to_json())
    return config_obj
