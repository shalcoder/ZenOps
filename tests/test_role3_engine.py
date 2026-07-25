"""
Automated Test Suite for Role 3: Simulation & Data Engineer (ZenOps / ForgeOps).
Verifies:
1. Provenance tags (source, record_id, timestamp) in all records.
2. What-if Simulation Engine calculations & tool contracts matching Blueprint Section 08.
3. Out-of-bounds operating range warnings.
4. Hard constraint checks (e.g. no supplier change).
5. Recommendation ranking & report exports with Risk Assessment.
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

    def test_02_blueprint_section08_simulation_matrix(self):
        sim = SimulationEngine(data_dir=self.data_dir)
        
        # Test 1: Queue delay <= 60 minutes -> 96% yield
        sc_queue = sim.run_scenario({"queue_delay_minutes": 30, "recalibrate_machine_7": True})
        self.assertEqual(sc_queue["predicted_yield"], 0.96)

        # Test 2: Replace Machine 7 -> 84% yield
        sc_m7 = sim.run_scenario({"replace_machine_7": True})
        self.assertEqual(sc_m7["predicted_yield"], 0.84)

        # Test 3: Humidity <= 55% -> 96% yield
        sc_hum = sim.run_scenario({"humidity_pct": 50.0})
        self.assertEqual(sc_hum["predicted_yield"], 0.96)

    def test_03_out_of_bounds_operating_range_warning(self):
        sim = SimulationEngine(data_dir=self.data_dir)
        # Test out-of-range queue delay (150 minutes > max 120 minutes)
        res = sim.run_scenario({"queue_delay_minutes": 150})
        self.assertFalse(res["in_validated_range"])
        self.assertTrue(len(res["warnings"]) > 0)

    def test_04_hard_constraint_evaluation(self):
        sim = SimulationEngine(data_dir=self.data_dir)
        # Test constraint: no supplier change
        res = sim.run_scenario({"change_supplier": True}, constraints={"no_supplier_change": True})
        self.assertEqual(res["implementation_effort"], "INFEASIBLE")

    def test_05_recommendation_ranking_and_risk_reports(self):
        rec_eng = RecommendationEngine(data_dir=self.data_dir)
        recs = rec_eng.generate_recommendations()
        
        self.assertGreaterEqual(len(recs), 3)
        self.assertEqual(recs[0]["rank"], 1)
        self.assertIn("business_impact", recs[0])

        gen = ReportGenerator(data_dir=self.data_dir)
        gen.export_all_reports()
        
        mgr_md = gen.generate_manager_report_markdown()
        self.assertIn("Risk Assessment", mgr_md)
        self.assertIn("Implementation Risk", mgr_md)
        self.assertIn("Decision Record Sign-Off", mgr_md)

if __name__ == "__main__":
    unittest.main()
