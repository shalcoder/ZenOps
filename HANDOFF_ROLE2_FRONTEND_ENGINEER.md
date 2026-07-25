# Handoff: Role 2 — Frontend Decision Workbench (`vaishak`)

## Role ownership

Role 2 owns the React/TypeScript visual product:

- Home Dashboard and incident navigation
- Shared synchronized workbench focus
- Incident Timeline and healthy-batch comparison
- Replay Production controls and pinned moments
- Root Cause Graph and evidence inspection
- What-if Simulator input/output experience
- Ranked recommendations and Business Impact
- Human approval gate and local decision record
- AI Engineer panel, evidence focus, MCP trace, and report preview

Role 2 does **not** own MCP server implementation, simulation physics, canonical backend persistence, or real production actions.

## Branch and build

- Local branch: `vaishak`
- Upstream branch: `origin/Vaishak`
- Frontend: Vite + React + TypeScript
- Install: `npm install`
- Develop: `npm run dev`
- Verify: `npm run build`

The application runs with deterministic golden-path fixtures if no backend is running. This is intentional for hackathon demo reliability.

## Canonical frontend demo identifiers

The visual demo follows the product blueprint and Role 1's implemented dataset:

- Incident: `INC-2407-001`
- Batch: `B-2407-184`
- Plant: `Plant Mumbai-1`
- Line: `Assembly Line 3`
- Baseline/current yield: `96% → 82%`
- Winning scenario: `sim:run_014`
- Winning causal node: `node_queue_delay`
- Winning event: `evt_2291`

Role 3's standalone `kv` fixture uses `BATCH-INC-2026-07`. Do not leak that identifier into UI components. Normalize it at the API boundary if the standalone Role 3 service becomes the incident source.

## Role 1 integration (`Vishal`)

The frontend accepts an optional Role 1 agent endpoint through:

```env
VITE_ROLE1_AGENT_URL=http://localhost:3000/api/agent/query
```

Request:

```json
{
  "intent": "evidence",
  "incident_id": "INC-2407-001",
  "batch_id": "B-2407-184"
}
```

Expected response fields:

```json
{
  "intent": "show_evidence",
  "conclusion": "Queue delay is the strongest controllable contributor.",
  "effect": "Reducing the wait below 60 minutes restores predicted yield from 82% to 96%.",
  "confidence": 0.96,
  "evidence_refs": ["timeline:evt_2291", "graph:node_queue_delay", "sim:run_014"],
  "assumptions": ["Machine 7 condition held constant"],
  "actions": ["open_evidence", "run_comparison", "generate_report"],
  "tool_trace": []
}
```

The adapter accepts either `evidence_refs` / `tool_trace` or camelCase equivalents. Role 1's current NitroStack handoff describes MCP/SSE tools but does not define a browser-safe agent query route. Keep the deterministic fallback until that HTTP route is exposed.

## Role 3 integration (`kv`)

The frontend can call the Role 3 Python REST service directly:

```env
VITE_ROLE3_API_URL=http://localhost:8080
```

Used route:

- `POST /api/simulate`

The adapter normalizes:

- Fractional or percentage yield values
- `in_validated_range` and `within_validated_range`
- Singular `warning` and plural `warnings`

Role 3 remains responsible for simulation calculations and operating-range enforcement. The frontend only presents the returned result and adds a visible UI warning for values outside the published handoff ranges.

## Merge boundaries

Recommended integration order on a temporary integration branch:

1. Merge `kv` for Role 3 data/simulation.
2. Merge `Vishal` for `forgeops-mcp/`.
3. Merge `Vaishak` for the frontend.
4. Resolve duplicate blueprint/task documents by keeping the newest shared copy.
5. Keep `forgeops-mcp/` owned by Role 1.
6. Keep Python simulation files and `data/` owned by Role 3.
7. Keep React `.tsx`, frontend CSS, Vite config, and browser adapters owned by Role 2.

Do not directly import NitroStack server classes into Vite browser code. Connect through an HTTP endpoint so server-only dependencies and secrets remain outside the frontend bundle.

## Evidence reference rule

All cross-module control uses namespaced references:

- `timeline:<event-id>`
- `graph:<node-id>`
- `sim:<run-id>`

Role 1 must return those references unchanged. The shared focus context resolves them into timeline selection, replay position, graph highlights, and evidence records.

## Demo verification path

1. Open the priority incident.
2. Select the humidity event.
3. Select the queue-delay event and verify replay, graph, and evidence synchronize.
4. Replay and pin the queue moment.
5. Select Machine 7 and inspect the replacement counterfactual.
6. Open **Decide** and run queue-delay reduction.
7. Confirm `82% → 96%`, assumptions, confidence, cost, and guardrails.
8. Review the queue-delay recommendation and Business Impact.
9. Open the human approval dialog and record the decision.
10. Ask the AI Engineer to show evidence, compare options, and generate the report.
11. Expand the MCP tool trace.

The golden path must remain usable manually if Role 1 or Role 3 is unavailable.
