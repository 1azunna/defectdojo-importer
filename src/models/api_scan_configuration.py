from dataclasses import dataclass


@dataclass
class ApiScanConfig:
    product: int
    tool_configuration: int
    service_key_1: str | None = None
    service_key_2: str | None = None
    service_key_3: str | None = None
