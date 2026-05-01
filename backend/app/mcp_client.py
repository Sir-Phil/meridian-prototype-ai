import os
import sys
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

# --- VERCEL PATH FIX ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from config import settings

class MeridianMCPClient:
    def __init__(self):
        self.session = None
        self._client_context = None

    async def connect(self):
        """Establishes connection with a safety timeout to prevent Vercel hangs."""
        if self.session:
            return self.session

        print(f"DEBUG: Connecting to MCP Server at {settings.MCP_SERVER_URL}")
        try:
            # Initialize SSE Client
            self._client_context = sse_client(settings.MCP_SERVER_URL)
            
            # Timeout set to 10s to handle server cold-starts
            read_stream, write_stream = await asyncio.wait_for(
                self._client_context.__aenter__(), 
                timeout=10.0
            )
            
            self.session = ClientSession(read_stream, write_stream)
            
            # Initialize the session protocol
            await asyncio.wait_for(self.session.initialize(), timeout=5.0)
            
            print("✅ Meridian MCP Connected Successfully")
            return self.session

        except asyncio.TimeoutError:
            print("❌ MCP Connection Timeout: Check if the server is awake.")
            raise Exception("Meridian Server Timeout")
        except Exception as e:
            print(f"❌ MCP Connection Error: {str(e)}")
            raise e

    async def get_tools(self):
        """Fetches available tools from the MCP server."""
        try:
            if not self.session:
                await self.connect()
            response = await self.session.list_tools()
            return response.tools
        except Exception as e:
            print(f"❌ Error fetching tools: {str(e)}")
            return []

    async def call_tool(self, tool_name: str, arguments: dict):
        """Executes a tool call through the MCP session."""
        if not self.session:
            await self.connect()
        return await self.session.call_tool(tool_name, arguments)

    async def disconnect(self):
        """Gracefully closes the SSE connection."""
        if self._client_context:
            await self._client_context.__aexit__(None, None, None)
            self.session = None
            print("🔌 MCP Disconnected")