# Handoff Guide for Role 1: MCP & Agent Engineer (ZenOps / ForgeOps)

Hi Role 1! Role 3 (Simulation & Data Engineer) has prepared all the canonical data schemas, golden incident fixtures, rules-based diagnostic correlation engines, What-if Simulation contracts, recommendation rankers, and report generators for you.

Everything is pushed to the `kv` branch on GitHub:
👉 **[GitHub Branch `kv`](https://github.com/shalcoder/ZenOps/tree/kv)**

---

## 1. Quick Start for Role 1 (MCP Tool Integration)

You have **two super easy ways** to integrate Role 3's engine into your MCP Server:

### Option A: Direct Python Import (Recommended for Fast MCP Execution)
Import [`src/mcp_tool_adapter.py`](https://github.com/shalcoder/ZenOps/blob/kv/src/mcp_tool_adapter.py) directly into your Python MCP server code:

```python
from src.mcp_tool_adapter import (
    tool_run_scenario,
    tool_compare_scenarios,
    tool_get_incident_diagnostics,
    tool_get_ranked_recommendations
)

# 1. Run a What-if Simulation
# Pass input variables (e.g., queue_delay_minutes, recalibrate_machine_7, humidity_pct)
result_json_str = tool_run_scenario(
    inputs={"queue_delay_minutes": 30, "recalibrate_machine_7": True},
    scenario_name="Reduce Queue & Recalibrate M7"
)

# 2. Compare Multiple Scenarios
compare_json_str = tool_compare_scenarios([
    {"name": "Option A", "inputs": {"queue_delay_minutes": 30}},
    {"name": "Option B", "inputs": {"replace_machine_7": True}}
])

# 3. Get Anomaly & Diagnostic Correlation Pathway
diag_json_str = tool_get_incident_diagnostics(batch_id="BATCH-INC-2026-07")

# 4. Get Ranked Recommendations & Business Impact
recs_json_str = tool_get_ranked_recommendations()
```

---

### Option B: HTTP REST Endpoints (If your MCP Server calls HTTP APIs)
Start the lightweight built-in HTTP server:
```bash
python3 src/api_server.py 8080
```

Available Endpoints (`http://localhost:8080`):
- `GET /api/incident`: Returns full incident batch data (`BATCH-INC-2026-07`).
- `GET /api/reference`: Returns healthy baseline batch data (`BATCH-REF-2026-06`).
- `GET /api/diagnose`: Returns root cause pathways and anomalies.
- `POST /api/simulate`: Accepts `{"inputs": {"queue_delay_minutes": 30}, "constraints": {"no_supplier_change": true}}` and returns exact counterfactual predictions.
- `GET /api/recommendations`: Returns ranked decision cards with business financial impact.
- `GET /api/report/manager`: Returns executive summary report in Markdown & HTML.

---

## 2. MCP Simulation Tool Contract (Exact JSON Output Shape)

When your agent calls `run_scenario`, the engine returns this exact JSON schema contract:

```json
{
  "scenario_id": "sim_ba5bf2",
  "scenario_name": "Reduce Queue & Recalibrate M7",
  "inputs": {
    "queue_delay_minutes": 30,
    "recalibrate_machine_7": true
  },
  "baseline_yield": 0.82,
  "predicted_yield": 0.96,
  "yield_delta_pct": 14.0,
  "confidence": 0.96,
  "cost_estimate": "Medium",
  "implementation_effort": "Medium",
  "assumptions": [
    "Machine 7 spindle thermal drift recalibrated to nominal ±0.02mm",
    "Queue delay reduced below 60 minutes via priority staging dispatch"
  ],
  "in_validated_range": true,
  "warnings": []
}
```

> [!NOTE]
> **Operating Range Guardrail**: If an agent or user requests parameters outside calibrated bounds (e.g. `queue_delay_minutes = 150`), the engine sets `"in_validated_range": false` and populates the `"warnings"` array so your agent can alert the user.

---

## 3. Data Schema & Provenance Tags

Every record in [`data/incident_batch.json`](https://github.com/shalcoder/ZenOps/blob/kv/data/incident_batch.json) includes non-negotiable provenance tags:
- `source`: (e.g., `"MES_PROD_DB"`, `"SCADA_IOT_SENSORS"`, `"QUALITY_LAB"`)
- `record_id`: (e.g., `"REC-EVT-104"`)
- `timestamp`: ISO-8601 UTC timestamp

Your MCP tool servers for MES, Quality, Maintenance, and Sensors can serve directly from these canonical fixtures.

---

## 4. File Links on `kv` Branch

- 📦 **MCP Tool Adapter**: [`src/mcp_tool_adapter.py`](https://github.com/shalcoder/ZenOps/blob/kv/src/mcp_tool_adapter.py)
- ⚙️ **Simulation Engine**: [`src/simulation_engine.py`](https://github.com/shalcoder/ZenOps/blob/kv/src/simulation_engine.py)
- 🔍 **Diagnostic Engine**: [`src/diagnostic_engine.py`](https://github.com/shalcoder/ZenOps/blob/kv/src/diagnostic_engine.py)
- 📊 **Recommendation Engine**: [`src/recommendation_engine.py`](https://github.com/shalcoder/ZenOps/blob/kv/src/recommendation_engine.py)
- 🌐 **HTTP API Server**: [`src/api_server.py`](https://github.com/shalcoder/ZenOps/blob/kv/src/api_server.py)
- 📄 **Executive Report Generator**: [`src/report_generator.py`](https://github.com/shalcoder/ZenOps/blob/kv/src/report_generator.py)
- 📋 **Incident Dataset**: [`data/incident_batch.json`](https://github.com/shalcoder/ZenOps/blob/kv/data/incident_batch.json)
