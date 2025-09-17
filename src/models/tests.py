from dataclasses import dataclass, field
from datetime import date


@dataclass
class Test:
    title: str
    engagement: int
    test_type: int
    description: str = "Created by Dojo CI"
    target_start: str = date.today().isoformat()
    target_end: str = date.today().isoformat()
    tags: list[str] = field(default_factory=lambda: ["defectdojo-importer"])
    build_id: str | None = None
    commit_hash: str | None = None
    branch_tag: str | None = None


@dataclass
class TestType:
    name: str
    active: bool = True
    tags: list[str] = field(default_factory=lambda: ["defectdojo-importer"])
    static_tool: bool = False
    dynamic_tool: bool = False
