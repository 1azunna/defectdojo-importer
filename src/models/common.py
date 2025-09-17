from dataclasses import dataclass
from enum import Enum


@dataclass
class SeverityLevel(Enum):
    INFO = "Info"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"
