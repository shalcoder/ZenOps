# Plan 02: Simulation & Diagnostic Engine

## Purpose
Build the computational engine for incident analysis, anomaly detection, rules-based diagnostic correlation, and what-if simulation scenarios.

## Tool Contracts & Functions
1. `run_scenario(inputs, baseline_batch_id)`:
   - Evaluates input modifications (e.g. `{"queue_delay_minutes": 45}`).
   - Calculates predicted yield, confidence, cost estimate, implementation effort, and assumptions.
   - Performs check against `validated_operating_range` and returns `in_validated_range: boolean`.
2. `compare_scenarios(scenario_ids_or_inputs)`:
   - Comparative output matrix across multiple interventions.
3. `diagnose_incident(batch_id)`:
   - Evaluates correlated sensor spikes & event triggers (e.g., `queue_delay > threshold AND humidity > threshold`).
