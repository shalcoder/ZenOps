"""
FastAPI main entry point for the ForgeOps 4-Agent Backend.
Exposes HTTP endpoints for the frontend and testing.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.pipeline import run_pipeline
from backend.database.audit_log import get_audit_log
from backend.config import FORGEOPS_MCP_URL, FORGEOPS_MODEL, LIVE_AGENTS_ENABLED
from backend.mcp.nitro_mcp_client import NitroMCPClient

app = FastAPI(
    title="ForgeOps 4-Agent Pipeline API",
    description="Planner → Research → Analysis → Execution multi-agent backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str
    incident_id: Optional[str] = "INC-2407-001"
    batch_id: Optional[str] = "B-2407-184"
    constraints: Dict[str, Any] = Field(default_factory=dict)


def _health_payload():
    mcp_attached = False
    tool_count = 0
    mcp_error = None
    try:
        with NitroMCPClient(timeout=12) as client:
            tool_count = len(client.list_tools())
            mcp_attached = tool_count > 0
    except Exception as exc:
        mcp_error = str(exc)
    return {
        "status": "ok" if mcp_attached else "degraded",
        "service": "forgeops-agent-pipeline",
        "agents": ["planner", "research", "analysis", "execution"],
        "agentRoles": 4,
        "orchestratorProcesses": 1,
        "llmBacked": LIVE_AGENTS_ENABLED,
        "model": FORGEOPS_MODEL,
        "mcp": {
            "attached": mcp_attached,
            "endpoint": FORGEOPS_MCP_URL,
            "toolCount": tool_count,
            "error": mcp_error,
        },
    }


@app.get("/api/health")
def health():
    return _health_payload()


@app.get("/api/agent/health")
def agent_health():
    return _health_payload()


@app.post("/api/agent/pipeline")
def pipeline_query(req: QueryRequest):
    """Run the full 4-agent pipeline for a user query."""
    result = run_pipeline(
        user_query=req.query,
        incident_id=req.incident_id,
        batch_id=req.batch_id,
        constraints=req.constraints,
    )
    return result.model_dump()


@app.get("/api/audit/log")
def audit_log(limit: int = 20):
    """Return the audit trail of agent pipeline runs."""
    return get_audit_log(limit=limit)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
