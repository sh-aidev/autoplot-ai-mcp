<div align="center">

# MCP Server Template

[![python](https://img.shields.io/badge/-Python_%7C_3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![mcp](https://img.shields.io/badge/MCP_%7C_1.28+-000000?logo=modelcontextprotocol&logoColor=white)](https://modelcontextprotocol.io/)
[![uv](https://img.shields.io/badge/uv_%7C_0.11+-de5fe9?logo=uv&logoColor=white)](https://github.com/astral-sh/uv)
![license](https://img.shields.io/badge/License-MIT-green?logo=mit&logoColor=white)

A minimal MCP (Model Context Protocol) server template managed with [uv](https://github.com/astral-sh/uv), exposing a string-reversal tool and basic two-integer arithmetic tools (`add`, `subtract`, `multiply`, `divide`).

</div>

## 📌 Feature
- [x] `uv` for dependency management
- [x] TOML + Pydantic based config
- [x] `reverse_string` tool
- [x] `add` / `subtract` / `multiply` / `divide` tools
- [x] Centralized logging (loguru)
- [x] Custom exception handling
- [x] Standalone stdio client for manual testing

## 📁 Project Structure
The directory structure of the project looks like this:

```
├── LICENSE
├── Makefile
├── README.md
├── client.py
├── main.py
├── configs
│   └── config.toml
├── outputs
├── pyproject.toml
└── src
    ├── __init__.py
    ├── app.py
    ├── server
    │   ├── __init__.py
    │   └── server.py
    └── utils
        ├── __init__.py
        ├── config.py
        ├── exceptions.py
        ├── logger.py
        └── models.py
```

## 🚀 Getting Started

### Step 1: Install dependencies
```bash
uv sync
```

### Step 2: Run the server
```bash
uv run python main.py
# or
make run
```

The server communicates over stdio and is meant to be launched by an MCP client (see Step 3), not run standalone in a terminal.

### Step 3: Try it with the bundled client
```bash
uv run python client.py
# or
make client
```

This spawns `main.py` as a subprocess over stdio, lists the available tools, then prompts you to try `reverse_string` and the arithmetic tools.

### Step 4 (optional): Inspect it with the MCP Inspector
```bash
uv run mcp dev main.py:mcp
```
Opens a browser UI to browse and call the registered tools interactively. `main.py` exposes a lazily-built `mcp` attribute for this purpose (see `__getattr__` at the bottom of the file) — normal runs via `make run` / `make client` don't trigger it.

## 📜 References
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [uv](https://github.com/astral-sh/uv)
