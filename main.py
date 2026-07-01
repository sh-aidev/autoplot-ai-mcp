from dotenv import load_dotenv
load_dotenv()

import warnings

warnings.filterwarnings("ignore")

from src.utils.logger import logger
from src import App


def main():
    app = App()
    app.run()


def __getattr__(name: str):
    # Lazily exposes a bare FastMCP instance as `mcp` so `mcp dev` / `mcp run`
    # tooling (which looks for a module-level mcp/server/app object) can find
    # it via `uv run mcp dev main.py:mcp`, without constructing the server on
    # every normal import.
    if name == "mcp":
        return App().server.server
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if __name__ == "__main__":
    main()
