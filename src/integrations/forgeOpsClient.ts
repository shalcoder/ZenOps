import { assistantResponses, simulationPresets } from '../mockData';
import type { AssistantResponse, SimulationResult } from '../types';

const apiBaseUrl = (
  import.meta.env.VITE_FORGEOPS_API_URL
  ?? import.meta.env.VITE_ROLE3_API_URL
  ?? ''
).replace(/\/$/, '');
const simulationUrl = `${apiBaseUrl}/api/simulate`;
const agentUrl = import.meta.env.VITE_ROLE1_AGENT_URL ?? `${apiBaseUrl}/api/agent/query`;

const toPercent = (value: number | undefined, fallback: number) => {
  if (value === undefined || Number.isNaN(value)) return fallback;
  return value <= 1 ? value * 100 : value;
};

type Role3SimulationPayload = {
  scenario_id?: string;
  scenario_name?: string;
  baseline_yield?: number;
  predicted_yield?: number;
  confidence?: number;
  cost_estimate?: string;
  implementation_effort?: string;
  assumptions?: string[];
  in_validated_range?: boolean;
  within_validated_range?: boolean;
  warnings?: string[];
  warning?: string | null;
};

export async function runScenario(
  scenarioKey: keyof typeof simulationPresets,
  inputs: Record<string, number | boolean>,
  constraints: Record<string, boolean>,
): Promise<SimulationResult> {
  const fallback = simulationPresets[scenarioKey] ?? simulationPresets.baseline;
  try {
    const response = await fetch(simulationUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: fallback.scenarioName, inputs, constraints }),
    });
    if (!response.ok) throw new Error(`Role 3 API returned ${response.status}`);
    const data = await response.json() as Role3SimulationPayload;
    const warnings = data.warnings ?? (data.warning ? [data.warning] : []);
    return {
      ...fallback,
      scenarioId: data.scenario_id ?? fallback.scenarioId,
      scenarioName: data.scenario_name ?? fallback.scenarioName,
      baselineYield: toPercent(data.baseline_yield, fallback.baselineYield),
      predictedYield: toPercent(data.predicted_yield, fallback.predictedYield),
      confidence: data.confidence ?? fallback.confidence,
      cost: data.cost_estimate ?? fallback.cost,
      effort: data.implementation_effort ?? fallback.effort,
      assumptions: data.assumptions ?? fallback.assumptions,
      inValidatedRange: data.in_validated_range ?? data.within_validated_range ?? fallback.inValidatedRange,
      warnings,
    };
  } catch (error) {
    return {
      ...fallback,
      warnings: [`Role 3 API unavailable; showing the deterministic handoff fixture. ${error instanceof Error ? error.message : ''}`.trim()],
    };
  }
}

export async function askAgent(intent: keyof typeof assistantResponses): Promise<AssistantResponse> {
  const fallback = assistantResponses[intent] ?? assistantResponses.evidence;
  try {
    const response = await fetch(agentUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ intent, incident_id: 'INC-2407-001', batch_id: 'B-2407-184' }),
    });
    if (!response.ok) throw new Error(`Role 1 agent returned ${response.status}`);
    const data = await response.json() as Partial<AssistantResponse>;
    return {
      ...fallback,
      ...data,
      evidenceRefs: data.evidenceRefs ?? (data as { evidence_refs?: string[] }).evidence_refs ?? fallback.evidenceRefs,
      toolTrace: data.toolTrace ?? (data as { tool_trace?: AssistantResponse['toolTrace'] }).tool_trace ?? fallback.toolTrace,
    };
  } catch (error) {
    return {
      ...fallback,
      effect: `${fallback.effect} Live MCP bridge unavailable; using the synchronized handoff fixture.`,
      assumptions: [
        ...fallback.assumptions,
        error instanceof Error ? error.message : 'MCP bridge unavailable',
      ],
    };
  }
}
