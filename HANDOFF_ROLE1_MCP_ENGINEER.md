# Handoff: Role 1 — MCP Agent Engineer (`Vishal` Branch)

## Overview
This document serves as the official handoff from **Role 1 (MCP Agent Engineer)** to **Role 2 (Frontend Workbench Engineer / Vaishak Branch)** and **Role 3 (Simulation Data Engineer / kv Branch)** for the **ForgeOps AI Decision Workbench**.

The MCP Server backend has been fully implemented using the **NitroStack TypeScript SDK (`@nitrostack/core`)** at `e:\ZenOps-1\forgeops-mcp`.

---

## 🛠 What Was Built

### 1. Framework & Server Setup
- **Framework**: Built with NitroStack TypeScript SDK using NestJS-style modular architecture (`@McpApp`, `@Module`, `@Tool`, `@Widget`) with **Zod** schema validation.
- **Location**: `e:\ZenOps-1\forgeops-mcp`
- **Transport**: Supports STDIO (for desktop MCP clients) and HTTP SSE / REST.

### 2. Domain Modules & MCP Tools (14 Tools Total)

| Domain Module | MCP Tool Name | Description | Key Inputs | Key Output Fields |
|---|---|---|---|---|
| **MES** | `get_batch_history` | Batch genealogy, route, timestamps, yield, material tracing | `batch_id` | `batch_id`, `yield_percent` (82%), `status`, `material_genealogy` |
| **MES** | `get_production_path` | Stage-by-stage cycle times, parameters, anomalies | `batch_id` | `stages[]`, `cycle_time_minutes`, `anomalies[]`, `failure_reason` |
| **MES** | `get_queue_events` | Queue wait times & delay anomalies | `batch_id`, `line_id` | `events[]`, `wait_time_minutes` (198 min), `severity` |
| **Maintenance** | `get_machine_alerts` | Machine vibration & temperature alerts | `machine_id` | `alerts[]`, `value`, `threshold`, `severity` |
| **Maintenance** | `get_maintenance_state` | Health score, service history, work orders | `machine_id` | `health_score` (72%), `service_history[]` |
| **Quality** | `get_defect_records` | Dimensional & surface defect measurements | `batch_id` | `defects[]`, `defect_class`, `measurements` |
| **Quality** | `get_inspection_results` | Inspection pass/fail criteria & scores | `batch_id` | `inspections[]`, `quality_score` (62.3), `criteria` |
| **Materials** | `get_supplier_lot_info` | Tata Steel lot specs & intake conditions | `lot_id` | `supplier_name`, `intake_conditions`, `storage_requirements` |
| **Materials** | `get_material_constraints` | Lead times, change freezes & alternatives | `material_type` | `lead_time_days`, `change_freeze_until`, `alternative_suppliers[]` |
| **Simulation** | `run_scenario` | Counterfactual simulation scenario runner | `scenario_name` | `predicted_yield`, `confidence`, `within_validated_range`, `warning` |
| **Simulation** | `compare_scenarios` | Side-by-side scenario comparison & deltas | `scenario_names` | `recommended_scenario`, `deltas[]`, `baseline` |
| **Orchestrator** | `get_incident_summary` | Executive summary of incident INC-2407-001 | `incident_id` | `title`, `kpi_change`, `causal_chain[]`, `status` |
| **Orchestrator** | `get_timeline` | Unified event timeline across all systems | `batch_id`, `filters` | `events[]` (ordered by timestamp) |
| **Orchestrator** | `get_causal_graph` | Root cause graph (nodes, edges, influence) | `batch_id` | `nodes[]`, `edges[]`, `influence`, `confidence` |
| **Orchestrator** | `get_recommendations` | Ranked action recommendations | `batch_id` | `recommendations[]`, `rank`, `cost`, `risk`, `evidence_refs[]` |
| **Orchestrator** | `get_business_impact` | Financial & operational impact analysis | `batch_id` | `monthly_loss_exposure_inr`, `monthly_savings_inr` |

---

## 🎯 Alignment with Role 3 (Simulation & Data)

Role 3's specifications (`03_Simulation_Data_Engineer.md`) have been **100% incorporated**:

1. **Golden-Path Dataset**: Pre-cached in `src/data/incident-data.ts` for **Batch B-2407-184** (Yield drop from 96% to 82% on Assembly Line 3 due to humidity → queue delay → Machine 7 vibration/temperature drift → quality failure).
2. **Provenance Traceability**: Every record returned by tools includes `source`, `record_id`, and ISO-8601 `timestamp`.
3. **Simulation Guardrails**:
   - `run_scenario` handles scenario names like `reduce_queue_delay`, `replace_machine_7`, `humidity_control`, `baseline`.
   - Fuzzy keyword resolution maps natural user phrasing.
   - Out-of-range scenarios explicitly set `within_validated_range: false` and return a safety warning.
4. **Ranking & Business Impact**: Exposes structured recommendation scoring (Yield, Confidence, Cost INR, Risk) and financial loss/savings metrics for leadership reports.

---

## 🤝 Integration Guide for Role 2 (Frontend Workbench Engineer)

Role 2 can consume this MCP server in two ways:

### Option A: Standard MCP SSE / REST Endpoint (NitroStack Server)
Run the server:
```bash
cd e:\ZenOps-1\forgeops-mcp
npm run dev
```
The server runs a dual-transport (STDIO + HTTP SSE / REST API) endpoint for tool calls.

### Option B: Direct TypeScript Module Import
Since `forgeops-mcp` is pure TypeScript, Role 2 can directly import the tool controllers or data provider:
```typescript
import { OrchestratorTools } from './forgeops-mcp/src/modules/orchestrator/orchestrator.tools.js';
import { SimulationTools } from './forgeops-mcp/src/modules/simulation/simulation.tools.ts';

const orchestrator = new OrchestratorTools();
const incident = await orchestrator.getIncidentSummary({});
const causalGraph = await orchestrator.getCausalGraph({});
const timeline = await orchestrator.getTimeline({});
```

---

## 🧪 Verification & Build Status

- **Unit/Integration Test Suite**: `npx tsx src/test-tools.ts`
  - **Result**: `Summary: 17 Passed, 0 Failed`
- **Build Verification**: `npm run build`
  - **Result**: `✓ Build Complete (TypeScript compiled & widgets bundled cleanly)`

---

## 🚀 Quick Commands

```bash
# 1. Install dependencies
cd e:\ZenOps-1\forgeops-mcp
npm install

# 2. Run verification test suite
npx tsx src/test-tools.ts

# 3. Build for production
npm run build

# 4. Start development server
npm run dev
```
