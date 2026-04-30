
---

# 🌐 Meridian AI Support Agent
### *Next-js + FastAPI + MCP Orchestration*

This project is a high-fidelity prototype of an **AI-powered Support Agent** for Meridian. It utilizes the **Model Context Protocol (MCP)** to securely bridge Large Language Models with Meridian’s internal order and inventory databases.

---

## 🚀 Key Features
*   **Agentic Workflow:** The agent doesn't just chat; it "thinks." It identifies when it needs data and autonomously calls tools to fetch it.
*   **MCP Integration:** Connects to a remote **Streamable HTTP (SSE)** MCP server for real-time inventory and order lookups.
*   **Multi-Step Authentication:** Demonstrates a secure "Identity-First" protocol, requiring user verification before accessing sensitive records.
*   **Modern Stack:** A responsive **Next.js** frontend paired with a high-performance **FastAPI** backend.

---

## 🏗 System Architecture

The system is designed as a modular monorepo:

*   **Frontend:** Next.js (App Router) hosted on **Vercel**.
*   **Backend:** FastAPI Agentic Service hosted on **Vercel Functions**.
*   **MCP Server:** Python SSE Server hosted on **Google Cloud Run**.



---

## 🛠 Tech Stack
*   **Frameworks:** Next.js 14, FastAPI.
*   **AI Orchestration:** MCP Python SDK, OpenAI/OpenRouter.
*   **Language:** TypeScript, Python 3.11+.
*   **Deployment:** Vercel (Web/API), GCP (MCP Server).

---

## 📖 How to Use the Demo

1.  **Start a Chat:** Open the deployed URL.
2.  **Request Info:** Ask for something like *"What is the status of order ORD-123?"*
3.  **Authentication Flow:** The Agent will recognize it lacks permissions. Follow the prompts to provide:
    *   Name & Email
    *   Order Confirmation / Phone digits
4.  **Tool Execution:** Once "Authenticated," the agent will connect to the MCP server, fetch the live data, and present it to you.

---

## ⚙️ Local Development

### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Set your .env: OPENROUTER_API_KEY, MCP_SERVER_URL
uvicorn app.main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🔗 Project Context
*   **MCP Server URL:** `[https://order-mcp-74afyau24q-uc.a.run.app/mcp](https://order-mcp-74afyau24q-uc.a.run.app/mcp)`
*   **Transport Mode:** SSE (Server-Sent Events)
*   **Discovery:** The backend utilizes `session.list_tools()` to dynamically discover capabilities at runtime.

---

meridian-prototype-ai/
├── vercel.json             # Root config for Vercel Monorepo routing
├── .gitignore              # Combined git ignore for Python/Node
├── frontend/               # Next.js Application
│   ├── src/
│   │   ├── app/            # App Router (Pages & Layout)
│   │   └── components/     # Chat UI Components
│   ├── public/             # Static assets
│   ├── package.json        # Frontend dependencies
│   └── next.config.mjs     # Next.js configuration
└── backend/                # FastAPI Application
    ├── app/
    │   ├── main.py         # Entry point & API Routes
    │   ├── agent.py        # AI Agent logic & System Prompts
    │   ├── mcp_client.py   # Meridian MCP Client (SSE Transport)
    │   └── config.py       # Pydantic Settings & Env management
    ├── requirements.txt    # Python dependencies for Vercel
    └── .env.example        # Template for API keys

**Author:** Philip Onuchukwu  
**Project:** Meridian AI Integration Challenge 2026