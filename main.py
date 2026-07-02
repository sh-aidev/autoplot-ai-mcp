"""
Entry point for running the Autoplot AI MCP server as a standalone process.
"""

import warnings
import sys

from dotenv import load_dotenv
load_dotenv()

from src.utils.logger import logger
from src import App

warnings.filterwarnings("ignore")



def main():
    """
    Builds the `App` and runs the MCP server until interrupted.
    """
    logger.info("Initializing Autoplot MCP Server")
    app = App()
    logger.info("Autoplot MCP Server Initialized")
    logger.info("Starting Autoplot MCP Server")
    app.run()



def __getattr__(name: str):
    """
    Lazily exposes a bare FastMCP instance as `mcp` so `mcp dev` / `mcp run`
    tooling (which looks for a module-level mcp/server/app object) can find
    it via `uv run mcp dev main.py:mcp`, without constructing the server on
    every normal import.

    Args:
        name (str): Attribute name being accessed on this module.

    Returns:
        FastMCP: The underlying FastMCP server instance, when `name == "mcp"`.

    Raises:
        AttributeError: If `name` is anything other than "mcp".
    """
    if name == "mcp":
        return App().server.server
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Keyboard Interrupt")
        sys.exit(0)

