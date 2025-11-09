import json
from datetime import date
from dataclasses import dataclass, asdict
from enum import Enum


class EngagementStatus(Enum):
    NOT_STARTED = "Not Started"
    BLOCKED = "Blocked"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    IN_PROGRESS = "In Progress"
    ON_HOLD = "On Hold"
    WAITING_FOR_RESOURCE = "Waiting for Resource"


@dataclass
class Engagement:
    name: str
    product: int
    description: str = "Created by Defectdojo Importer"
    engagement_type: str = "CI/CD"
    status: EngagementStatus = EngagementStatus.IN_PROGRESS
    target_start: str = date.today().isoformat()
    target_end: str = "2999-12-31"
    build_id: str | None = None
    commit_hash: str | None = None
    branch_tag: str | None = None

    def to_dict(self):
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                if key == "status":
                    result[key] = value.value
                else:
                    result[key] = value
        return result

    def to_json(self):
        return json.dumps(self.to_dict())
