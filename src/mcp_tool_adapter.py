"""
MCP Tool Adapter for ZenOps (Interface between Role 1 Agent MCP server and Role 3 Data Engine).
Exposes JSON-serializable tool functions for MCP invocation.
"""

import json
import sys
import os
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulation_engine import SimulationEngine
from diagnostic_engine import DiagnosticEngine
from recommendation_engine import RecommendationEngine
from report_generator import ReportGenerator

def tool_run_scenario(inputs: Dict[str, Any], scenario_name: str = None) -> str:
    """
    MCP Tool Contract: run_scenario
    Inputs: Dict of parameters (e.g. {"queue_delay_minutes": 30, "recalibrate_machine_7": True})
    Returns: JSON string adhering to blueprint simulation contract
    """
    sim = SimulationEngine()
    result = sim.run_scenario(inputs, scenario_name=scenario_name)
    return json.dumps(result, indent=2)

def tool_compare_scenarios(scenarios: List[Dict[str, Any]]) -> str:
    """
    MCP Tool Contract: compare_scenarios
    Inputs: List of scenario objects [{"name": "S1", "inputs": {...}}, ...]
    Returns: JSON string matrix of scenario comparisons
    """
    sim = SimulationEngine()
    results = sim.compare_scenarios(scenarios)
    return json.dumps(results, indent=2)

def tool_get_incident_diagnostics(batch_id: str = "BATCH-INC-2026-07") -> str:
    """
    MCP Tool Contract: get_incident_diagnostics
    Returns: Anomaly detections and correlated root cause pathways
    """
    diag = DiagnosticEngine()
    result = diag.analyze_batch()
    return json.dumps(result, indent=2)

def tool_get_ranked_recommendations() -> str:
    """
    MCP Tool Contract: get_ranked_recommendations
    Returns: Ranked interventions with business financial impact
    """
    rec = RecommendationEngine()
    result = rec.generate_recommendations()
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    print("Testing MCP Tool Adapter...")
    sample_sim = tool_run_scenario({"queue_delay_minutes": 30, "recalibrate_machine_7": True}, "Demo Intervention")
    print(sample_sim)
