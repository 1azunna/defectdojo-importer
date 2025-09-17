from dataclasses import dataclass
from .common import SeverityLevel


@dataclass
class Config:
    api_url: str
    api_key: str
    product_name: str
    product_type_name: str
    critical_product: bool = False
    product_platform: str | None = None
    engagement_name: str = "CI/CD Engagement"
    test_name: str | None = None
    test_type_name: str | None = None
    static_tool: bool = False
    dynamic_tool: bool = False
    minimum_severity: SeverityLevel = SeverityLevel.INFO
    push_to_jira: bool = False
    close_old_findings: bool = True
    build_id: str | None = None
    commit_hash: str | None = None
    branch_tag: str | None = None
    scm_uri: str | None = None
    dtrack_api_url: str | None = None
    dtrack_api_key: str | None = None
    dtrack_project_name: str | None = None
    dtrack_project_version: str | None = None
    dtrack_reimport: bool = True
    dtrack_reactivate: bool = True
