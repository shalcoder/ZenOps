"""
Agent 2 — Research Agent
Retrieves all evidence from forgeops-mcp HTTP endpoints.
No reasoning. No recommendations. Pure retrieval and normalization.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.schemas.planner_models import ExecutionPlan, MCPServer
from backend.schemas.research_models import ResearchInput, EvidenceBundle
import backend.mcp.base_client as mcp


class ResearchAgent:
    """
    Agent 2 — Research Agent
    Input: ResearchInput (execution plan + incident/batch IDs)
    Output: EvidenceBundle (all evidence from all MCP servers)
    """

    def retrieve(self, inp: ResearchInput) -> EvidenceBundle:
        plan = inp.execution_plan
        required = set(plan.required_servers)
        bundle = EvidenceBundle()
        sources = []

        # Always retrieve core incident context
        incident = mcp.get_incident()
        bundle.batch_history = incident
        sources.append("orchestrator:incident")

        if MCPServer.MES in required or MCPServer.ORCHESTRATOR in required:
            timeline = mcp.get_timeline()
            bundle.timeline_events = timeline if isinstance(timeline, list) else []
            sources.append("mes:timeline")

        if MCPServer.MAINTENANCE in required:
            # Pull maintenance-relevant events from timeline
            maint_events = mcp.get_timeline(source_filter="maintenance")
            bundle.maintenance_logs = maint_events if isinstance(maint_events, list) else []
            sources.append("maintenance:alerts")

        if MCPServer.QUALITY in required:
            quality_events = mcp.get_timeline(source_filter="quality")
            bundle.quality_data = {"inspection_events": quality_events}
            sources.append("quality:inspections")

        if MCPServer.SIMULATION in required or MCPServer.ORCHESTRATOR in required:
            graph = mcp.get_causal_graph()
            bundle.causal_graph = graph
            sources.append("simulation:causal_graph")

        if MCPServer.ORCHESTRATOR in required:
            recs = mcp.get_recommendations()
            bundle.historical_incidents = recs  # Reuse field for recommendations bundle
            impact = mcp.get_business_impact()
            bundle.constraints = {"business_impact": impact}
            sources.append("orchestrator:recommendations")
            sources.append("orchestrator:business_impact")

        if MCPServer.MATERIALS in required:
            bundle.constraints["supplier_freeze"] = True
            bundle.constraints["no_supplier_change_days"] = 30
            sources.append("materials:constraints")

        bundle.retrieval_sources = sources
        return bundle
