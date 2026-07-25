**Product Blueprint**

# ForgeOps

*AI Decision Workbench for Smart Manufacturing*

A visual-first platform that helps manufacturing engineers diagnose incidents, replay production, simulate corrective actions, and make evidence-backed decisions with an MCP-orchestrated AI engineering copilot.

## Run the integrated application

ForgeOps now ships as one verified project: the React workbench calls a four-role FastAPI agent orchestrator, which uses NitroCloud's hosted model and the deployed NitroStack MCP server. The MCP exposes 16 read-only manufacturing and simulation tools.

Runtime note: Planner, Research, Analysis, and Execution are four isolated LLM calls coordinated by one backend process. They are agent roles, not four operating-system processes. The Research and Analysis roles call the live MCP; deterministic logic is retained only as an explicitly labelled degraded fallback.

```powershell
npm install
npm install --prefix forgeops-mcp
python -m pip install -r backend/requirements.txt
```

Start the bridge, agent orchestrator, and frontend in separate terminals:

```powershell
npm run dev:api
npm run dev:agents
npm run dev
```

Open `http://localhost:4173`. Vite sends `/api/agent` and `/api/audit` to the agent backend on port 8000 and the remaining `/api` routes to the bridge on port 8787. NitroCloud keeps its model gateway credential server-side, so this repository needs no OpenAI, Gemini, or Anthropic key.

Run the complete frontend, MCP-tool, and HTTP integration checks with:

```powershell
npm run verify
```

- **VISUAL FIRST<br>Workbench is the hero**
- **AGENTIC<br>Copilot coordinates tools**
- **DECISION READY<br>Evidence to action**

Comprehensive product concept, experience, architecture, and delivery plan

July 2026

*Section 01*

## Executive Summary

ForgeOps turns fragmented factory data into a guided, evidence-backed decision workflow.

> ONE-LINE PITCH
> ForgeOps is an AI-powered Decision Workbench that helps manufacturing engineers diagnose production issues, simulate corrective actions, and make evidence-backed decisions using agentic AI orchestrated through MCP.

### The idea in one sentence

The visual Decision Workbench is the product; the AI Engineer Assistant is the secondary interaction layer that explains, investigates, controls the workbench, and generates decision-ready outputs.

![Three-layer ForgeOps hierarchy: Decision Workbench, AI Engineer Assistant, and MCP orchestration.](ForgeOps_Product_Blueprint_assets/diagram-1.png)

### Why it matters

- Factory information is distributed across MES, ERP, quality, maintenance, sensor, PLC, and incident systems.
- Engineers currently spend valuable downtime correlating dashboards, spreadsheets, calls, and machine history.
- Traditional analytics explains what happened; ForgeOps helps evaluate what to do next.
- The product makes causal reasoning inspectable through timelines, replay, graphs, simulations, and evidence.
- MCP gives the AI assistant a meaningful orchestration role across manufacturing tools instead of reducing the experience to a generic chatbot.

### Product promise

| Item | Details |
| --- | --- |
| Diagnose | Reveal the sequence, relationships, and strongest causal contributors behind an incident. |
| Simulate | Test operational changes before applying them to a live production environment. |
| Decide | Rank options using confidence, yield, cost, effort, risk, and business impact. |
| Explain | Answer engineering questions with traceable evidence and visible workbench actions. |
| Communicate | Generate concise reports for plant managers and other stakeholders. |

*Section 02*

## Problem, Opportunity, and Product Positioning

The opportunity is not another manufacturing dashboard; it is a decision system that connects evidence to action.

### The operating problem

Modern plants generate abundant data, but that data is rarely organized around the decision an engineer must make during a production incident. When yield drops or a batch fails, teams search several systems, compare exports, contact maintenance, inspect historical records, and manually assemble a narrative.

| Current source | What it contains | Typical friction |
| --- | --- | --- |
| MES | Batch, routing, cycle, queue, and production events | Useful sequence data is isolated from quality and maintenance context. |
| ERP | Orders, materials, suppliers, cost, and inventory | Business constraints are separated from engineering analysis. |
| Quality | Defects, inspection results, rejects, and yield | Signals identify failure but not necessarily causal intervention. |
| Maintenance | Alerts, work orders, machine condition, and service history | Machine correlation can be mistaken for root cause. |
| IoT / PLC | Temperature, humidity, vibration, pressure, and state | High-volume signals are difficult to connect to batch outcomes. |
| Incident archive | Past investigations, actions, and reports | Knowledge is hard to retrieve and compare under time pressure. |

### Consequences of the fragmented workflow

- Diagnosis takes hours while production remains constrained or stopped.
- Teams overreact to correlated symptoms, such as replacing a machine that is not the primary cause.
- Corrective actions are selected without quantified trade-offs.
- Reports are produced after the fact and often omit the evidence chain.
- Institutional learning remains buried in systems and individual experience.

### Positioning

> CATEGORY STATEMENT
> ForgeOps is a manufacturing decision-making platform with an AI engineer embedded inside it - not a chat application with factory data attached.

### What ForgeOps is not

- Not an autonomous controller that changes production equipment without human authorization.
- Not a replacement for MES, ERP, QMS, CMMS, historians, or control systems.
- Not a black-box root-cause score with no supporting evidence.
- Not a chat-first interface that hides the factory state behind conversation.
*Section 03*

## Users, Jobs, and Decision Moments

ForgeOps serves the people who must understand an incident, choose an intervention, and defend the decision.

| User | Primary job | ForgeOps value |
| --- | --- | --- |
| Manufacturing engineer | Diagnose a failed batch and test corrective actions. | A visual investigation with evidence, simulation, and ranked options. |
| Process engineer | Understand process sensitivity and optimize operating parameters. | Counterfactual analysis across conditions and stages. |
| Quality engineer | Connect defects to upstream production conditions. | Traceable quality evidence and similar-incident comparison. |
| Maintenance engineer | Separate machine-related causes from process or material causes. | Maintenance history contextualized inside the causal chain. |
| Plant manager | Approve action based on throughput, cost, risk, and downtime. | Business impact and a concise executive report. |
| Operations leader | Find recurring causes across lines and plants. | Comparable incident history and standardized decision records. |

### Core jobs to be done

- When a production incident occurs, help me reconstruct what happened in the correct sequence.
- When several factors appear suspicious, help me distinguish correlation from causal influence.
- When I have operational constraints, help me find the best feasible intervention.
- When I recommend an action, help me show the evidence and expected outcome.
- When leadership asks for a summary, help me communicate the decision without recreating the investigation manually.

### Representative incident

Production yield falls from 96% to 82% on a batch. Humidity is elevated, queue delay increases, Machine 7 produces a maintenance alert, temperature drifts, defects appear, and the batch is rejected. The immediate question is not simply which event happened first; it is which intervention is most likely to restore yield with acceptable cost and disruption.

| Item | Details |
| --- | --- |
| Observed signals | Humidity rise, queue delay, Machine 7 alert, temperature drift, quality defects. |
| Candidate actions | Reduce queue delay, control humidity, replace Machine 7, change supplier, or alter process settings. |
| Constraint example | Supplier cannot be changed for one month. |
| Decision objective | Restore yield quickly while minimizing cost, downtime, and implementation risk. |

*Section 04*

## Experience Architecture

Engineers begin with the factory evidence, then use the copilot to deepen or accelerate the investigation.

### Primary experience

1. An incident appears on the Home Dashboard with severity, line, batch, and KPI change.
1. The engineer opens the incident in the Decision Workbench.
1. Replay Production reconstructs the manufacturing path and exposes the failure point.
1. The Incident Timeline and Root Cause Graph show the temporal and causal context.
1. The engineer tests interventions in the What-if Simulator.
1. The Recommendation Panel ranks feasible actions and shows the Business Impact.
1. The AI Engineer Assistant explains conclusions, opens evidence, runs additional analyses, or generates a report.

### Workbench composition

| Area | Purpose | Key interaction |
| --- | --- | --- |
| Incident Timeline | Reconstruct event order and context. | Select an event to synchronize every other view. |
| Replay Production | Animate the batch through each process stage. | Play, pause, scrub, change speed, and jump to anomalies. |
| Root Cause Graph | Show influence relationships and confidence. | Expand evidence and compare direct versus indirect factors. |
| What-if Simulator | Evaluate counterfactual operating scenarios. | Change parameters, apply constraints, and compare predicted outcomes. |
| Recommendation Panel | Turn analysis into ranked actions. | Inspect confidence, cost, effort, risk, evidence, and next steps. |
| Business Impact | Translate engineering outcomes into operational value. | Compare loss avoided, savings, downtime, yield, and throughput. |
| AI Engineer Assistant | Provide conversational control and explanation. | Ask, investigate, compare, highlight, simulate, and report. |

### Interaction principle

> Engineer
> "Show me the evidence."
>
> ForgeOps
> The assistant opens the replay timeline, focuses the dependency graph, displays the simulation comparison, and retrieves similar historical incidents. The answer is visible in the workbench, not only described in text.
*Section 05*

## Home Dashboard

The dashboard is the operational entry point: a concise view of plant performance and incidents that require decisions.

### Top-level production signals

| KPI | Example | Meaning |
| --- | --- | --- |
| Yield | 95.2% | Share of production meeting quality requirements. |
| OEE | 91% | Combined availability, performance, and quality effectiveness. |
| Open incidents | 3 | Events requiring investigation or corrective action. |
| Machine health | 89% | Aggregated equipment condition and risk indicator. |

### Recent alerts

- High humidity
- Conveyor delay
- Machine 7 vibration

### Recommended dashboard behavior

- Prioritize incidents by severity, financial exposure, and time since detection.
- Show the affected plant, line, product, batch, and current production state.
- Use a clear call to action: Open Decision Workbench.
- Keep global chat out of the main visual hierarchy; the assistant becomes prominent after an incident is opened.
- Allow filters for plant, line, shift, product, incident type, and status.

### Incident card

| Item | Details |
| --- | --- |
| Incident | Yield degradation - Batch B-2407-184 |
| Line | Assembly Line 3 |
| Detected | 08:47 |
| Change | Yield 96% to 82% |
| Severity | High |
| Primary action | Open Decision Workbench |

*Section 06*

## Incident Timeline and Replay Production

These modules rebuild the story of the batch before any recommendation is accepted.

### Module 1 - Incident Timeline

The Incident Timeline behaves like Git history for a production process. It aligns sensor changes, queue events, maintenance alerts, inspection results, operator notes, and system actions on one synchronized sequence.

| Item | Details |
| --- | --- |
| 08:31 | Humidity increased. |
| 08:38 | Queue delay started. |
| 08:42 | Machine 7 maintenance alert. |
| 08:47 | Quality defects detected. |
| 08:49 | Batch rejected. |

#### Timeline capabilities

- Filter events by source, stage, severity, or confidence.
- Select an event to highlight the related production stage, graph nodes, and evidence.
- Compare the incident timeline with a normal or successful batch.
- Show the provenance of every event: source system, timestamp, asset, and record identifier.

### Module 2 - Replay Production

> CORE FEATURE
> Replay Production is explicitly part of the ForgeOps workbench. It replays the entire manufacturing process like CCTV for production data.

When the engineer presses Replay, the workbench animates the selected batch through raw material intake, Machine A, Machine B, inspection, packaging, and the failure point. The replay synchronizes process state, sensor signals, wait time, maintenance events, and quality outcomes.

#### Replay controls

- Play, pause, restart, and scrub across the batch timeline.
- Change playback speed for overview or detailed inspection.
- Jump to anomalies, alerts, state changes, or quality failures.
- Overlay a healthy reference batch or a simulated counterfactual run.
- Select a stage to open its inputs, outputs, timestamps, sensor values, and evidence.
- Pin a moment so the root-cause graph and copilot remain anchored to the same context.

#### Production path example

| Stage | Replay signal | Observed issue |
| --- | --- | --- |
| Raw material | Supplier lot and intake conditions | No critical anomaly. |
| Machine A | Cycle time and process parameters | Within expected range. |
| Queue | Wait time before Machine B | Delay exceeds 3 hours. |
| Machine B / 7 | State, temperature, and vibration | Alert present; causal role uncertain. |
| Inspection | Defect class and quality score | Defects detected. |
| Packaging | Batch disposition | Batch rejected. |

#### Why replay is essential

A replay gives engineers a shared, inspectable reconstruction of the incident. It prevents the analysis from becoming a collection of disconnected charts and makes later causal claims easier to challenge, explain, and trust.

*Section 07*

## Root Cause Graph and Evidence

ForgeOps represents a causal hypothesis as a navigable graph, with every relationship tied to evidence.

### Module 3 - Root Cause Graph

The graph shows how operating conditions, delays, equipment behavior, materials, and environmental variables influence one another and contribute to the observed quality failure.

> EXAMPLE CAUSAL CHAIN
> Humidity → Queue Delay → Temperature Drift → Quality Failure

### Visual encoding

| Item | Details |
| --- | --- |
| Node size | Relative influence on the target outcome. |
| Node color | Confidence or evidence quality. |
| Edge strength | Estimated strength of the relationship. |
| Edge direction | Proposed direction of influence. |
| Halo / glow | Current selection or AI-highlighted evidence. |
| Badge | Data source, anomaly, controllability, or constraint. |

### Evidence behavior

- Every node opens supporting records, feature history, incident comparisons, and simulation results.
- The interface distinguishes observed correlation, model-estimated influence, and counterfactual evidence.
- Confidence should reflect data quality, model certainty, sample coverage, and cross-source consistency.
- Engineers can hide weak links, expand indirect paths, or compare the graph before and after a simulated intervention.
- User annotations and accepted conclusions are stored with the incident decision record.

### Explainability example

> Engineer
> "Why was Machine 7 ruled out?"
>
> ForgeOps
> Machine 7 appeared in 81% of failed batches, but counterfactual replay showed that replacing the machine alone still resulted in failures. When queue delay was reduced below 3 hours while keeping Machine 7 unchanged, the batch passed in 92.8% of simulated scenarios. This indicates that queue delay had a stronger causal influence than machine selection.

### Guardrail

ForgeOps should avoid claiming certainty that the evidence cannot support. Recommendations must display assumptions, confidence, data gaps, and the distinction between model output and verified plant knowledge.

*Section 08*

## What-if Simulator

The simulator converts diagnosis into decision support by testing the effect of specific interventions.

### Module 4 - What-if Simulator

Engineers adjust controllable variables or describe an operational constraint in natural language. ForgeOps retrieves the required context, runs a rules-based or model-based simulation, and compares the predicted outcome with the incident baseline.

| Scenario | Predicted yield | Interpretation |
| --- | --- | --- |
| Incident baseline | 82% | Observed degraded outcome. |
| Humidity below 55% | 96% | Strong recovery if environmental control is feasible. |
| Replace Machine 7 | 84% | Small improvement; machine is unlikely to be the primary driver. |
| Queue delay below 60 minutes | 96% | High recovery with low operational disruption. |

### Simulation inputs

- Environmental variables: humidity, temperature, pressure, or contamination level.
- Process variables: dwell time, queue delay, cycle time, setpoint, speed, or routing.
- Equipment choices: machine, tool, maintenance state, or line assignment.
- Material choices: supplier, lot, formulation, or storage condition.
- Operational constraints: change freeze, available labor, maintenance window, cost ceiling, or delivery commitment.

### Simulation output contract

| Item | Details |
| --- | --- |
| Outcome | Predicted yield, defect rate, throughput, downtime, or other target KPI. |
| Uncertainty | Confidence interval or probability distribution, not only a point estimate. |
| Assumptions | Conditions held constant and data substitutions used. |
| Coverage | Relevant batches, date range, line, product family, and operating envelope. |
| Sensitivity | Variables with the greatest influence on the predicted result. |
| Comparison | Baseline, candidate scenarios, deltas, cost, effort, and risk. |

### Decision support example

> Engineer
> "We cannot change suppliers for another month. What should we do?"
>
> ForgeOps
> Based on the simulations, reducing queue delay below 60 minutes increases predicted yield from 82% to 96% with minimal operational disruption. Installing humidity control achieves slightly better yield but has a much higher implementation cost.
*Section 09*

## Recommendations and Business Impact

A ForgeOps recommendation is a decision card with evidence, trade-offs, and executable next steps.

### Module 5 - Recommendation Panel

The Recommendation Panel ranks feasible interventions rather than stopping at “root cause detected.” Recommendations are compared across technical effectiveness, confidence, cost, speed, operational effort, and business impact.

| # | Action | Conf. | Yield | Cost | Implementation | Impact |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Reduce queue delay | 96% | 96% | Low | Easy / ~2 hours | High |
| 2 | Install humidity control | 94% | 97% | High | Medium | High |
| 3 | Replace Machine 7 | 61% | 84% | High | Disruptive | Low |

### Decision card

| Item | Details |
| --- | --- |
| Recommended action | Reduce queue delay. |
| Confidence | 96%. |
| Expected yield | 96%. |
| Cost | Low. |
| Time | Approximately 2 hours. |
| Estimated savings | INR 4.2 lakh per week. |
| Evidence | 327 historical batches, simulation output, maintenance history, and quality reports. |
| Actions | Run again, generate report, notify manager. |

### Module 6 - Business Impact

The Business Impact view translates an engineering choice into the outcomes plant leadership cares about. Every estimate should expose its basis and confidence.

| Measure | If nothing changes | If recommendation is applied |
| --- | --- | --- |
| Monthly loss exposure | INR 18 lakh | Reduced by approximately INR 15 lakh |
| Downtime | Current incident trajectory | 41% reduction |
| Yield | 82% | Approximately 96% |
| Yield improvement | - | 14 percentage points |

### Human approval

> DECISION OWNERSHIP
> ForgeOps recommends and explains. The engineer or authorized manager approves any operational action.

*Section 10*

## AI Engineer Assistant

The assistant is an engineering copilot embedded in the workbench, not a separate generic chatbot.

### What the copilot does

- Explains why a factor was included, deprioritized, or ruled out.
- Translates a question into a sequence of MCP tool calls and analysis steps.
- Controls the workbench by opening views, highlighting events, filtering evidence, and comparing scenarios.
- Runs simulations and presents assumptions, uncertainty, and trade-offs.
- Retrieves historical incidents and maintenance or quality records.
- Generates engineer-facing and manager-facing reports.

### Interaction patterns

| Engineer request | Assistant response | Workbench action |
| --- | --- | --- |
| Why was Machine 7 ruled out? | Explains counterfactual evidence and relative causal influence. | Highlights Machine 7, queue delay, and the relevant simulations. |
| Compare Option A and Option B. | Summarizes KPI, cost, effort, risk, and confidence trade-offs. | Opens a side-by-side scenario comparison. |
| Show me the evidence. | Lists the strongest supporting and contradicting evidence. | Opens timeline, graph, simulations, and similar incidents. |
| We cannot change suppliers. | Treats the constraint as a hard filter and finds feasible alternatives. | Updates the scenario set and recommendation ranking. |
| Generate a report for the plant manager. | Creates a concise executive narrative. | Packages incident summary, evidence, recommendation, impact, and risk. |

### Response design

- Lead with the conclusion and quantify the expected effect.
- Name the evidence and make it clickable or visibly highlighted.
- State assumptions, confidence, and meaningful alternatives.
- Offer context-relevant actions such as Run comparison, Open evidence, or Generate report.
- Keep conversational responses concise because the workbench carries the detailed evidence.

### Permission boundaries

The assistant may query connected systems, run simulations, change the local analysis view, and draft outputs. Actions that affect production, maintenance schedules, procurement, or external communication require explicit approval and role-based authorization.

*Section 11*

## MCP Architecture and Agent Workflow

MCP is the orchestration fabric that lets one engineering question become a coordinated, inspectable investigation.

![Flow from engineer question to ForgeOps Copilot, MCP tools, recommendation, and visible workbench response.](ForgeOps_Product_Blueprint_assets/diagram-2.png)

### MCP server landscape

| MCP server | Representative tools | Decision contribution |
| --- | --- | --- |
| MES | Get batch genealogy, route, cycle time, queue delay, and production events. | Reconstructs what happened and when. |
| ERP | Get material, supplier, order, cost, and inventory constraints. | Adds feasibility and business context. |
| Maintenance | Get alerts, work orders, condition history, and service records. | Tests equipment-related hypotheses. |
| Quality | Get inspections, defect classes, rejects, and yield history. | Defines the outcome and supporting evidence. |
| Inventory | Get available materials, parts, and lead times. | Constrains recommended actions. |
| IoT sensors | Get time-series conditions and anomalies. | Supplies environmental and equipment signals. |
| Knowledge base | Search SOPs, incident reports, and engineering guidance. | Adds institutional knowledge and policy context. |
| Simulation engine | Run counterfactuals, sensitivity tests, and comparisons. | Estimates the effect of interventions. |

### Agent workflow: compare two options

1. Interpret the decision question, requested options, target KPI, and constraints.
1. Retrieve production history from the MES MCP server.
1. Retrieve relevant maintenance records and machine condition.
1. Retrieve quality outcomes and defect patterns.
1. Retrieve material, cost, or availability constraints when relevant.
1. Run both scenarios through the Simulation Engine.
1. Combine results into a comparable decision model.
1. Display the result in the workbench and explain the recommendation.

### Traceability requirement

Every agent run should produce an audit trail containing the question, selected tools, query parameters, retrieved record references, simulation version, assumptions, outputs, and user decision. This turns agentic behavior into an inspectable workflow suitable for industrial environments.

*Section 12*

## Data, Models, and Trust

The strongest ForgeOps demo is credible because the evidence chain is visible and the model boundaries are explicit.

### Canonical data model

| Entity | Key attributes | Relationships |
| --- | --- | --- |
| Incident | ID, plant, line, severity, start/end, status, target KPI | Contains events, hypotheses, simulations, decisions, and reports. |
| Batch | Product, lot, route, timestamps, material genealogy | Moves through process stages and produces quality outcomes. |
| Asset | Machine, component, condition, maintenance state | Participates in stages and emits events. |
| Event | Timestamp, source, type, value, severity, provenance | Appears on timeline and may support a graph node. |
| Evidence | Source record, confidence, coverage, contradiction | Supports or weakens a hypothesis or recommendation. |
| Scenario | Intervention, fixed variables, constraints, model version | Produces simulated outcomes. |
| Recommendation | Action, confidence, impact, cost, effort, risk | Compares scenarios and records approval. |

### Analytical layers

- Descriptive: reconstruct the incident using synchronized production and sensor events.
- Diagnostic: detect anomalies, correlations, and candidate causal paths.
- Counterfactual: estimate outcomes under specific interventions.
- Prescriptive: rank actions using technical and business objectives.
- Communicative: explain the evidence and produce stakeholder-ready outputs.

### Trust and safety controls

- Provenance: every claim links to a source record or simulation result.
- Uncertainty: confidence and model limitations are visible.
- Human authority: operational changes require approval.
- Role-based access: plant and system permissions are respected.
- Auditability: tool calls and decisions are recorded.
- Data quality: missing, stale, or conflicting inputs are flagged.
- Simulation scope: the system warns when a scenario is outside the validated operating range.

### Model strategy for a hackathon

A credible prototype can combine deterministic rules, historical comparisons, and a lightweight simulation model. The LLM should orchestrate tools and explain results; it should not fabricate sensor values, causal scores, or simulation outcomes.

*Section 13*

## Reports, Notifications, and Decision Records

ForgeOps converts an investigation into an artifact that can be reviewed, approved, and learned from.

### Executive report contents

- Incident summary: what failed, where, when, and how performance changed.
- Root cause: the strongest causal explanation and relevant contributing factors.
- Evidence: timeline events, graph relationships, records, and historical comparison.
- Simulation: tested scenarios, assumptions, uncertainty, and predicted outcomes.
- Recommended action: the ranked intervention and why it is preferred.
- Business impact: expected yield, downtime, cost, savings, and loss avoided.
- Risk assessment: implementation risk, residual risk, and monitoring plan.
- Decision record: approver, selected action, timestamp, and follow-up ownership.

### Audience-specific output

| Audience | Emphasis | Format |
| --- | --- | --- |
| Engineer | Detailed evidence, parameter changes, assumptions, and simulation comparison. | Technical investigation report. |
| Plant manager | Recommended action, confidence, downtime, yield, cost, and risk. | One- to two-page executive summary. |
| Quality / compliance | Traceability, inspection records, deviations, and corrective action. | Controlled incident record. |
| Operations leadership | Recurring patterns, cross-line impact, and portfolio of actions. | Periodic management report. |

### Notification actions

The decision card may offer Notify Manager, create a maintenance task, or export a report. These are external actions and should always show the recipient, content, and affected system before the user confirms.

*Section 14*

## Visual and Interaction Design

The interface should feel like a professional industrial analysis environment, with AI attention expressed through context rather than spectacle.

### Visual language

| Item | Details |
| --- | --- |
| Theme | Dark industrial workspace with restrained contrast. |
| Primary color | Industrial blue for navigation, active analysis, and trusted information. |
| Alert color | Orange for anomalies, warnings, and AI-directed attention. |
| Positive state | Green for successful outcomes and approved recovery scenarios. |
| Critical state | Red for rejected batches, severe incidents, and high risk. |
| Motion | Purposeful timeline and replay animation; never decorative or distracting. |

### AI highlights

When the assistant explains a factor, the relevant workbench regions glow or focus. For example, “Show humidity evidence” highlights the humidity event on the timeline, the humidity node in the graph, and the matching sensor chart. The visual response should remain until the user dismisses it or asks a new question.

### Usability requirements

- Preserve the engineer's context when opening evidence or changing views.
- Use synchronized selection across replay, timeline, graph, and charts.
- Make baseline versus simulated data visually distinct.
- Provide keyboard access and high-contrast alternatives for graph and alert colors.
- Avoid overwhelming the user with every data source at once; reveal detail progressively.
- Display loading, tool progress, partial data, and failure states transparently.
*Section 15*

## Hackathon Demo Story

A seven-minute narrative should make the workbench memorable and reveal MCP only after the product value is clear.

| Time | Beat | What happens | Judge takeaway |
| --- | --- | --- | --- |
| 0:00-0:30 | Introduction | “Yesterday, production yield dropped from 96% to 82%.” | A concrete operational problem. |
| 0:30-1:10 | Incident | Open the dashboard and select the new high-severity incident. | Immediate context and urgency. |
| 1:10-2:00 | Replay | Replay Production and pause at the queue delay and failure point. | The audience sees the incident unfold. |
| 2:00-2:45 | Root cause | Open the graph; humidity and queue delay stand out. | Relationships are visible, not hidden in chat. |
| 2:45-3:45 | Simulation | Test reduced queue delay and replacing Machine 7. | Counterfactual evidence separates cause from correlation. |
| 3:45-4:30 | Recommendation | Show ranked action, confidence, cost, effort, and impact. | Analysis becomes a decision. |
| 4:30-5:20 | Copilot | Ask “Why not Machine 7?” and “Show me the evidence.” | AI explains and controls the workbench. |
| 5:20-6:10 | MCP reveal | Show MES, Quality, Maintenance, Sensors, and Simulation orchestration. | Agentic integration is meaningful. |
| 6:10-7:00 | Report | Generate the plant-manager report and close on the product statement. | The investigation becomes an actionable record. |

### Closing line

> DEMO CLOSE
> ForgeOps is not another chat app with manufacturing data. It is a decision-making platform with an AI engineer built into it.

### Demo reliability

- Use a deterministic incident dataset and cached MCP responses for the critical path.
- Precompute simulation results but still expose the agent's tool sequence.
- Keep a manual navigation fallback if a copilot action fails.
- Show the workbench first; reveal the architecture only after the recommendation is understood.
*Section 16*

## Technical Architecture and Stack

The implementation separates the visual workbench, orchestration layer, manufacturing connectors, and simulation services.

| Layer | Recommended technology | Responsibility |
| --- | --- | --- |
| Frontend | React + TypeScript | Workbench state, synchronized views, copilot actions, and reporting workflow. |
| Styling | Tailwind CSS | Industrial visual system and responsive layout. |
| Graphs | React Flow or D3.js | Root-cause and dependency visualization. |
| Charts | Recharts | KPI trends, scenario comparisons, and sensor evidence. |
| Backend API | FastAPI | Incident APIs, orchestration endpoints, security, and report generation. |
| Agent | OpenAI Agents SDK or LangGraph | Planning, MCP tool use, tool sequencing, and response synthesis. |
| Model | A current tool-capable GPT model | Question interpretation, orchestration, explanation, and report drafting. |
| Protocol | MCP | Standardized tool access to plant and simulation systems. |
| Operational data | PostgreSQL | Incidents, entities, decisions, permissions, and audit records. |
| Knowledge retrieval | ChromaDB or equivalent vector store | Historical incidents, SOPs, and engineering knowledge. |
| Cache | Redis (optional) | Tool result caching, session state, and long-running job coordination. |
| Simulation | Python rules or ML-based engine | Counterfactual and sensitivity analysis. |
| Authentication | Clerk or Auth.js (optional for demo) | Identity and role-based access. |

### Suggested service boundaries

- Workbench API: incidents, timeline, graph, evidence, and view state.
- Agent service: intent, orchestration plan, MCP calls, summaries, and action messages.
- Simulation service: scenario validation, execution, uncertainty, and comparison.
- Connector layer: MCP servers that adapt source-specific schemas into stable tool contracts.
- Reporting service: report templates, charts, exports, and approval records.
- Audit service: tool traces, evidence provenance, model versions, decisions, and access events.
*Section 17*

## MVP Scope, Roadmap, and Success Measures

The MVP should prove the end-to-end decision loop before expanding to live plant integration.

### Hackathon MVP

| Capability | MVP definition | Proof in demo |
| --- | --- | --- |
| Dashboard | One plant, one line, several KPI cards, and three incidents. | Open the featured yield incident. |
| Timeline | Five to ten synchronized incident events. | Select humidity, queue, machine, and defect events. |
| Replay Production | Animated six-stage batch journey with controls. | Pause at queue delay and failure point. |
| Root Cause Graph | Four to seven causal nodes with confidence and evidence drawer. | Compare queue delay with Machine 7. |
| What-if Simulator | Three deterministic or lightweight model scenarios. | Show 82% baseline, 96% queue scenario, and 84% machine scenario. |
| Recommendations | Ranked decision cards with cost, effort, and impact. | Select reduce queue delay. |
| Copilot | Four scripted but tool-backed intents. | Explain, compare, show evidence, and generate report. |
| MCP | At least three data servers plus the simulation server. | Show the orchestrated tool trace. |
| Report | Plant-manager summary generated from the incident state. | Export or preview the report. |

### Roadmap

| Phase | Focus | Key outcomes |
| --- | --- | --- |
| Phase 1 - Demo | Coherent story and deterministic evidence. | End-to-end workbench, MCP orchestration, and report. |
| Phase 2 - Pilot | Read-only connection to one production line. | Live incident ingestion, user roles, audit trail, and validated simulations. |
| Phase 3 - Scale | Multiple lines, products, and incident types. | Reusable schemas, model monitoring, cross-plant learning, and workflow integrations. |
| Phase 4 - Operationalize | Controlled action workflows. | Approved tasks, closed-loop outcome tracking, and continuous recommendation evaluation. |

### Success metrics

- Median time from incident detection to an evidence-backed recommendation.
- Percentage of recommendations with complete provenance and visible assumptions.
- Engineer agreement with the top-ranked action and reason for overrides.
- Simulation calibration: predicted versus observed outcome after an action.
- Reduction in manual investigation and report-preparation time.
- Yield recovery, downtime avoided, and loss avoided for supported incidents.
- User adoption of Replay Production, evidence drill-down, and scenario comparison.

### Key risks and mitigations

| Risk | Why it matters | Mitigation |
| --- | --- | --- |
| False causal confidence | A persuasive graph may overstate what the data proves. | Label evidence type, show uncertainty, and require engineering review. |
| Poor data quality | Clock drift, missing records, and inconsistent identifiers weaken reconstruction. | Validate timestamps, flag gaps, and normalize source schemas. |
| Simulation misuse | Scenarios outside the trained or validated range may be unreliable. | Show coverage, assumptions, and out-of-range warnings. |
| Integration fragility | Source systems may be slow or unavailable. | Cache read-only data, expose partial results, and provide retry/fallback states. |
| Automation risk | An agent could trigger unintended operational actions. | Default to read-only tools and require explicit approvals for mutations. |
| Demo complexity | Too many modules can obscure the core story. | Use one incident, one primary recommendation, and one strong counterfactual. |

*Section 18*

## Final Product Narrative

ForgeOps gives manufacturing teams a new way to move from scattered signals to a defensible operational decision.

An engineer should not have to choose between a visual dashboard that cannot reason and an AI chat experience that hides the evidence. ForgeOps combines both in the correct hierarchy: the Decision Workbench makes the factory state, replay, causal model, simulations, recommendations, and business impact visible; the AI Engineer Assistant helps the user interrogate and operate that environment.

Replay Production is central to that story. It reconstructs the batch in time and space, giving the team a shared starting point before causal claims or recommendations are made. The Root Cause Graph organizes hypotheses, the What-if Simulator tests interventions, and the Recommendation Panel turns the result into a practical choice.

MCP makes the assistant an authentic orchestrator. One question can retrieve MES history, quality outcomes, maintenance records, material constraints, sensor signals, and simulation results, while the workbench shows exactly how those inputs support the recommendation.

> PRODUCT THESIS
> Visual Workbench first. AI Copilot second. Evidence throughout. Human decision authority always.

### The memorable demo promise

ForgeOps helps an engineer see what happened, understand why it happened, test what could change the outcome, choose the best feasible action, and explain that decision to everyone who needs to trust it.

### Recommended next build step

Build the single-incident vertical slice first: Dashboard → Replay Production → Root Cause Graph → What-if Simulator → Recommendation → Copilot explanation → MCP reveal → Executive report. This sequence demonstrates the product, the agent, and the architecture without allowing any one component to become the entire experience.
