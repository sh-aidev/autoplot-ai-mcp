"""
Standalone MCP client that connects to the Autoplot AI server over stdio,
prompts for search keywords, and prints the matching datasets.
"""

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio


async def main():
    """
    Launches the MCP server as a subprocess, lists its tools, then calls
    `get_datasets_list` with keywords parsed from user input and prints
    the results.
    """
    server_params = StdioServerParameters(
        command="python",
        args=["main.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Connected to MCP server")

            print("\n--- Available tools ---")
            tools = (await session.list_tools()).tools
            for t in tools:
                print(f"- {t.name}: {t.description}")

            query = input("\nWhat kind of dataset are you looking for? ")
            keywords = [keyword.strip() for keyword in query.split() if keyword.strip()]
            result = await session.call_tool(
                "get_datasets_list",
                arguments={"keywords": keywords},
            )
            print(f"\n--- {len(result.content)} dataset(s) returned ---")
            for item in result.content:
                print(item.text)


if __name__ == "__main__":
    asyncio.run(main())
