"""
What-If Simulation Engine for ZenOps (Role 3: Simulation & Data Engineer).
Implements run_scenario and compare_scenarios tool contracts.
Evaluates input variables against validated operating ranges.
"""

import json
import os
import uuid
from typing import Dict, Any, List

class SimulationEngine:
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, "data")
        self.data_dir = data_dir
        with open(os.path.join(self.data_dir, "operating_ranges.json"), "r") as f:
            self.operating_ranges = json.load(f)
        with open(os.path.join(self.data_dir, "incident_batch.json"), "r") as f:
            self.incident_data = json.load(f)

    def run_scenario(self, inputs: Dict[str, Any], scenario_name: str = None) -> Dict[str, Any]:
        scenario_id = f"sim_{uuid.uuid4().hex[:6]}"
        baseline_yield = self.incident_data["batch"]["yield_pct"] / 100.0  # 0.82
        max_baseline_yield = self.incident_data["batch"]["baseline_yield_pct"] / 100.0  # 0.96

        # Check parameter bounds
        in_validated_range = True
        out_of_range_warnings = []

        for param_key, param_value in inputs.items():
            if param_key in self.operating_ranges:
                bounds = self.operating_ranges[param_key]
                if param_value < bounds["min_valid"] or param_value > bounds["max_valid"]:
                    in_validated_range = False
                    out_of_range_warnings.append(
                        f"{param_key}={param_value} is outside calibrated operating range ({bounds['min_valid']}-{bounds['max_valid']} {bounds['unit']})"
                    )

        # Calculate predicted yield based on deterministic physics model
        queue_delay = inputs.get("queue_delay_minutes", 85.0)
        humidity = inputs.get("humidity_pct", 76.0)
        recalibrate_m7 = inputs.get("recalibrate_machine_7", False)
        change_supplier = inputs.get("change_supplier", False)

        # Baseline impact factors
        yield_recovery = 0.0
        cost_level = "low"
        effort_level = "low"
        assumptions = []

        if recalibrate_m7:
            yield_recovery += 0.07
            cost_level = "medium"
            effort_level = "medium"
            assumptions.append("Machine 7 spindle thermal drift recalibrated to nominal ±0.02mm")

        if queue_delay <= 30.0:
            yield_recovery += 0.08
            effort_level = "low" if effort_level == "low" else effort_level
            assumptions.append("Queue delay reduced below 30 minutes via priority staging dispatch")
        elif queue_delay <= 60.0:
            yield_recovery += 0.05
            assumptions.append("Queue delay reduced to 60 minutes")

        if humidity <= 50.0:
            yield_recovery += 0.04
            cost_level = "medium" if cost_level == "low" else "high"
            assumptions.append("Desiccant dehumidification unit active in material staging area")

        if change_supplier:
            yield_recovery += 0.03
            cost_level = "high"
            effort_level = "high"
            assumptions.append("Switched resin supplier (Requires 30-day qualification audit)")

        # Target yield bounded by max baseline (0.96 or 96%)
        predicted_yield = min(max_baseline_yield, baseline_yield + yield_recovery)

        # Confidence calculation
        confidence = 0.90 if in_validated_range else 0.65

        if not assumptions:
            assumptions.append("No operational parameters modified; baseline scenario held constant")

        return {
            "scenario_id": scenario_id,
            "scenario_name": scenario_name or "Custom Scenario",
            "inputs": inputs,
            "baseline_yield": baseline_yield,
            "predicted_yield": round(predicted_yield, 2),
            "yield_delta_pct": round((predicted_yield - baseline_yield) * 100, 1),
            "confidence": confidence,
            "cost_estimate": cost_level,
            "implementation_effort": effort_level,
            "assumptions": assumptions,
            "in_validated_range": in_validated_range,
            "warnings": out_of_range_warnings
        }

    def compare_scenarios(self, scenario_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for sc in scenario_list:
            inputs = sc.get("inputs", {})
            name = sc.get("name", "Scenario")
            res = self.run_scenario(inputs, scenario_name=name)
            results.append(res)
        return results

if __name__ == "__main__":
    engine = SimulationEngine()
    
    # Test golden scenario 1: Reduce queue delay below 60 minutes
    sc1 = engine.run_scenario({"queue_delay_minutes": 30, "recalibrate_machine_7": True}, "Reduce Queue Delay & Recalibrate M7")
    print("--- Scenario 1 ---")
    print(json.dumps(sc1, indent=2))

    # Test out-of-range scenario: Extreme queue delay 150 minutes
    sc2 = engine.run_scenario({"queue_delay_minutes": 150}, "Extreme Queue Delay Out-of-Bounds Test")
    print("\n--- Scenario 2 (Out of Bounds Warning) ---")
    print(json.dumps(sc2, indent=2))
