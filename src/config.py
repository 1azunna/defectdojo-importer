import os
from argparse import Namespace
from dotenv import dotenv_values
from models.config import Config


env = {
    **os.environ,
    **dotenv_values(".env"),
    **dotenv_values(".env.defectdojo"),
}


def env_config(defaults: Namespace) -> dict:
    """Return config dict from environment variables and defaults."""
    # pylint: disable=no-member
    keys = list(Config.__dataclass_fields__.keys())
    config_dict = {key: env.get(f"DD_{key.upper()}", getattr(defaults, key, None)) for key in keys}
    config_dict = {key: value for key, value in config_dict.items() if value is not None}

    return config_dict
