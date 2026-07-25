# Plan 03: Recommendation Ranking & Reports Generator

## Purpose
Rank simulation interventions using multi-criteria weighted scoring, compute business financial/operational metrics, and generate executive & technical reports.

## Deliverables
1. `src/recommendation_engine.py`:
   - Scores actions across technical effectiveness, confidence, cost, speed, and operational effort.
   - Calculates financial ROI: Yield recovery %, Downtime avoided ($/hrs), Cost savings vs implementation cost.
2. `src/report_generator.py`:
   - Produces Markdown & HTML exports.
   - Engineer View: Full event log, sensor graphs data, causal scores, simulation parameters.
   - Manager View: Executive summary, root cause statement, top recommended intervention, ROI, decision record sign-off fields.
