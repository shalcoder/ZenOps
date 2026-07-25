# ZenOps - Role 3 Master Implementation Plan

## Goal
Build the canonical data model, golden incident datasets, diagnostic rules, What-if Simulation Engine (`run_scenario`/`compare_scenarios`), recommendation ranking, business impact calculator, and report generator for ZenOps.

---

## Plan Structure in `implementation_plan/`

1. **`01_canonical_schema_and_fixtures_plan.md`**: Canonical JSON Schema design, incident baseline batch (`BATCH-INC-2026-07`) and healthy reference batch (`BATCH-REF-2026-06`).
2. **`02_simulation_and_diagnostic_engine_plan.md`**: Analytical layers (Descriptive, Diagnostic), What-if Simulation Engine (`run_scenario`, `compare_scenarios`), and Operating Range Validation (`in_validated_range`).
3. **`03_recommendation_and_reports_plan.md`**: Recommendation scoring engine, Business Impact Translator (financial & operational metrics), and Executive/Technical Report Generator.

---

## Execution Deliverables Architecture

```
ZenOps/
├── implementation_plan/
│   ├── master_implementation_plan.md
│   ├── 01_canonical_schema_and_fixtures_plan.md
│   ├── 02_simulation_and_diagnostic_engine_plan.md
│   └── 03_recommendation_and_reports_plan.md
├── data/
│   ├── canonical_schema.json
│   ├── incident_batch.json
│   ├── healthy_reference_batch.json
│   └── operating_ranges.json
├── src/
│   ├── __init__.py
│   ├── schema.py
│   ├── generate_fixtures.py
│   ├── diagnostic_engine.py
│   ├── simulation_engine.py
│   ├── recommendation_engine.py
│   └── report_generator.py
└── tests/
    ├── test_fixtures.py
    ├── test_simulation.py
    └── test_reports.py
```

---

## Next Steps
Proceeding to generate all plans into `implementation_plan/` and start step-by-step implementation.
