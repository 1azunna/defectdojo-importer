import json
from dataclasses import dataclass, asdict


@dataclass
class ApiScanConfig:
    product: int
    tool_configuration: int
    service_key_1: str | None = None
    service_key_2: str | None = None
    service_key_3: str | None = None

    def to_dict(self):
        return dict((x, y) for x, y in asdict(self).items() if y is not None)

    def to_json(self):
        return json.dumps(self.to_dict())
