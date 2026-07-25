"""
Execution Agent Pydantic Models — Agent 4 interface contract.
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from backend.schemas.analysis_models import AnalysisResult
from backend.schemas.shared_models import UIState


class UIAction(BaseModel):
    action: str  # OPEN_TIMELINE | HIGHLIGHT_QUEUE_DELAY | OPEN_GRAPH | FOCUS_NODE | OPEN_SIMULATION
    target_id: Optional[str] = None
    params: Dict[str, Any] = {}


class GeneratedReport(BaseModel):
    report_type: str  # "manager_executive" | "engineer_detailed"
    markdown: str
    html: Optional[str] = None


class Notification(BaseModel):
    recipient: str
    subject: str
    body: str
    requires_approval: bool = True


class ExecutionInput(BaseModel):
    analysis: AnalysisResult
    current_ui: UIState
    intent: str
    raw_query: str


class ExecutionOutput(BaseModel):
    assistant_message: str
    conclusion: str
    confidence: float
    evidence_refs: List[str]
    assumptions: List[str]
    ui_actions: List[UIAction]
    generated_reports: List[GeneratedReport] = []
    notifications: List[Notification] = []
    actions_available: List[str]
    tool_trace: List[Dict[str, Any]] = []
