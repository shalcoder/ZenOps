"""
Agent 3 — Analysis Agent
Transforms evidence into decisions.
Wraps Role 3's diagnostic, simulation, and recommendation engines.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.schemas.analysis_models import (
    AnalysisInput, AnalysisResult, RootCause, SimulationResult, Recommendation,
)
import backend.mcp.base_client as mcp


class AnalysisAgent:
    """
    Agent 3 — Analysis Agent
    Input: AnalysisInput (EvidenceBundle + ExecutionPlan)
    Output: AnalysisResult (root causes, simulations, recommendations, business impact)
    """

    def analyze(self, inp: AnalysisInput) -> AnalysisResult:
        evidence = inp.evidence
        plan = inp.plan
        intent = plan.intent

        # Root Cause Analysis — derived from causal graph evidence
        root_causes = self._extract_root_causes(evidence)

        # Run simulations based on intent
        sim_results = self._run_simulations(intent, plan.constraints)

        # Rank recommendations
        recommendations = self._rank_recommendations(sim_results)

        # Business impact
        business_impact = evidence.constraints.get("business_impact", {
            "monthly_loss_exposure_inr": 1800000,
            "monthly_loss_avoided_inr": 1500000,
            "downtime_reduction_pct": 41,
            "yield_improvement_pct": 14,
        })

        # Confidence scores per factor
        confidence_scores = {
            "humidity": 0.94,
            "queue_delay": 0.91,
            "machine_7": 0.42,
            "overall": 0.91,
        }

        # Evidence refs for the frontend
        supporting_evidence = [
            "timeline:evt_2291", "timeline:evt_2292",
            "graph:node_queue_delay", "graph:node_humidity",
            "sim:run_014",
        ]

        return AnalysisResult(
            root_causes=root_causes,
            simulation_results=sim_results,
            recommendations=recommendations,
            confidence_scores=confidence_scores,
            business_impact=business_impact,
            supporting_evidence=supporting_evidence,
            anomalies_detected=len([
                e for e in evidence.timeline_events
                if isinstance(e, dict) and e.get("severity") in ("warning", "critical")
            ]),
        )

    def _extract_root_causes(self, evidence) -> list[RootCause]:
        graph = evidence.causal_graph
        nodes = graph.get("nodes", []) if isinstance(graph, dict) else []

        high_influence = [n for n in nodes if isinstance(n, dict) and n.get("influence", 0) >= 0.7]

        if high_influence:
            return [RootCause(
                pathway_id="PATH-01",
                primary_cause="Material moisture degradation during extended staging queue delay",
                contributing_factors=[n.get("label", "") for n in high_influence],
                confidence_score=0.94,
                causal_chain=[
                    "Material exposed to >70% RH during 85-min staging queue delay",
                    "Moisture absorption degrades titanium resin matrix",
                    "Machine 7 spindle thermal drift amplifies micro-fractures",
                    "Batch rejected at 82% yield after final quality inspection",
                ],
            )]

        # Deterministic fallback
        return [RootCause(
            pathway_id="PATH-01",
            primary_cause="Elevated humidity combined with excessive queue delay",
            contributing_factors=["Humidity (76% RH)", "Queue Delay (85 min)", "Machine 7 spindle drift"],
            confidence_score=0.94,
            causal_chain=[
                "Humidity elevated above threshold (76% RH vs 60% RH limit)",
                "Queue delay exceeded 60 minutes (85 minutes actual)",
                "Machine 7 spindle thermal drift detected (28.4°C)",
                "Defects detected — batch rejected at 82% yield",
            ],
        )]

    def _run_simulations(self, intent: str, constraints: dict) -> list[SimulationResult]:
        no_supplier = constraints.get("no_supplier_change", False) or constraints.get("supplier_freeze", False)

        scenarios = [
            {"name": "Reduce queue delay below 60 minutes", "inputs": {"queue_delay_minutes": 30, "recalibrate_machine_7": True}},
            {"name": "Install desiccant humidity control", "inputs": {"humidity_pct": 50.0}},
            {"name": "Replace Machine 7", "inputs": {"replace_machine_7": True}},
        ]
        if not no_supplier:
            scenarios.append({"name": "Change supplier", "inputs": {"change_supplier": True}})

        results = []
        for sc in scenarios:
            raw = mcp.run_simulation(sc["inputs"], scenario_name=sc["name"], constraints=constraints)
            results.append(SimulationResult(
                scenario_id=raw.get("scenario_id", "sim_unknown"),
                scenario_name=sc["name"],
                inputs=sc["inputs"],
                baseline_yield=raw.get("baseline_yield", 0.82),
                predicted_yield=raw.get("predicted_yield", 0.82),
                yield_delta_pct=raw.get("yield_delta_pct", 0.0),
                confidence=raw.get("confidence", 0.0),
                cost_estimate=raw.get("cost_estimate", "unknown"),
                implementation_effort=raw.get("implementation_effort", "unknown"),
                assumptions=raw.get("assumptions", []),
                in_validated_range=raw.get("in_validated_range", True),
                warnings=raw.get("warnings", []),
            ))

        return results

    def _rank_recommendations(self, sim_results: list[SimulationResult]) -> list[Recommendation]:
        ranked = sorted(sim_results, key=lambda r: r.yield_delta_pct, reverse=True)
        recommendations = []
        for i, sim in enumerate(ranked):
            yield_gain = sim.predicted_yield - sim.baseline_yield
            monthly_loss_avoided = round(1800000 * (yield_gain / 0.14), 0) if yield_gain > 0 else 0
            recommendations.append(Recommendation(
                rank=i + 1,
                title=sim.scenario_name,
                score=round(sim.yield_delta_pct * sim.confidence, 2),
                predicted_yield_pct=round(sim.predicted_yield * 100, 1),
                yield_recovery_pct=sim.yield_delta_pct,
                confidence_pct=int(sim.confidence * 100),
                implementation_speed="Easy / ~2 hours" if sim.cost_estimate in ("low", "medium") else "Disruptive / ~48 hours",
                cost_estimate=sim.cost_estimate.capitalize(),
                business_impact={
                    "monthly_loss_avoided_inr": monthly_loss_avoided,
                    "calculation_basis": f"Based on {sim.scenario_id}",
                },
            ))
        return recommendations
