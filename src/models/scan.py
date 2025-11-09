import json
from datetime import date
from dataclasses import dataclass, field, asdict
from .common import SeverityLevel


@dataclass
class Scan:
    scan_type: str
    product_name: str
    test_title: str
    engagement: int
    engagement_name: str
    test: int | None = None
    push_to_jira: bool = False
    active: bool = True
    verified: bool = True
    api_scan_id: int | None = None
    close_old_findings: bool = True
    minimum_severity: SeverityLevel = SeverityLevel.INFO
    tags: list[str] = field(default_factory=lambda: ["defectdojo-importer"])
    scan_date: str = date.today().isoformat()
    build_id: str | None = None
    commit_hash: str | None = None
    branch_tag: str | None = None
    source_code_management_uri: str | None = None

    def to_dict(self):
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                if key == "minimum_severity":
                    result[key] = value.value
                else:
                    result[key] = value
        return result

    def to_json(self):
        return json.dumps(self.to_dict())
