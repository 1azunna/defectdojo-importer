import json
from dataclasses import dataclass, field, asdict


@dataclass
class Product:
    name: str
    prod_type: int
    tags: list[str] = field(default_factory=lambda: ["defectdojo-importer"])
    enable_full_risk_acceptance: bool = True
    enable_simple_risk_acceptance: bool = True
    description: str = "Created by Defectdojo Importer"
    platform: str | None = None

    def to_dict(self):
        return dict((x, y) for x, y in asdict(self).items() if y is not None)

    def to_json(self):
        return json.dumps(self.to_dict())


@dataclass
class ProductType:
    name: str
    description: str = "Created by Defectdojo Importer"
    critical_product: bool = False
    key_product: bool = True

    def to_dict(self):
        return dict((x, y) for x, y in asdict(self).items() if y is not None)

    def to_json(self):
        return json.dumps(self.to_dict())
