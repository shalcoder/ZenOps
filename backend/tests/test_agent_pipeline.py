"""
End-to-end pipeline tests for all 4 golden-path queries.
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.pipeline import run_pipeline
from backend.agents.planner.planner import PlannerAgent, classify_intent
from backend.schemas.planner_models import PlannerInput


class TestPlannerIntentClassification(unittest.TestCase):
    def test_show_evidence_intent(self):
        self.assertEqual(classify_intent("Show me the evidence"), "show_evidence")

    def test_explain_exclusion_intent(self):
        self.assertEqual(classify_intent("Why was Machine 7 ruled out?"), "explain_exclusion")

    def test_compare_intent(self):
        self.assertEqual(classify_intent("Compare Option A vs Option B"), "compare_options")

    def test_constraint_intent(self):
        self.assertEqual(classify_intent("We cannot change suppliers for a month. What should we do?"), "constraint_query")

    def test_report_intent(self):
        self.assertEqual(classify_intent("Generate a report for the plant manager"), "generate_report")


class TestFullPipeline(unittest.TestCase):
    def test_show_evidence_pipeline(self):
        output = run_pipeline("Show me the evidence.")
        self.assertIsNotNone(output.conclusion)
        self.assertGreater(len(output.ui_actions), 0)
        self.assertGreater(output.confidence, 0)

    def test_explain_exclusion_pipeline(self):
        output = run_pipeline("Why was Machine 7 ruled out?")
        self.assertIn("Machine 7", output.conclusion)
        self.assertTrue(any(a.target_id == "machine_7" for a in output.ui_actions))

    def test_compare_pipeline(self):
        output = run_pipeline("Compare Option A vs Option B.")
        self.assertGreater(len(output.ui_actions), 0)

    def test_constraint_pipeline(self):
        output = run_pipeline("We cannot change suppliers. What should we do?",
                              constraints={"no_supplier_change": True})
        self.assertIsNotNone(output.conclusion)

    def test_report_pipeline(self):
        output = run_pipeline("Generate a report for the plant manager.")
        self.assertGreater(len(output.generated_reports), 0)
        self.assertIn("ForgeOps", output.generated_reports[0].markdown)


if __name__ == "__main__":
    unittest.main()
