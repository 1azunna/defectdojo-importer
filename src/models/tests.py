import json
from dataclasses import dataclass, field, asdict
from datetime import date


@dataclass
class Test:
    title: str
    engagement: int
    test_type: int
    description: str = "Created by DefectDojo Importer"
    target_start: str = date.today().isoformat()
    target_end: str = date.today().isoformat()
    tags: list[str] = field(default_factory=lambda: ["defectdojo-importer"])
    build_id: str | None = None
    commit_hash: str | None = None
    branch_tag: str | None = None

    def to_dict(self):
        return dict((x, y) for x, y in asdict(self).items() if y is not None)

    def to_json(self):
        return json.dumps(self.to_dict())


@dataclass
class TestType:
    name: str
    active: bool = True
    tags: list[str] = field(default_factory=lambda: ["defectdojo-importer"])
    static_tool: bool = False
    dynamic_tool: bool = False

    def to_dict(self):
        return dict((x, y) for x, y in asdict(self).items() if y is not None)

    def to_json(self):
        return json.dumps(self.to_dict())
