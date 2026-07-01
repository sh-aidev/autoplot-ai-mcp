from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio


async def main():
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

            text = input("\nEnter text to reverse: ")
            reverse_result = await session.call_tool(
                "reverse_string",
                arguments={"text": text},
            )
            print(f"Reversed text: {reverse_result.content[0].text}")

            a = int(input("\nEnter first integer: "))
            b = int(input("Enter second integer: "))

            add_result = await session.call_tool("add", arguments={"a": a, "b": b})
            print(f"{a} + {b} = {add_result.content[0].text}")

            subtract_result = await session.call_tool("subtract", arguments={"a": a, "b": b})
            print(f"{a} - {b} = {subtract_result.content[0].text}")

            multiply_result = await session.call_tool("multiply", arguments={"a": a, "b": b})
            print(f"{a} * {b} = {multiply_result.content[0].text}")

            divide_result = await session.call_tool("divide", arguments={"a": a, "b": b})
            print(f"{a} / {b} = {divide_result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
