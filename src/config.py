import os
from dotenv import dotenv_values
from models.config import Config


config = {
    **os.environ,
    **dotenv_values(".env"),
    **dotenv_values(".env.defectdojo"),
}


def env_config() -> dict:
    return {
        "api_url": config.get("DD_URL"),
        "api_key": config.get("DD_API_KEY"),
        "product_name": config.get("DD_PRODUCT_NAME"),
        "product_type_name": config.get("DD_PRODUCT_TYPE_NAME"),
        "critical_product": config.get("DD_CRITICAL_PRODUCT"),
        "product_platform": config.get("DD_PRODUCT_PLATFORM"),
        "engagement_name": config.get("DD_ENGAGEMENT_NAME"),
        "test_name": config.get("DD_TEST_NAME"),
        "test_type_name": config.get("DD_TEST_TYPE_NAME"),
        "tool_configuration_name": config.get("DD_TOOL_CONFIGURATION_NAME"),
        "tool_configuration_params": config.get("DD_TOOL_CONFIGURATION_PARAMS"),
        "static_tool": config.get("DD_STATIC_TOOL"),
        "dynamic_tool": config.get("DD_DYNAMIC_TOOL"),
        "minimum_severity": config.get("DD_MINIMUM_SEVERITY"),
        "push_to_jira": config.get("DD_PUSH_TO_JIRA"),
        "close_old_findings": config.get("DD_CLOSE_OLD_FINDINGS"),
        "build_id": config.get("DD_BUILD_ID"),
        "commit_hash": config.get("DD_COMMIT_HASH"),
        "branch_tag": config.get("DD_BRANCH_TAG"),
        "scm_uri": config.get("DD_SCM_URI"),
        "reimport": config.get("DD_REIMPORT"),
        "reimport_condition": config.get("DD_REIMPORT_CONDITION"),
        "debug": config.get("DD_DEBUG"),
        "dtrack_api_url": config.get("DD_DTRACK_API_URL"),
        "dtrack_api_key": config.get("DD_DTRACK_API_KEY"),
        "dtrack_project_name": config.get("DD_DTRACK_PROJECT_NAME"),
        "dtrack_project_version": config.get("DD_DTRACK_PROJECT_VERSION"),
        "dtrack_reimport": config.get("DD_DTRACK_REIMPORT"),
        "dtrack_reactivate": config.get("DD_DTRACK_REACTIVATE"),
    }


def defectdojo_config(config: Config) -> str:
    return f"""
DD_URL:                        {config.api_url}
DD_PRODUCT_TYPE_NAME:          {config.product_type_name}
DD_CRITICAL_PRODUCT:           {config.critical_product}
DD_PRODUCT_NAME:               {config.product_name}
DD_PRODUCT_PLATFORM:           {config.product_platform}
DD_ENGAGEMENT_NAME:            {config.engagement_name}
DD_TEST_NAME:                  {config.test_name}
DD_TEST_TYPE_NAME:             {config.test_type_name}
DD_TOOL_CONFIGURATION_NAME:    {config.tool_configuration_name}
DD_TOOL_CONFIGURATION_PARAMS:  {config.tool_configuration_params}
DD_STATIC_TOOL:                {config.static_tool}
DD_DYNAMIC_TOOL:               {config.dynamic_tool}
DD_MINIMUM_SEVERITY:           {config.minimum_severity.value}
DD_PUSH_TO_JIRA:               {config.push_to_jira}
DD_CLOSE_OLD_FINDINGS:         {config.close_old_findings}
DD_BUILD_ID:                   {config.build_id}
DD_COMMIT_HASH:                {config.commit_hash}
DD_BRANCH_TAG:                 {config.branch_tag}
DD_SCM_URI:                    {config.scm_uri}
DD_REIMPORT:                   {config.reimport}
DD_REIMPORT_CONDITION:         {config.reimport_condition.value}
DD_DEBUG:                      {config.debug}
"""


def dtrack_integration_config(config: Config) -> str:
    return f"""
DD_DTRACK_API_URL:             {config.dtrack_api_url}
DD_DTRACK_PROJECT_NAME:        {config.dtrack_project_name}
DD_DTRACK_PROJECT_VERSION:     {config.dtrack_project_version}
DD_DTRACK_REIMPORT:            {config.dtrack_reimport}
DD_DTRACK_REACTIVATE:          {config.dtrack_reactivate}
"""
