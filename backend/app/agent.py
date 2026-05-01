import os
import sys
import json
from openai import AsyncOpenAI

# --- VERCEL PATH FIX ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from config import settings

client = AsyncOpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url=settings.OPENROUTER_BASE_URL
)

class SupportAgent:
    def __init__(self, mcp_client):
        self.mcp = mcp_client
        # System prompt defines the persona and rules
        self.system_prompt = (
            "You are the Meridian Electronics Support Agent. "
            "Use tools to check availability and orders. "
            "Always authenticate users before showing specific order details."
        )

    async def run(self, user_input: str):
        # Start a fresh conversation context for each request (recommended for stateless APIs)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        # 1. Fetch current tools from MCP
        mcp_tools = await self.mcp.get_tools()
        
        # Map MCP tool definitions to OpenAI's function schema
        openai_tools = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.inputSchema
                }
            } for t in mcp_tools
        ] if mcp_tools else None

        # 2. Initial Model Call
        response = await client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=messages,
            tools=openai_tools,
            tool_choice="auto" if openai_tools else None
        )

        response_message = response.choices[0].message
        
        # 3. Handle Tool Calls
        if response_message.tool_calls:
            # Add the assistant's request for tool use to history
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"🛠️ Executing Tool: {function_name} with {function_args}")
                
                # Execute via MCP Client
                tool_result = await self.mcp.call_tool(function_name, function_args)
                
                # Add the result back to the conversation
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": str(tool_result.content)
                })
            
            # 4. Final response generation
            final_response = await client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=messages
            )
            return final_response.choices[0].message.content

        return response_message.content