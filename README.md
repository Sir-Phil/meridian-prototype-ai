
```markdown
# 🌐 Meridian AI Support Agent
### *Next.js + FastAPI + MCP Orchestration*

This project is a high-fidelity prototype of an **AI-powered Support Agent** for Meridian. It demonstrates the use of the **Model Context Protocol (MCP)** to securely bridge Large Language Models with Meridian’s internal order and inventory databases.

---

## 🏗 Project Structure
```text
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
```

---

## 🚀 Key Features

*   **Agentic Workflow:** The agent identifies when it needs data and autonomously calls tools to fetch it.
*   **MCP Integration:** Connects to a remote **Streamable HTTP (SSE)** MCP server for real-time inventory and order lookups.
*   **Multi-Step Authentication:** A secure "Identity-First" protocol, requiring user verification (Name, Email, Phone digits) before accessing sensitive records.
*   **Modern Monorepo:** Unified deployment of a **Next.js** frontend and **FastAPI** backend via Vercel.

---

## 🛠 Tech Stack

*   **Frontend:** Next.js 14 (App Router), Tailwind CSS.
*   **Backend:** FastAPI, Python 3.11+.
*   **AI Orchestration:** MCP Python SDK, OpenRouter (LLM).
*   **Infrastructure:** Vercel (Web/API), Google Cloud Run (MCP Server).

---

## 📖 How to Use the Demo

1.  **Open the App:** Navigate to the deployed Vercel URL.
2.  **Inquire:** Ask for order details, e.g., *"Can you check the status of order ORD-123?"*
3.  **Authenticate:** Follow the agent's prompts to verify your identity.
4.  **Live Tool Call:** Watch as the agent handshakes with the MCP server to retrieve live inventory or order status data.

---

## ⚙️ Local Development

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
# Configure .env with OPENROUTER_API_KEY and MCP_SERVER_URL
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

**Author:** Philip Onuchukwu  
**Project:** Meridian AI Integration Challenge 2026
```