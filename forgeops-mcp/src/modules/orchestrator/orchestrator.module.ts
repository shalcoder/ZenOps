import { Module } from '@nitrostack/core';
import { OrchestratorTools } from './orchestrator.tools.js';

@Module({
  name: 'orchestrator',
  description: 'Orchestrator — incident summary, timeline, causal graph, recommendations, impact',
  controllers: [OrchestratorTools],
})
export class OrchestratorModule {}
