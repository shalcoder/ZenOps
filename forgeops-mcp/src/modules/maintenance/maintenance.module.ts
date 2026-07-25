import { Module } from '@nitrostack/core';
import { MaintenanceTools } from './maintenance.tools.js';

@Module({
  name: 'maintenance',
  description: 'Maintenance Management — machine alerts, condition monitoring, service history',
  controllers: [MaintenanceTools],
})
export class MaintenanceModule {}
