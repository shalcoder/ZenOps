import { Module } from '@nitrostack/core';
import { SimulationTools } from './simulation.tools.js';

@Module({
  name: 'simulation',
  description: 'Simulation Engine — counterfactual scenarios, sensitivity analysis, comparisons',
  controllers: [SimulationTools],
})
export class SimulationModule {}
