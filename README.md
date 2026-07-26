# ForgeOps — An agentic AI orchestrator for real-time manufacturing root-cause analysis and simulation

> ForgeOps is an explainable, multi-agent manufacturing decision-intelligence platform that turns fragmented factory data into evidence-backed corrective actions.

![Model Context Protocol](https://img.shields.io/badge/Model%20Context%20Protocol-MCP-blue) ![Built with Nitrostack](https://img.shields.io/badge/Built%20with-Nitrostack-0A66FF) ![Status](https://img.shields.io/badge/status-live-brightgreen)

**ForgeOps — An agentic AI orchestrator for real-time manufacturing root-cause analysis and simulation** uses an [MCP (Model Context Protocol)](https://nitrostack.ai) server that extends AI assistants with new, real-world manufacturing capabilities. It is built and deployed on [Nitrostack](https://nitrostack.ai), the fastest way to build, deploy, and share MCP apps.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Live Demo](#live-demo)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Connect to an MCP Client](#connect-to-an-mcp-client)
- [Deploy Your Own MCP App](#deploy-your-own-mcp-app)
- [License](#license)

## Overview

ForgeOps solves a critical industry problem: conventional monitoring systems detect faults but often cannot explain their causes, compare interventions, or show engineers why a decision should be trusted.

A Python orchestrator coordinates four specialized AI agents:
1. **Planner**: Defines the investigation strategy.
2. **Research**: Retrieves relevant operational evidence.
3. **Analysis**: Identifies causal relationships and evaluates counterfactual scenarios.
4. **Execution**: Produces the final recommendation with expected business impact.

The agents are powered through NitroCloud’s deployed NitroChat inference layer and its configured Gemini model. They use 16 MCP operations—11 direct tools and five task workflows—to securely access MES events, sensor telemetry, maintenance history, quality inspections, supplier constraints, production timelines, causal graphs, business-impact calculations, and simulations.

ForgeOps reconstructs production incidents, synchronizes anomalies across the manufacturing timeline, distinguishes symptoms from root causes, compares possible actions, and supports natural-language investigation. The React frontend communicates with the Python orchestration backend through HTTP APIs, displaying an interactive, auditable trace for human approval.

## Architecture

ForgeOps is a monorepo consisting of three main components:
*   `frontend/` (Root): React / Vite web application (The ForgeOps Workbench).
*   `backend/`: Python FastAPI orchestrator and Multi-Agent AI system.
*   `forgeops-mcp/`: TypeScript MCP Server exposing factory data tools (MES, Quality, Maintenance, Materials, Simulation).

## Live Demo

🚀 **Live MCP endpoint:** https://zenops-6a649dab-zen-net-amrita-university-coimbatore.app.nitrocloud.ai

Point your MCP client at the endpoint above to try it instantly. Prefer a hosted setup? Deploy your own in minutes on [Nitrostack](https://nitrostack.ai).

## Getting Started

### Prerequisites

- Node.js 18+ 
- Python 3.10+
- An MCP-compatible client (Claude Desktop, Cursor, etc.)

### Installation & Running Locally

Clone the repository:
```bash
git clone https://github.com/shalcoder/ZenOps.git
cd ZenOps
```

**1. Start the MCP Server:**
```bash
cd forgeops-mcp
npm install
npm run dev
```

**2. Start the Python Orchestrator Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**3. Start the Frontend Workbench:**
```bash
# From the root directory
npm install
npm run dev
```

## Configuration

We keep secrets strictly out of the repository. Copy the example environment file and add your own values to connect the frontend to the backend and MCP server.

```bash
cp .env.example .env
```

Ensure your `.env` contains your `VITE_FORGEOPS_API_URL` to point to your deployed backend, or `http://localhost:8000` for local development.

## Connect to an MCP Client

Add this server to your MCP client configuration (e.g., Claude Desktop). A typical entry looks like:

```json
{
  "mcpServers": {
    "forgeops": {
      "url": "https://zenops-6a649dab-zen-net-amrita-university-coimbatore.app.nitrocloud.ai"
    }
  }
}
```

Restart your client and the tools from this MCP server will be available to your AI assistant.

## Deploy Your Own MCP App

Want to build and ship an MCP server like this one? **[Nitrostack](https://nitrostack.ai)** lets you create, deploy, and host MCP apps in minutes — no infrastructure to manage.

## License

MIT © 2026 Zennet

---

Built with ❤️ using the Model Context Protocol on [Nitrostack](https://nitrostack.ai). Share your MCP app on [r/mcptothemoon](https://www.reddit.com/r/mcptothemoon/).
