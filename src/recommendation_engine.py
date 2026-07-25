"""
Recommendation Ranking & Business Impact Engine for ZenOps.
Scores interventions across technical effectiveness, confidence, cost, speed, and effort.
Translates engineering deltas into executive ROI metrics.
"""

import json
import os
from typing import Dict, Any, List
from simulation_engine import SimulationEngine

class RecommendationEngine:
    def __init__(self, data_dir: str = None):
        self.sim_engine = SimulationEngine(data_dir=data_dir)
        # Cost per scrapped batch: $45,000
        # Hourly downtime cost: $12,500
        self.batch_value = 45000.0
        self.hourly_downtime_cost = 12500.0

    def generate_recommendations(self) -> List[Dict[str, Any]]:
        # Define candidate intervention scenarios
        candidates = [
            {
                "name": "Intervention A: Recalibrate Machine 7 + Cap Queue Delay at 30 mins",
                "inputs": {"queue_delay_minutes": 30, "recalibrate_machine_7": True},
                "speed": "Immediate (2 hrs)",
                "cost_val": 1  # 1: Low, 2: Med, 3: High
            },
            {
                "name": "Intervention B: Activate Desiccant Dehumidifiers + Staging Queue Priority",
                "inputs": {"queue_delay_minutes": 25, "humidity_pct": 45.0},
                "speed": "Fast (4 hrs)",
                "cost_val": 2
            },
            {
                "name": "Intervention C: Complete Supplier Resin Changeover",
                "inputs": {"change_supplier": True},
                "speed": "Slow (30 days)",
                "cost_val": 3
            }
        ]

        scored_recommendations = []

        for item in candidates:
            sim_res = self.sim_engine.run_scenario(item["inputs"], scenario_name=item["name"])
            
            yield_gain = sim_res["predicted_yield"] - sim_res["baseline_yield"]  # e.g. 0.14 = 14%
            confidence = sim_res["confidence"]
            
            # Weighted scoring function
            # Effectiveness (40%), Confidence (25%), Cost efficiency (20%), Speed (15%)
            cost_score = (4 - item["cost_val"]) / 3.0  # Low cost = high score
            score = round((yield_gain * 0.40 * 10) + (confidence * 0.25 * 10) + (cost_score * 0.20 * 10), 2)

            # Business Impact calculation
            recovered_batches_per_month = 12
            monthly_loss_avoided = round(yield_gain * recovered_batches_per_month * self.batch_value, 2)
            downtime_avoided_hours = round(yield_gain * 40.0, 1)
            downtime_savings = round(downtime_avoided_hours * self.hourly_downtime_cost, 2)

            scored_recommendations.append({
                "rank": 0,  # Will sort & assign
                "title": item["name"],
                "score": score,
                "predicted_yield_pct": round(sim_res["predicted_yield"] * 100, 1),
                "yield_recovery_pct": sim_res["yield_delta_pct"],
                "confidence": sim_res["confidence"],
                "implementation_speed": item["speed"],
                "cost_estimate": sim_res["cost_estimate"],
                "effort": sim_res["implementation_effort"],
                "in_validated_range": sim_res["in_validated_range"],
                "business_impact": {
                    "monthly_financial_loss_avoided_usd": monthly_loss_avoided,
                    "downtime_avoided_hours": downtime_avoided_hours,
                    "downtime_savings_usd": downtime_savings,
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
