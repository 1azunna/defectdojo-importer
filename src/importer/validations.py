import logging
from argparse import Namespace
from models.config import Config
from models.common import SeverityLevel, ReimportConditions
from models.exceptions import ConfigurationError
from common.utils import get_branch_tag, get_build_id, get_commit_hash, get_scm_uri

logger = logging.getLogger("defectdojo_importer")


def validate_config(args: Namespace, config: dict) -> Config:

    keys = list(Config.__dataclass_fields__.keys())
    merged_config = {key: getattr(args, key, None) or config.get(key) for key in keys}
    config_obj = Config(
        api_url=str(merged_config.get("api_url")),
        api_key=str(merged_config.get("api_key")),
        product_name=str(merged_config.get("product_name")),
        product_type_name=str(merged_config.get("product_type_name")),
        engagement_name=str(merged_config.get("engagement_name")),
        critical_product=bool(merged_config.get("critical_product")),
        product_platform=merged_config.get("product_platform"),
        test_name=merged_config.get("test_name"),
        test_type_name=merged_config.get("test_type_name"),
        tool_configuration_name=merged_config.get("tool_configuration_name"),
        tool_configuration_params=str(merged_config.get("tool_configuration_params")),
        static_tool=bool(merged_config.get("static_tool")),
        dynamic_tool=bool(merged_config.get("dynamic_tool")),
        minimum_severity=SeverityLevel(merged_config.get("minimum_severity")),
        push_to_jira=bool(merged_config.get("push_to_jira")),
        close_old_findings=bool(merged_config.get("close_old_findings")),
        build_id=str(merged_config.get("build_id")) or get_build_id(),
        commit_hash=str(merged_config.get("commit_hash")) or get_commit_hash(),
        branch_tag=str(merged_config.get("branch_tag")) or get_branch_tag(),
        scm_uri=str(merged_config.get("scm_uri")) or get_scm_uri(),
        reimport=bool(merged_config.get("reimport")),
        reimport_condition=ReimportConditions(merged_config.get("reimport_condition")),
        debug=bool(merged_config.get("debug")),
        dtrack_api_url=str(merged_config.get("dtrack_api_url")),
        dtrack_api_key=str(merged_config.get("dtrack_api_key")),
        dtrack_project_name=str(merged_config.get("dtrack_project_name")),
        dtrack_project_version=str(merged_config.get("dtrack_project_version")),
        dtrack_reimport=bool(merged_config.get("dtrack_reimport")),
        dtrack_reactivate=bool(merged_config.get("dtrack_reactivate")),
    )

    if not config_obj.api_url:
        raise ConfigurationError("DefectDojo API URL is required.")
    if not config_obj.api_key:
        raise ConfigurationError("DefectDojo API Key is required.")
    if not config_obj.product_name:
        raise ConfigurationError("Product name is required.")
    if not config_obj.product_type_name:
        raise ConfigurationError("Product type name is required.")

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
    return config_obj
