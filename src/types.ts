export type Severity = 'info' | 'warning' | 'critical';
export type LoadState = 'idle' | 'loading' | 'success' | 'partial' | 'error';
export type EvidenceType = 'observed_correlation' | 'model_estimated' | 'counterfactual_simulated';
export type FocusOrigin = 'user' | 'replay' | 'assistant';

export type Incident = {
  id: string;
  title: string;
  plant: string;
  line: string;
  product: string;
  batchId: string;
  severity: 'low' | 'medium' | 'high';
  status: 'open' | 'investigating' | 'monitoring';
  detectedAt: string;
  baselineYield: number;
  currentYield: number;
  exposureInr: number;
  summary: string;
};

export type IncidentEvent = {
  id: string;
  timestamp: string;
  offsetMinutes: number;
  label: string;
  category: 'sensor' | 'queue' | 'maintenance' | 'inspection' | 'operator' | 'system';
  severity: Severity;
  source: string;
  recordId: string;
  stageId: string;
  graphNodeIds: string[];
  evidenceIds: string[];
  confidence: number;
  value: string;
  description: string;
};

export type ReplayStage = {
  id: string;
  label: string;
  shortLabel: string;
  status: 'ok' | 'warning' | 'failure';
  startMinute: number;
  endMinute: number;
  summary: string;
  inputs: string[];
  outputs: string[];
  metrics: Array<{ label: string; value: string; state?: 'normal' | 'warning' | 'critical' }>;
  eventIds: string[];
};

export type GraphNode = {
  id: string;
  label: string;
  type: 'condition' | 'process' | 'equipment' | 'material' | 'environment' | 'outcome';
  influence: number;
  confidence: number;
  evidenceType: EvidenceType;
  controllable: boolean;
  source: string;
  value: string;
  threshold: string;
  description: string;
  eventIds: string[];
  evidenceIds: string[];
  position: { x: number; y: number };
};

export type GraphEdge = {
  id: string;
  from: string;
  to: string;
  strength: number;
  evidenceType: EvidenceType;
  label: string;
};

export type EvidenceRecord = {
  id: string;
  title: string;
  source: string;
  recordId: string;
  timestamp: string;
  kind: 'record' | 'sensor' | 'simulation' | 'comparison';
  summary: string;
  confidence: number;
  evidenceType: EvidenceType;
};

export type SimulationResult = {
  scenarioId: string;
  scenarioName: string;
  baselineYield: number;
  predictedYield: number;
  confidence: number;
  cost: string;
  effort: string;
  assumptions: string[];
  inValidatedRange: boolean;
  warnings: string[];
  evidenceRefs: string[];
  modelVersion: string;
};

export type Recommendation = {
  id: string;
  rank: number;
  title: string;
  confidence: number;
  predictedYield: number;
  cost: string;
  costInr: number;
  effort: string;
  impact: 'Low' | 'Medium' | 'High';
  risk: 'Low' | 'Medium' | 'High';
  description: string;
  savingsPerWeekInr: number;
  evidenceRefs: string[];
};

export type BusinessImpact = {
  currentMonthlyLossInr: number;
  monthlySavingsInr: number;
  downtimeReductionPct: number;
  baselineYield: number;
  predictedYield: number;
  paybackPeriod: string;
  basis: string;
};

export type ToolTraceStep = {
  id: string;
  server: string;
  tool: string;
  status: 'queued' | 'running' | 'complete';
  durationMs: number;
  records: string[];
};

export type AssistantResponse = {
  intent: string;
  conclusion: string;
  effect: string;
  confidence: number;
  evidenceRefs: string[];
  assumptions: string[];
  actions: Array<'open_evidence' | 'run_comparison' | 'generate_report'>;
  toolTrace: ToolTraceStep[];
};

export type FocusContext = {
  incidentId: string;
  eventId: string | null;
  stageId: string | null;
  graphNodeIds: string[];
  evidenceIds: string[];
  timeMinute: number;
  timeRange: [number, number] | null;
  pinned: boolean;
  origin: FocusOrigin;
  aiLabel: string | null;
};
