from mcp.server.fastmcp import FastMCP

from src.utils.logger import logger
from src.utils.config import Config
from src.utils.exceptions import ToolExecutionError


class Server:
    def __init__(self, cfg: Config) -> None:
        self.config = cfg
        logger.debug("Configs Loaded...")

        self.server = FastMCP(self.config.app_config.server.name)
        logger.debug("MCP server initialized...")

        self._register_tools()
        logger.debug("Tools registered...")

    def _register_tools(self) -> None:
        @self.server.tool()
        def reverse_string(text: str) -> str:
            """Reverse a given string"""
            logger.debug(f"Reversing string: {text}")
            return text[::-1]

        @self.server.tool()
        def add(a: int, b: int) -> int:
            """Add two integers"""
            logger.debug(f"Adding {a} + {b}")
            return a + b

        @self.server.tool()
        def subtract(a: int, b: int) -> int:
            """Subtract the second integer from the first"""
            logger.debug(f"Subtracting {a} - {b}")
            return a - b

        @self.server.tool()
        def multiply(a: int, b: int) -> int:
            """Multiply two integers"""
            logger.debug(f"Multiplying {a} * {b}")
            return a * b

        @self.server.tool()
        def divide(a: int, b: int) -> float:
            """Divide the first integer by the second"""
            if b == 0:
                logger.error("Division by zero attempted")
                raise ToolExecutionError("Cannot divide by zero")
            logger.debug(f"Dividing {a} / {b}")
            return a / b

    def serve(self) -> None:
        logger.debug("Starting MCP server...")
        self.server.run()
