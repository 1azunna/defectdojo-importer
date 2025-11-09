from dataclasses import dataclass, asdict


@dataclass
class Project:
    name: str
    version: str

    def to_dict(self):
        return dict((x, y) for x, y in asdict(self).items() if y is not None)


@dataclass
class ProjectProperty:
    uuid: str
    engagement: int
    reimport: bool = True
    reactivate: bool = True
