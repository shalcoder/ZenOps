"""
Automated Test Suite for Role 3: Simulation & Data Engineer (ZenOps).
Verifies:
1. Provenance tags (source, record_id, timestamp) in all records.
2. What-if Simulation Engine calculations & tool contracts.
3. Out-of-bounds operating range warnings.
4. Recommendation ranking & report exports.
"""

import os
import json
import unittest
import sys

# Ensure src directory is in path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from schema import BatchRecord, EventRecord
from diagnostic_engine import DiagnosticEngine
from simulation_engine import SimulationEngine
from recommendation_engine import RecommendationEngine
from report_generator import ReportGenerator

class TestRole3Engine(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, "data")

    def test_01_provenance_tags_in_fixtures(self):
        with open(os.path.join(self.data_dir, "incident_batch.json"), "r") as f:
            data = json.load(f)

        batch = data["batch"]
        self.assertIn("source", batch)
        self.assertIn("record_id", batch)
        self.assertIn("timestamp", batch)

        for evt in data["events"]:
            self.assertIn("source", evt)
            self.assertIn("record_id", evt)
            self.assertIn("timestamp", evt)

        for sr in data["sensor_readings"]:
            self.assertIn("source", sr)
            self.assertIn("record_id", sr)
            self.assertIn("timestamp", sr)

    def test_02_simulation_engine_contracts(self):
        sim = SimulationEngine(data_dir=self.data_dir)
        res = sim.run_scenario({"queue_delay_minutes": 30, "recalibrate_machine_7": True})
        
        self.assertIn("scenario_id", res)
        self.assertIn("baseline_yield", res)
        self.assertIn("predicted_yield", res)
        self.assertIn("confidence", res)
        self.assertIn("cost_estimate", res)
        self.assertIn("implementation_effort", res)
        self.assertIn("assumptions", res)
        self.assertIn("in_validated_range", res)

        self.assertTrue(res["in_validated_range"])
        self.assertEqual(res["predicted_yield"], 0.96)

    def test_03_out_of_bounds_operating_range_warning(self):
        sim = SimulationEngine(data_dir=self.data_dir)
        # Test out-of-range queue delay (150 minutes > max 120 minutes)
        res = sim.run_scenario({"queue_delay_minutes": 150})
        self.assertFalse(res["in_validated_range"])
        self.assertTrue(len(res["warnings"]) > 0)

    def test_04_recommendation_ranking(self):
        rec_eng = RecommendationEngine(data_dir=self.data_dir)
        recs = rec_eng.generate_recommendations()
        
        self.assertGreaterEqual(len(recs), 3)
        self.assertEqual(recs[0]["rank"], 1)
        self.assertIn("business_impact", recs[0])
        self.assertGreater(recs[0]["business_impact"]["monthly_financial_loss_avoided_usd"], 0)

    def test_05_report_generator(self):
        gen = ReportGenerator(data_dir=self.data_dir)
        mgr_md = gen.generate_manager_report_markdown()
        eng_md = gen.generate_engineer_report_markdown()

        self.assertIn("Executive Incident Report", mgr_md)
        self.assertIn("Detailed Engineering", eng_md)

if __name__ == "__main__":
    unittest.main()
