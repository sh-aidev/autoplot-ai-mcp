"""
Pydantic models describing the shape of the application's configuration.
"""

from pydantic import BaseModel


class Logger(BaseModel):
    """
    Configuration for the application logger.

    Args:
        environment (str): Deployment environment (e.g. "dev", "prod"),
                            used to select log verbosity.
    """

    environment: str


class Server(BaseModel):
    """
    Configuration for the MCP server.

    Args:
        name (str): Name the MCP server advertises to clients.
    """

    name: str


class ApiSource(BaseModel):
    """
    Configuration for a single external data source (API).

    Args:
        name (str): Identifier used to select this source (e.g. "world_bank").
        type (str): Which API shape this source speaks, used to pick the
                    right fetch strategy (e.g. "world_bank_v2", "data360").
        description (str): Human-readable description of the data source.
        discovery_endpoint (str): URL used to list available datasets.
        data_endpoint (str): URL (template) used to download a dataset.
        format (str): Response format requested from the API (default: "json").
        per_page (int): Number of results requested per page (default: 1000).
    """

    name: str
    type: str
    description: str
    discovery_endpoint: str
    data_endpoint: str
    format: str = "json"
    per_page: int = 1000


class AppConfig(BaseModel):
    """
    Top-level application configuration, merged from all config files.

    Args:
        logger (Logger): Logger configuration.
        server (Server): MCP server configuration.
        apis (list[ApiSource]): Configured external data sources.
    """

    logger: Logger
    server: Server
    apis: list[ApiSource]
