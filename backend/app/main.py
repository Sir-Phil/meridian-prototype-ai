from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Internal Imports
from app.mcp_client import MeridianMCPClient
from app.agent import SupportAgent
from discover_tools import discover_meridian_capabilities

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This logic runs ONCE when the server starts.
    It acts as a 'Health Check' for your MCP connection.
    """
    print("\n--- [STARTUP] Initializing Meridian System ---")
    try:
        # Run discovery to log tools in the terminal for the demo
        await discover_meridian_capabilities()
        print("--- [STARTUP] MCP Discovery Successful ---\n")
    except Exception as e:
        print(f"--- [WARNING] MCP Discovery failed during startup: {e} ---")
        print("--- Check your MCP_SERVER_URL in .env ---\n")
    
    yield
    print("--- [SHUTDOWN] Cleaning up resources ---")

app = FastAPI(
    title="Meridian Support API",
    description="Backend for AI-integrated Inventory & Order Management",
    lifespan=lifespan
)

# 1. Enable CORS so Next.js can communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://meridian-prototype-ei9kk9ex1-phil9icy-5142s-projects.vercel.app", 
        "https://meridian-prototype-ai.vercel.app", # Your likely production URL
        "*" # Since "*" is here, it will work regardless, but good for best practice!
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Initialize the AI Logic
mcp_client = MeridianMCPClient()
agent = SupportAgent(mcp_client)

# 3. Define the request structure
class ChatRequest(BaseModel):
    message: str

# 4. Create the API endpoint for Next.js
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Receives text from Next.js, processes it through 
    the Agentic workflow, and returns the AI's response.
    """
    response = await agent.run(request.message)
    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    # Added 'app.' prefix so the reloader knows where to look
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)