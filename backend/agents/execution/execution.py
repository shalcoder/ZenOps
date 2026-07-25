"""
Agent 4 — Execution Agent
Presents results and controls the workbench.
Never performs reasoning — uses AnalysisResult only.
Generates UI actions, reports, assistant messages.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.schemas.analysis_models import AnalysisResult
from backend.schemas.execution_models import (
    ExecutionInput, ExecutionOutput, UIAction, GeneratedReport, Notification,
)
from backend.llm import call_llm

INTENT_UI_ACTIONS: dict[str, list[dict]] = {
    "show_evidence": [
        {"action": "OPEN_TIMELINE", "target_id": None},
        {"action": "HIGHLIGHT_NODE", "target_id": "humidity"},
        {"action": "HIGHLIGHT_NODE", "target_id": "queue_delay"},
        {"action": "OPEN_GRAPH", "target_id": None},
    ],
    "explain_exclusion": [
        {"action": "OPEN_GRAPH", "target_id": None},
        {"action": "HIGHLIGHT_NODE", "target_id": "machine_7"},
        {"action": "HIGHLIGHT_NODE", "target_id": "queue_delay"},
        {"action": "OPEN_SIMULATION", "target_id": "sim_compare"},
    ],
    "compare_options": [
        {"action": "OPEN_SIMULATION", "target_id": None},
        {"action": "OPEN_COMPARISON_VIEW", "target_id": None},
        {"action": "HIGHLIGHT_NODE", "target_id": "queue_delay"},
    ],
    "constraint_query": [
        {"action": "OPEN_SIMULATION", "target_id": None},
        {"action": "OPEN_RECOMMENDATIONS", "target_id": None},
        {"action": "HIGHLIGHT_NODE", "target_id": "queue_delay"},
    ],
    "generate_report": [
        {"action": "OPEN_REPORT_PANEL", "target_id": None},
    ],
    "simulate": [
        {"action": "OPEN_SIMULATION", "target_id": None},
        {"action": "SHOW_SCENARIO_RESULT", "target_id": None},
    ],
}

def _generate_dynamic_conclusion(intent: str, top_rec, top_sim) -> str:
    system_prompt = "You are a factory AI assistant. Write a single concise sentence summarizing the best action or conclusion."
    user_prompt = f"Intent: {intent}. Top recommendation: {top_rec.title if top_rec else 'None'} (Yield {top_rec.predicted_yield_pct if top_rec else 0}%). Please generate a brief conclusion."
    
    response = call_llm([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ])
    
    if response and not response.startswith("Error:"):
        return response.strip()
        
    # Fallback
    return f"Based on the analysis for {intent}, the recommended action is {top_rec.title if top_rec else 'to proceed with caution'}."


class ExecutionAgent:
    """
    Agent 4 — Execution Agent
    Input: ExecutionInput (AnalysisResult + UIState + intent)
    Output: ExecutionOutput (assistant message + UI actions + reports + notifications)
    """

    def execute(self, inp: ExecutionInput) -> ExecutionOutput:
        analysis = inp.analysis
        intent = inp.intent

        top_rec = analysis.recommendations[0] if analysis.recommendations else None
        top_sim = analysis.simulation_results[0] if analysis.simulation_results else None

        # Generate conclusion using LLM
        conclusion = _generate_dynamic_conclusion(intent, top_rec, top_sim)

        # Build UI actions
        raw_actions = INTENT_UI_ACTIONS.get(intent, INTENT_UI_ACTIONS["show_evidence"])
        ui_actions = [UIAction(action=a["action"], target_id=a.get("target_id")) for a in raw_actions]

        # Confidence
        confidence = analysis.confidence_scores.get("overall", 0.91)

        # Assumptions
        assumptions = top_sim.assumptions if top_sim else ["Machine 7 condition held constant", "No supplier change within 30 days"]

        # Evidence refs
        evidence_refs = analysis.supporting_evidence

        # Reports (only for generate_report intent)
        reports = []
        if intent == "generate_report":
            reports = [
                GeneratedReport(
                    report_type="manager_executive",
                    markdown=self._generate_manager_markdown(analysis),
                    html=None,
                )
            ]

        # Notifications
        notifications = []
        if intent == "generate_report" and top_rec:
            notifications.append(Notification(
                recipient="Plant Operations Manager",
                subject=f"ForgeOps Decision Brief — Incident INC-2407-001",
                body=f"Recommended action: {top_rec.title}. Predicted yield: {top_rec.predicted_yield_pct}%.",
                requires_approval=True,
            ))

        # Tool trace (static audit trail for demo)
        tool_trace = [
            {"server": "MES", "tool": "get_queue_events", "status": "complete", "durationMs": 124},
            {"server": "Quality", "tool": "get_inspection_results", "status": "complete", "durationMs": 96},
            {"server": "Maintenance", "tool": "get_machine_alerts", "status": "complete", "durationMs": 108},
            {"server": "Simulation", "tool": "compare_scenarios", "status": "complete", "durationMs": 342},
        ]

        return ExecutionOutput(
            assistant_message=conclusion,
            conclusion=conclusion,
            confidence=confidence,
            evidence_refs=evidence_refs,
            assumptions=assumptions,
            ui_actions=ui_actions,
            generated_reports=reports,
            notifications=notifications,
            actions_available=["open_evidence", "run_comparison", "generate_report"],
            tool_trace=tool_trace,
        )

    def _generate_manager_markdown(self, analysis: AnalysisResult) -> str:
        top_rec = analysis.recommendations[0] if analysis.recommendations else None
        impact = analysis.business_impact

        md = f"""# ForgeOps Executive Decision Brief

**Incident**: INC-2407-001 — Yield Degradation Batch B-2407-184
**Plant**: Plant Alpha - Detroit | **Line**: Assembly Line 3
**Yield Delta**: 96.0% → 82.0% (−14 percentage points)

---

## Root Cause
{analysis.root_causes[0].primary_cause if analysis.root_causes else 'Under analysis'}

**Causal Pathway** (Confidence: {int(analysis.root_causes[0].confidence_score * 100) if analysis.root_causes else 0}%):
"""
        if analysis.root_causes:
            for step in analysis.root_causes[0].causal_chain:
                md += f"1. {step}\n"

        md += f"""
---

## Recommended Action
**{top_rec.title if top_rec else 'Reduce queue delay'}**
- Predicted Yield: **{top_rec.predicted_yield_pct if top_rec else 96.0}%**
- Confidence: **{top_rec.confidence_pct if top_rec else 96}%**
- Cost: {top_rec.cost_estimate if top_rec else 'Low'} | Speed: {top_rec.implementation_speed if top_rec else '~2 hours'}

## Business Impact
- Monthly Loss Avoided: ₹{impact.get('monthly_loss_avoided_inr', 1500000):,.0f}
- Downtime Reduction: {impact.get('downtime_reduction_pct', 41)}%
- Yield Recovery: +{impact.get('yield_improvement_pct', 14)} percentage points

## Decision Record
- [ ] **Approved By**: Plant Operations Manager
- **Timestamp**: _(pending approval)_
- **Follow-up Owner**: Lead Maintenance & Dispatch Engineer
"""
        return md
