"""
MCP server setup for Autoplot AI.

Wraps a `FastMCP` instance and delegates registration of the data pipeline
tools (see `src.tools`) that MCP clients call to discover and download
datasets from the configured data sources.
"""

from mcp.server.fastmcp import FastMCP

from src.utils.logger import logger
from src.utils.config import Config
from src.tools import register_all


class Server:
    """
    MCP server wrapper that builds the FastMCP instance and registers tools.
    """

    def __init__(self, cfg: Config) -> None:
        """
        Initializes the underlying FastMCP server and registers its tools.

        Args:
            cfg (Config): Loaded application configuration, including the
                          server name and the list of configured API sources.
        """
        self.config = cfg
        logger.debug("Configs Loaded...")

        self.server = FastMCP(self.config.app_config.server.name)
        logger.debug("MCP server initialized...")

        register_all(self.server, self.config)
        logger.debug("Tools registered...")

    def serve(self) -> None:
        """
        Starts the MCP server and blocks, serving tool calls until stopped.
        """
        logger.debug("Starting MCP server...")
        self.server.run()
