"""
What-If Simulation Engine for ZenOps (Role 3: Simulation & Data Engineer).
Implements run_scenario and compare_scenarios tool contracts adhering to ForgeOps Product Blueprint.
Evaluates input variables against validated operating ranges and operational constraints.
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

    def run_scenario(self, inputs: Dict[str, Any], scenario_name: str = None, constraints: Dict[str, Any] = None) -> Dict[str, Any]:
        scenario_id = f"sim_{uuid.uuid4().hex[:6]}"
        baseline_yield = self.incident_data["batch"]["yield_pct"] / 100.0  # 0.82 (82%)
        max_baseline_yield = self.incident_data["batch"]["baseline_yield_pct"] / 100.0  # 0.96 (96%)

        constraints = constraints or {}

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

        # Inputs & Interventions aligned with Blueprint Section 08
        queue_delay = inputs.get("queue_delay_minutes", 85.0)
        humidity = inputs.get("humidity_pct", 76.0)
        replace_m7 = inputs.get("replace_machine_7", False)
        recalibrate_m7 = inputs.get("recalibrate_machine_7", False)
        change_supplier = inputs.get("change_supplier", False)

        # Hard Constraint Checks (e.g. no supplier change for 1 month)
        if constraints.get("no_supplier_change", False) and change_supplier:
            return {
                "scenario_id": scenario_id,
                "scenario_name": scenario_name or "Constraint Violation Scenario",
                "inputs": inputs,
                "baseline_yield": baseline_yield,
                "predicted_yield": baseline_yield,
                "yield_delta_pct": 0.0,
                "confidence": 0.0,
                "cost_estimate": "N/A",
                "implementation_effort": "INFEASIBLE",
                "assumptions": ["Rejected due to hard constraint: Supplier change frozen for 30 days"],
                "in_validated_range": False,
                "warnings": ["Hard Constraint Violated: Supplier change is frozen."]
            }

        # Calculate exact blueprint counterfactual outcomes (Section 08 table)
        yield_recovery = 0.0
        cost_level = "low"
        effort_level = "low"
        assumptions = []

        if replace_m7:
            # Blueprint: "Replace Machine 7 -> 84% yield (small improvement)"
            yield_recovery += 0.02
            cost_level = "high"
            effort_level = "disruptive"
            assumptions.append("Machine 7 replaced with brand new CNC unit; root cause primary queue delay unaddressed")
        elif recalibrate_m7:
            yield_recovery += 0.05
            cost_level = "medium"
            effort_level = "medium"
            assumptions.append("Machine 7 spindle thermal drift recalibrated to nominal ±0.02mm")

        if queue_delay <= 60.0:
            # Blueprint: "Queue delay below 60 minutes -> 96% predicted yield"
            yield_recovery += 0.14
            effort_level = "low" if effort_level == "low" else effort_level
            assumptions.append("Queue delay reduced below 60 minutes via priority staging dispatch")

        if humidity <= 55.0:
            # Blueprint: "Humidity below 55% -> 96% predicted yield"
            yield_recovery += 0.14
            cost_level = "high" if cost_level == "high" else "medium"
            assumptions.append("Humidity reduced below 55% RH via staging desiccant climate unit")

        if change_supplier:
            yield_recovery += 0.03
            cost_level = "high"
            effort_level = "high"
            assumptions.append("Switched resin supplier (Requires 30-day qualification audit)")

        # Target yield capped at baseline target max (96% / 0.96)
        predicted_yield = min(max_baseline_yield, baseline_yield + yield_recovery)

        # Confidence score calculation
        confidence = 0.96 if in_validated_range else 0.65

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

    def compare_scenarios(self, scenario_list: List[Dict[str, Any]], constraints: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        results = []
        for sc in scenario_list:
            inputs = sc.get("inputs", {})
            name = sc.get("name", "Scenario")
            res = self.run_scenario(inputs, scenario_name=name, constraints=constraints)
            results.append(res)
        return results

if __name__ == "__main__":
    engine = SimulationEngine()
    
    # Test exact blueprint table from Section 08
    print("--- Blueprint Section 08 Simulation Matrix ---")
    sc1 = engine.run_scenario({"queue_delay_minutes": 55}, "Queue delay below 60 minutes")
    sc2 = engine.run_scenario({"humidity_pct": 50.0}, "Humidity below 55%")
    sc3 = engine.run_scenario({"replace_machine_7": True}, "Replace Machine 7")
    
    print(f"Queue Delay Scenario: {sc1['predicted_yield']*100}% yield (Expected: 96%)")
    print(f"Humidity Scenario: {sc2['predicted_yield']*100}% yield (Expected: 96%)")
    print(f"Replace Machine 7 Scenario: {sc3['predicted_yield']*100}% yield (Expected: 84%)")
