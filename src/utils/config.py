"""
Loads and merges the application's TOML configuration files into a single
validated `AppConfig` model.
"""

import toml
import os
from src.utils.models import AppConfig


class Config:
    """
    Loads `config.toml` and `api_config.toml` from a directory and exposes
    them as a validated `AppConfig`.
    """

    def __init__(self, root_config_path: str):
        """
        Loads and merges the base and API configs into `self.app_config`.

        Args:
            root_config_path (str): Directory containing `config.toml` and
                                     `api_config.toml`.
        """
        base_config = toml.load(os.path.join(root_config_path, "config.toml"))
        api_config = toml.load(os.path.join(root_config_path, "api_config.toml"))

        self.app_config = AppConfig(**base_config, **api_config)
