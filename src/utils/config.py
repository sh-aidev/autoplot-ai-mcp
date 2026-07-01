import toml
import os
from src.utils.models import AppConfig


class Config:

    def __init__(self, root_config_path: str):

        self.app_config = AppConfig(
            **toml.load(os.path.join(root_config_path, "config.toml"))
        )
