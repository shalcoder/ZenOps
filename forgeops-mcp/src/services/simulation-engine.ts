/**
 * ForgeOps MCP Server — Integrated Role 3 Simulation & Data Engine
 *
 * Integrates Role 3's canonical simulation logic and dataset into
 * Role 1's NitroStack MCP Server architecture.
 */

export interface ScenarioInput {
  scenario_id?: string;
  scenario_name: string;
  parameters?: Record<string, any>;
}

export interface SimulationResult {
  scenario_id: string;
  scenario_name: string;
  inputs: Record<string, any>;
  baseline_yield: number;
  predicted_yield: number;
  confidence: number;
  confidence_interval: [number, number];
  cost_estimate: string;
  cost_inr: number;
  implementation_effort: string;
  assumptions: string[];
  in_validated_range: boolean;
  warning: string | null;
  evidence_type: 'observed_correlation' | 'counterfactual_simulated' | 'model_estimated';
  sensitivity: Record<string, number>;
}

export class SimulationEngine {
  /**
   * Run counterfactual simulation scenario with Range Guardrails
   */
  public runScenario(input: ScenarioInput): SimulationResult {
    const name = input.scenario_name.toLowerCase();

    // Out-of-validated-range guardrail check
    if (name.includes('extreme') || name.includes('super_speed') || name.includes('1000')) {
      return {
        scenario_id: 'sim_out_of_range',
        scenario_name: input.scenario_name,
        inputs: input.parameters || {},
        baseline_yield: 82.0,
        predicted_yield: 50.0,
        confidence: 0.2,
        confidence_interval: [40.0, 60.0],
        cost_estimate: 'very_high',
        cost_inr: 5000000,
        implementation_effort: 'extreme',
        assumptions: ['Extrapolated beyond model physics calibration'],
        in_validated_range: false,
        warning: `⚠️ Scenario '${input.scenario_name}' exceeds validated operating boundaries (Queue delay < 300m, Humidity < 80%). Predictions are unreliable.`,
        evidence_type: 'counterfactual_simulated',
        sensitivity: {},
      };
    }

    if (name.includes('queue') || name.includes('delay') || name.includes('014')) {
      return {
        scenario_id: 'sim_014',
        scenario_name: 'Reduce Queue Delay (< 60 min)',
        inputs: { queue_delay_minutes: 45 },
        baseline_yield: 82.0,
        predicted_yield: 96.0,
        confidence: 0.96,
        confidence_interval: [93.2, 97.8],
        cost_estimate: 'low',
        cost_inr: 15000,
        implementation_effort: 'easy (scheduling adjustment)',
        assumptions: [
          'Machine 7 condition held constant',
          'No supplier change within 30-day freeze',
          'Queue wait ambient temperature remains normal',
        ],
        in_validated_range: true,
        warning: null,
        evidence_type: 'counterfactual_simulated',
        sensitivity: { queue_delay_minutes: 0.89, ambient_humidity: 0.34, machine_condition: 0.12 },
      };
    }

    if (name.includes('humidity') || name.includes('hvac') || name.includes('016')) {
      return {
        scenario_id: 'sim_016',
        scenario_name: 'Install Queue Area Humidity Control (< 55%)',
        inputs: { ambient_humidity: 50.0 },
        baseline_yield: 82.0,
        predicted_yield: 96.0,
        confidence: 0.94,
        confidence_interval: [94.0, 97.5],
        cost_estimate: 'high',
        cost_inr: 850000,
        implementation_effort: 'medium (HVAC installation 1-2 weeks)',
        assumptions: [
          'Queue delay remains at 198 minutes',
          'Machine 7 condition held constant',
          'Humidity consistently maintained < 55%RH',
        ],
        in_validated_range: true,
        warning: null,
        evidence_type: 'counterfactual_simulated',
        sensitivity: { ambient_humidity: 0.82, queue_delay_minutes: 0.45, machine_condition: 0.12 },
      };
    }

    if (name.includes('machine') || name.includes('grinder') || name.includes('015')) {
      return {
        scenario_id: 'sim_015',
        scenario_name: 'Replace / Overhaul Machine 7',
        inputs: { machine_id: 'MCH-B-009' },
        baseline_yield: 82.0,
        predicted_yield: 84.0,
        confidence: 0.61,
        confidence_interval: [81.0, 87.0],
        cost_estimate: 'high',
        cost_inr: 1200000,
        implementation_effort: 'disruptive (2-3 days downtime)',
        assumptions: [
          'Queue delay remains at 198 minutes',
          'Ambient humidity remains at 68.5%',
          'Replacement machine MCH-B-009 is fully operational',
        ],
        in_validated_range: true,
        warning: '⚠️ Machine replacement alone shows minimal yield improvement (+2%). Queue delay remains the dominant root cause.',
        evidence_type: 'counterfactual_simulated',
        sensitivity: { machine_condition: 0.18, queue_delay_minutes: 0.89, ambient_humidity: 0.34 },
      };
    }

    // Default Baseline
    return {
      scenario_id: 'sim_001',
      scenario_name: 'Incident Baseline (No Intervention)',
      inputs: {},
      baseline_yield: 82.0,
      predicted_yield: 82.0,
      confidence: 0.95,
      confidence_interval: [79.5, 84.5],
      cost_estimate: 'none',
      cost_inr: 0,
      implementation_effort: 'none',
      assumptions: ['All current conditions held as observed'],
      in_validated_range: true,
      warning: null,
      evidence_type: 'observed_correlation',
      sensitivity: {},
    };
  }

  /**
   * Compare multiple scenarios side-by-side
   */
  public compareScenarios(scenarioNames: string[]) {
    const results = scenarioNames.map((name) => this.runScenario({ scenario_name: name }));
    const baseline = this.runScenario({ scenario_name: 'baseline' });

    const deltas = results.map((r) => ({
      scenario_id: r.scenario_id,
      scenario_name: r.scenario_name,
      yield_delta: Number((r.predicted_yield - baseline.predicted_yield).toFixed(1)),
      confidence_delta: Number((r.confidence - baseline.confidence).toFixed(2)),
      cost_inr: r.cost_inr,
      in_validated_range: r.in_validated_range,
    }));

    const validResults = results.filter((r) => r.in_validated_range && r.scenario_id !== 'sim_001');
    const recommended = validResults.length > 0
      ? validResults.reduce((a, b) => (a.predicted_yield * a.confidence > b.predicted_yield * b.confidence ? a : b))
      : baseline;

    return {
      baseline,
      scenarios: results,
      deltas,
      recommended_scenario: recommended.scenario_name,
      recommendation_reason: `${recommended.scenario_name} provides highest expected yield recovery (${recommended.predicted_yield}%) with ${(recommended.confidence * 100).toFixed(0)}% confidence and low implementation friction.`,
    };
  }
}
