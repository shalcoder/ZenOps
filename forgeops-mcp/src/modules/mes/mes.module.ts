import { Module } from '@nitrostack/core';
import { MesTools } from './mes.tools.js';

@Module({
  name: 'mes',
  description: 'Manufacturing Execution System — batch history, production paths, queue events',
  controllers: [MesTools],
})
export class MesModule {}
