# Plan 01: Canonical Schema & Data Fixtures

## Purpose
Define the schema and populate structured JSON datasets for both the Representative Incident (`BATCH-INC-2026-07`) and the Healthy Reference Batch (`BATCH-REF-2026-06`).

## Deliverables
1. `data/canonical_schema.json`: Formal JSON Schema defining Batches, Events, Machines, SensorReadings, QualityRecords, Materials.
2. Mandatory metadata for every record: `source`, `record_id`, `timestamp`.
3. `data/incident_batch.json`:
   - Yield drop 96% -> 82%.
   - Full timeline spine: Elevated humidity -> Queue delay (>60m) -> Machine 7 maintenance alert -> Temperature drift -> Defect inspection -> Batch rejection.
4. `data/healthy_reference_batch.json`:
   - Nominal operating conditions with 97.2% yield.
5. `data/operating_ranges.json`: Validated bounds for queue delay, humidity, temperature, cycle time.
