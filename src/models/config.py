import json
from dataclasses import dataclass, asdict
from .common import SeverityLevel, ReimportConditions


@dataclass
class Config:
    api_url: str
    api_key: str
    product_name: str
    product_type_name: str
    critical_product: bool
    product_platform: str | None
    engagement_name: str
    test_name: str | None
    test_type_name: str
    tool_configuration_name: str | None
    tool_configuration_params: str | None
    static_tool: bool
    dynamic_tool: bool
    minimum_severity: SeverityLevel
    push_to_jira: bool
    close_old_findings: bool
    build_id: str | None
    commit_hash: str | None
    branch_tag: str | None
    scm_uri: str | None
    reimport: bool
    reimport_condition: ReimportConditions
    debug: bool
    dtrack_api_url: str | None
    dtrack_api_key: str | None
    dtrack_project_name: str | None
    dtrack_project_version: str | None
    dtrack_reimport: bool
    dtrack_reactivate: bool

    def to_dict(self):
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                if key in ["minimum_severity", "reimport_condition"]:
                    result[key] = value.value
                else:
                    result[key] = value
        return result

    def to_json(self):
        return json.dumps(
            {
                key: value
                for key, value in self.to_dict().items()
                if key not in ["api_key", "dtrack_api_key"]
            }
        )
