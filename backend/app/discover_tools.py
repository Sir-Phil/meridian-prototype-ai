import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client
from config import settings 

async def discover_meridian_capabilities():
    print(f"Connecting to Meridian MCP at: {settings.MCP_SERVER_URL}...")
    
    async with sse_client(settings.MCP_SERVER_URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            tools_result = await session.list_tools()
            
            print("\n--- DISCOVERED TOOLS ---")
            for tool in tools_result.tools:
                print(f"\nTool Name: {tool.name}")
                print(f"Description: {tool.description}")
                print(f"Schema: {tool.inputSchema}")
            print("\n------------------------")

if __name__ == "__main__":
    asyncio.run(discover_meridian_capabilities())