import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client
from config import settings

class MeridianMCPClient:
    def __init__(self):
        self.session = None
        self._client_context = None

    async def connect(self):
        """Establishes connection with a safety timeout."""
        if self.session:
            return self.session

        print(f"DEBUG: Attempting connection to {settings.MCP_SERVER_URL}")
        try:
            # Use wait_for to ensure the cloud server doesn't hang our backend
            self._client_context = sse_client(settings.MCP_SERVER_URL)
            
            # This is the line that was hanging:
            read_stream, write_stream = await asyncio.wait_for(
                self._client_context.__aenter__(), 
                timeout=10.0
            )
            
            self.session = ClientSession(read_stream, write_stream)
            await asyncio.wait_for(self.session.initialize(), timeout=5.0)
            
            print("✅ Meridian MCP Connected Successfully")
            return self.session
        except asyncio.TimeoutError:
            print("❌ MCP Connection Timeout: Server is likely cold-starting.")
            raise Exception("Meridian Server Timeout")
        except Exception as e:
            print(f"❌ MCP Connection Error: {str(e)}")
            raise e

    async def get_tools(self):
        """Fetches tools; returns an empty list if the server is down."""
        try:
            if not self.session:
                await self.connect()
            response = await self.session.list_tools()
            return response.tools
        except Exception as e:
            print(f"❌ Error fetching tools: {str(e)}")
            # Return empty list so the Agent can still function (or explain the error)
            return []

    async def call_tool(self, tool_name: str, arguments: dict):
        if not self.session:
            await self.connect()
        return await self.session.call_tool(tool_name, arguments)