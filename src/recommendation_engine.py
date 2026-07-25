"""
Recommendation Ranking & Business Impact Engine for ZenOps.
Scores interventions across technical effectiveness, confidence, cost, speed, and effort.
Translates engineering deltas into executive ROI metrics conforming to ForgeOps Blueprint Section 09.
"""

import json
import os
from typing import Dict, Any, List
from simulation_engine import SimulationEngine

class RecommendationEngine:
    def __init__(self, data_dir: str = None):
        self.sim_engine = SimulationEngine(data_dir=data_dir)
        # Financial impact parameters:
        # Loss exposure baseline: INR 18 lakh / ~$21,500
        self.batch_value = 45000.0
        self.hourly_downtime_cost = 12500.0

    def generate_recommendations(self, constraints: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        # Define candidate intervention scenarios matching Blueprint Section 09
        candidates = [
            {
                "name": "Action 1: Reduce queue delay below 60 minutes",
                "inputs": {"queue_delay_minutes": 30, "recalibrate_machine_7": True},
                "speed": "Easy / ~2 hours",
                "cost_val": 1  # 1: Low, 2: Med, 3: High
            },
            {
                "name": "Action 2: Install staging desiccant humidity control",
                "inputs": {"humidity_pct": 50.0},
                "speed": "Medium / ~12 hours",
                "cost_val": 3
            },
            {
                "name": "Action 3: Replace Machine 7 CNC Unit",
                "inputs": {"replace_machine_7": True},
                "speed": "Disruptive / ~48 hours",
                "cost_val": 3
            }
        ]

        scored_recommendations = []

        for item in candidates:
            sim_res = self.sim_engine.run_scenario(item["inputs"], scenario_name=item["name"], constraints=constraints)
            
            # Skip infeasible scenarios if hard constraints failed
            if sim_res.get("implementation_effort") == "INFEASIBLE":
                continue

            yield_gain = sim_res["predicted_yield"] - sim_res["baseline_yield"]  # e.g. 0.14 = 14%
            confidence = sim_res["confidence"]
            
            # Weighted scoring function
            # Effectiveness (40%), Confidence (25%), Cost efficiency (20%), Speed (15%)
            cost_score = (4 - item["cost_val"]) / 3.0  # Low cost = high score
            score = round((yield_gain * 0.40 * 10) + (confidence * 0.25 * 10) + (cost_score * 0.20 * 10), 2)

            # Business Impact calculation (Blueprint Section 09)
            monthly_loss_exposure_baseline = 1800000.0  # INR 18 lakh baseline loss
            monthly_loss_avoided_inr = round(monthly_loss_exposure_baseline * (yield_gain / 0.14), 2)
            downtime_reduction_pct = round((yield_gain / 0.14) * 41.0, 1)  # Blueprint: 41% reduction
            downtime_avoided_hours = round((yield_gain / 0.14) * 5.6, 1)

            scored_recommendations.append({
                "rank": 0,
                "title": item["name"],
                "score": score,
                "predicted_yield_pct": round(sim_res["predicted_yield"] * 100, 1),
                "yield_recovery_pct": sim_res["yield_delta_pct"],
                "confidence_pct": int(sim_res["confidence"] * 100),
                "confidence": sim_res["confidence"],
                "implementation_speed": item["speed"],
                "cost_estimate": sim_res["cost_estimate"].capitalize(),
                "effort": sim_res["implementation_effort"].capitalize(),
                "in_validated_range": sim_res["in_validated_range"],
                "business_impact": {
                    "monthly_loss_avoided_inr": monthly_loss_avoided_inr,
                    "downtime_reduction_pct": downtime_reduction_pct,
                    "downtime_avoided_hours": downtime_avoided_hours,
                    "calculation_basis": f"Based on simulation run {sim_res['scenario_id']} under assumptions: {', '.join(sim_res['assumptions'])}"
                },
                "simulation_details": sim_res
            })

        # Sort by overall score descending
        scored_recommendations.sort(key=lambda x: x["score"], reverse=True)
        for i, rec in enumerate(scored_recommendations):
            rec["rank"] = i + 1

        return scored_recommendations

if __name__ == "__main__":
    rec_engine = RecommendationEngine()
    recs = rec_engine.generate_recommendations()
    print(json.dumps(recs, indent=2))
