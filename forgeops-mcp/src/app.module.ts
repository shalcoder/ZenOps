/**
 * ForgeOps MCP Server — Root Application Module
 *
 * Wires all 6 domain modules into a single NitroStack MCP server:
 *   1. MES (Manufacturing Execution System)
 *   2. Maintenance Management
 *   3. Quality Management
 *   4. Materials & Procurement
 *   5. Simulation Engine
 *   6. Orchestrator (Copilot-level aggregation)
 */
import { McpApp, Module, ConfigModule } from '@nitrostack/core';
import { SystemHealthCheck } from './health/system.health.js';

// Domain Modules
import { MesModule } from './modules/mes/mes.module.js';
import { MaintenanceModule } from './modules/maintenance/maintenance.module.js';
import { QualityModule } from './modules/quality/quality.module.js';
import { MaterialsModule } from './modules/materials/materials.module.js';
import { SimulationModule } from './modules/simulation/simulation.module.js';
import { OrchestratorModule } from './modules/orchestrator/orchestrator.module.js';

@McpApp({
  module: AppModule,
  server: {
    name: 'forgeops-mcp',
    version: '1.0.0',
  },
  logging: {
    level: 'info',
  },
})
@Module({
  name: 'app',
  description: 'ForgeOps — AI Decision Workbench MCP Server for Smart Manufacturing',
  imports: [
    ConfigModule.forRoot(),
    MesModule,
    MaintenanceModule,
    QualityModule,
    MaterialsModule,
    SimulationModule,
    OrchestratorModule,
  ],
  providers: [SystemHealthCheck],
})
export class AppModule {}
