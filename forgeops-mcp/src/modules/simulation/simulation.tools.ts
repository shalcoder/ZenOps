/**
 * ForgeOps — Simulation MCP Server Module
 *
 * Tools:
 *   - run_scenario: Run a counterfactual simulation scenario
 *   - compare_scenarios: Compare multiple scenarios side-by-side
 *
 * This module talks to Role 3's simulation engine.
 * For the hackathon, results are pre-computed but structured
 * as if they came from a real engine.
 */
import { ToolDecorator as Tool, ExecutionContext, z } from '@nitrostack/core';
import { SIMULATION_SCENARIOS } from '../../data/incident-data.js';

export class SimulationTools {

  /**
   * Resolve scenario by name, key, or fuzzy keyword match.
   */
  private resolveScenario(scenarioName: string): any | null {
    // Direct key match
    if (SIMULATION_SCENARIOS[scenarioName]) {
      return SIMULATION_SCENARIOS[scenarioName];
    }

    // Fuzzy match by common phrases
    const nameLower = scenarioName.toLowerCase();
    const mapping: Record<string, string> = {
      baseline: 'baseline',
      incident: 'baseline',
      current: 'baseline',
      queue: 'reduce_queue_delay',
      'reduce queue': 'reduce_queue_delay',
      'queue delay': 'reduce_queue_delay',
      machine: 'replace_machine_7',
      'replace machine': 'replace_machine_7',
      'machine 7': 'replace_machine_7',
      humidity: 'humidity_control',
      'humidity control': 'humidity_control',
      'install humidity': 'humidity_control',
    };

    for (const [keyword, key] of Object.entries(mapping)) {
      if (nameLower.includes(keyword)) {
        return SIMULATION_SCENARIOS[key];
      }
    }

    return null;
  }

  @Tool({
    name: 'run_scenario',
    description: 'Run a counterfactual simulation scenario with modified parameters. Returns predicted yield, confidence, assumptions, and warnings if the scenario is outside the validated operating range.',
    inputSchema: z.object({
      scenario_name: z.string().describe('Name or key for the scenario (e.g. "reduce_queue_delay", "replace_machine_7", "humidity_control", "baseline")'),
    }),
  })
  async runScenario(input: { scenario_name: string }, ctx: ExecutionContext) {
    ctx.logger.info('Simulation: Running scenario', { scenario_name: input.scenario_name });

    const result = this.resolveScenario(input.scenario_name);
    if (result) return result;

    // Guardrail: out-of-range warning for unknown scenarios
    return {
      source: 'simulation',
      record_id: 'sim:unknown',
      timestamp: new Date().toISOString(),
      scenario_name: input.scenario_name,
      predicted_yield: null,
      confidence: 0.0,
      within_validated_range: false,
      warning: `Scenario '${input.scenario_name}' is outside the validated operating range. Cannot provide a reliable prediction.`,
      model_version: 'forgeops-sim-v1.0',
    };
  }

  @Tool({
    name: 'compare_scenarios',
    description: 'Compare multiple simulation scenarios side-by-side with deltas against the baseline. Returns recommended scenario based on yield × confidence.',
    inputSchema: z.object({
      scenario_names: z.array(z.string()).describe('List of scenario names/keys to compare'),
    }),
  })
  async compareScenarios(input: { scenario_names: string[] }, ctx: ExecutionContext) {
    ctx.logger.info('Simulation: Comparing scenarios', { scenarios: input.scenario_names });

    const baseline = this.resolveScenario('baseline') || SIMULATION_SCENARIOS['baseline'];
    const scenarios: any[] = [];

    for (const name of input.scenario_names) {
      if (!['baseline', 'incident', 'current'].includes(name.toLowerCase())) {
        const s = this.resolveScenario(name);
        if (s) scenarios.push(s);
      }
    }

    // Compute deltas
    const deltas = scenarios.map((s) => ({
      scenario: s.scenario_name,
      yield_delta: s.predicted_yield - baseline.predicted_yield,
      confidence_delta: s.confidence - baseline.confidence,
    }));

    // Find recommended (best yield × confidence)
    const best = scenarios.length > 0
      ? scenarios.reduce((a, b) => (a.predicted_yield * a.confidence > b.predicted_yield * b.confidence ? a : b))
      : null;

    return {
      source: 'simulation',
      record_id: 'sim:comparison_001',
      timestamp: baseline.timestamp,
      comparison_id: 'sim:comparison_001',
      baseline,
      scenarios,
      recommended_scenario: best?.scenario_name ?? null,
      recommendation_reason: best
        ? `${best.scenario_name} provides the best balance of predicted yield (${best.predicted_yield}%) and confidence (${(best.confidence * 100).toFixed(0)}%)`
        : '',
      deltas,
    };
  }
}
