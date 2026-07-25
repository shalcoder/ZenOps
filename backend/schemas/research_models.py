"""
Research Agent Pydantic Models — Agent 2 interface contract.
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from backend.schemas.planner_models import ExecutionPlan


class ResearchInput(BaseModel):
    execution_plan: ExecutionPlan
    incident_id: str = "INC-2407-001"
    batch_id: str = "B-2407-184"


class SensorReading(BaseModel):
    reading_id: str
    timestamp: str
    humidity_pct: float
    temperature_c: float
    queue_delay_minutes: float
    cycle_time_seconds: float
    source: str
    record_id: str


class EvidenceBundle(BaseModel):
    batch_history: Dict[str, Any] = {}
    machine_history: Dict[str, Any] = {}
    sensor_readings: List[Dict[str, Any]] = []
    quality_data: Dict[str, Any] = {}
    maintenance_logs: List[Dict[str, Any]] = []
    historical_incidents: List[Dict[str, Any]] = []
    causal_graph: Dict[str, Any] = {}
    timeline_events: List[Dict[str, Any]] = []
    constraints: Dict[str, Any] = {}
    retrieval_sources: List[str] = []
