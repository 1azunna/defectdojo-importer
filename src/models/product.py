from dataclasses import dataclass, field


@dataclass
class Product:
    name: str
    prod_type: int
    tags: list[str] = field(default_factory=lambda: ["defectdojo-importer"])
    enable_full_risk_acceptance: bool = True
    enable_simple_risk_acceptance: bool = True
    description: str = "Created by Defectdojo Importer"
    platform: str | None = None


@dataclass
class ProductType:
    name: str
    description: str = "Created by Defectdojo Importer"
    critical_product: bool = False
    key_product: bool = True
