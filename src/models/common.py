from enum import Enum


class ImportTypes(Enum):
    FINDINGS = "findings"
    LANGUAGES = "languages"


class ReimportConditions(Enum):
    DEFAULT = "default"
    BRANCH = "branch"
    COMMIT = "commit"
    BUILD = "build"
    PULL_REQUEST = "pull_request"


class SeverityLevel(Enum):
    INFO = "Info"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"
