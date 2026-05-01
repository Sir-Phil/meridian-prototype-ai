from openai import AsyncOpenAI
from .config import settings
import json

client = AsyncOpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url=settings.OPENROUTER_BASE_URL
)

class SupportAgent:
    def __init__(self, mcp_client):
        self.mcp = mcp_client
        self.messages = [
            {"role": "system", "content": "You are the Meridian Electronics Support Agent. Use tools to check availability and orders. Authenticate users before showing order details."}
        ]

    async def run(self, user_input: str):
        self.messages.append({"role": "user", "content": user_input})
        
        # 1. Fetch tools from MCP to pass to GPT
        mcp_tools = await self.mcp.get_tools()
        
        # Convert MCP tools to OpenAI tool schema
        openai_tools = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.inputSchema
                }
            } for t in mcp_tools
        ]

        # 2. First call to GPT
        response = await client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=self.messages,
            tools=openai_tools,
            tool_choice="auto"
        )

        response_message = response.choices[0].message
        
        # 3. Handle Tool Calls (The "Hands")
        if response_message.tool_calls:
            self.messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute via our MCP Client
                tool_result = await self.mcp.call_tool(function_name, function_args)
                
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": str(tool_result.content)
                })
            
            # 4. Final response after tool execution
            final_response = await client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=self.messages
            )
            return final_response.choices[0].message.content

        return response_message.content