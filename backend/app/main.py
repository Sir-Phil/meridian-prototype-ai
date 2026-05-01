import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- VERCEL PATH FIX ---
# This ensures sibling files like discover_tools.py can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import local modules using flat imports
from discover_tools import discover_meridian_capabilities
from mcp_client import MeridianMCPClient
from agent import SupportAgent
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Logic runs on server start. Acts as a Health Check for MCP.
    """
    print("\n--- [STARTUP] Initializing Meridian System ---")
    try:
        # Check if MCP server is reachable
        await discover_meridian_capabilities()
        print("--- [STARTUP] MCP Discovery Successful ---\n")
    except Exception as e:
        print(f"--- [WARNING] MCP Discovery failed: {e} ---")
    
    yield
    # Cleanup logic if necessary
    print("--- [SHUTDOWN] Cleaning up resources ---")

app = FastAPI(
    title="Meridian Support API",
    description="Backend for AI-integrated Inventory & Order Management",
    lifespan=lifespan
)

# Enable CORS for Next.js communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://meridian-prototype-ai.vercel.app", 
        "*" 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Logic
mcp_client = MeridianMCPClient()
agent = SupportAgent(mcp_client)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Processes text from Next.js through the Agentic workflow.
    """
    response = await agent.run(request.message)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    # Use "main:app" for easier local reloading
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)