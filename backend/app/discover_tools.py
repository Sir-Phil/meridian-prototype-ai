import os
import sys
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

# --- VERCEL PATH FIX ---
# Ensures 'config.py' can be found in the same directory on serverless environments
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from config import settings 

async def discover_meridian_capabilities():
    """
    Connects to the MCP server to list all available tools.
    Useful for debugging and verifying the agent's 'vision'.
    """
    print(f"🔍 Connecting to Meridian MCP at: {settings.MCP_SERVER_URL}...")
    
    try:
        # Use a timeout context to prevent the script from hanging indefinitely
        async with asyncio.timeout(15.0): 
            async with sse_client(settings.MCP_SERVER_URL) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    
                    tools_result = await session.list_tools()
                    
                    if not tools_result.tools:
                        print("⚠️ No tools found on the server.")
                        return

                    print("\n🚀 --- DISCOVERED TOOLS ---")
                    for tool in tools_result.tools:
                        print(f"📦 Name: {tool.name}")
                        print(f"📝 Info: {tool.description}")
                        # Using json.dumps makes the schema much easier to read in logs
                        import json
                        print(f"⚙️  Schema: {json.dumps(tool.inputSchema, indent=2)}")
                        print("-" * 30)
                    
                    print(f"\n✅ Discovery Complete: {len(tools_result.tools)} tools found.")
                    
    except asyncio.TimeoutError:
        print("❌ Error: Connection timed out. Is the MCP server awake?")
    except Exception as e:
        print(f"❌ Discovery failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(discover_meridian_capabilities())