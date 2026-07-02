"""
Application entry point that wires configuration to the MCP server.
"""

from src.utils.logger import logger
from src.utils.config import Config
from src.server.server import Server


class App:
    """
    Main application class to run the MCP server. This class will initialize the server and run it.
    """
    def __init__(self) -> None:
        """
        Initializes the App class by setting up the configuration and server.
        """
        root_config_dir = "configs"
        logger.debug(f"Root config dir: {root_config_dir}")
        self.config = Config(root_config_dir)
        self.server = Server(self.config)

    def run(self) -> None:
        """
        Runs the MCP server. This method starts the server and keeps it running until interrupted.
        """
        self.server.serve()
