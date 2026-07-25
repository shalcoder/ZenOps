import { Module } from '@nitrostack/core';
import { MaterialsTools } from './materials.tools.js';

@Module({
  name: 'materials',
  description: 'Materials & Procurement — supplier info, material constraints, availability',
  controllers: [MaterialsTools],
})
export class MaterialsModule {}
