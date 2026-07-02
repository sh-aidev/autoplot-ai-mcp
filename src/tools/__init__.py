"""
MCP tool implementations, grouped one module per tool (or tool family).
"""

from mcp.server.fastmcp import FastMCP

from src.utils.config import Config
from src.tools.dataset_discovery import DatasetDiscoveryTool


def register_all(mcp: FastMCP, config: Config) -> None:
    """
    Registers every tool module's tools on the given FastMCP server.

    Args:
        mcp (FastMCP): The MCP server instance to register tools on.
        config (Config): Loaded application configuration.
    """
    DatasetDiscoveryTool(config).register(mcp)
