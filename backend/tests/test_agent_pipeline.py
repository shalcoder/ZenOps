"""
End-to-end pipeline tests for all 4 golden-path queries.
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.pipeline import run_pipeline
from backend.agents.planner.planner import PlannerAgent, classify_intent_llm
from backend.schemas.planner_models import PlannerInput
from unittest.mock import patch
import json

class TestPlannerIntentClassification(unittest.TestCase):
    @patch('backend.agents.planner.planner.call_llm')
    def test_show_evidence_intent(self, mock_call_llm):
        mock_call_llm.return_value = '{"intent": "show_evidence"}'
        self.assertEqual(classify_intent_llm("Show me the evidence"), "show_evidence")

    @patch('backend.agents.planner.planner.call_llm')
    def test_explain_exclusion_intent(self, mock_call_llm):
        mock_call_llm.return_value = '{"intent": "explain_exclusion"}'
        self.assertEqual(classify_intent_llm("Why was Machine 7 ruled out?"), "explain_exclusion")

    @patch('backend.agents.planner.planner.call_llm')
    def test_compare_intent(self, mock_call_llm):
        mock_call_llm.return_value = '{"intent": "compare_options"}'
        self.assertEqual(classify_intent_llm("Compare Option A vs Option B"), "compare_options")

    @patch('backend.agents.planner.planner.call_llm')
    def test_constraint_intent(self, mock_call_llm):
        mock_call_llm.return_value = '{"intent": "constraint_query"}'
        self.assertEqual(classify_intent_llm("We cannot change suppliers for a month. What should we do?"), "constraint_query")

    @patch('backend.agents.planner.planner.call_llm')
    def test_report_intent(self, mock_call_llm):
        mock_call_llm.return_value = '{"intent": "generate_report"}'
        self.assertEqual(classify_intent_llm("Generate a report for the plant manager"), "generate_report")


class TestFullPipeline(unittest.TestCase):
    @patch('backend.agents.execution.execution.call_llm')
    @patch('backend.agents.planner.planner.call_llm')
    def test_show_evidence_pipeline(self, mock_planner_llm, mock_exec_llm):
        mock_planner_llm.return_value = '{"intent": "show_evidence"}'
        mock_exec_llm.return_value = "Here is the evidence."
        output = run_pipeline("Show me the evidence.")
        self.assertIsNotNone(output.conclusion)
        self.assertGreater(len(output.ui_actions), 0)
        self.assertGreater(output.confidence, 0)

    @patch('backend.agents.execution.execution.call_llm')
    @patch('backend.agents.planner.planner.call_llm')
    def test_explain_exclusion_pipeline(self, mock_planner_llm, mock_exec_llm):
        mock_planner_llm.return_value = '{"intent": "explain_exclusion"}'
        mock_exec_llm.return_value = "Machine 7 was ruled out because queue delay is a stronger factor."
        output = run_pipeline("Why was Machine 7 ruled out?")
        self.assertIn("Machine 7", output.conclusion)
        self.assertTrue(any(a.target_id == "machine_7" for a in output.ui_actions))

    @patch('backend.agents.execution.execution.call_llm')
    @patch('backend.agents.planner.planner.call_llm')
    def test_compare_pipeline(self, mock_planner_llm, mock_exec_llm):
        mock_planner_llm.return_value = '{"intent": "compare_options"}'
        mock_exec_llm.return_value = "Option A is better."
        output = run_pipeline("Compare Option A vs Option B.")
        self.assertGreater(len(output.ui_actions), 0)

    @patch('backend.agents.execution.execution.call_llm')
    @patch('backend.agents.planner.planner.call_llm')
    def test_constraint_pipeline(self, mock_planner_llm, mock_exec_llm):
        mock_planner_llm.return_value = '{"intent": "constraint_query"}'
        mock_exec_llm.return_value = "Due to the constraint, do this."
        output = run_pipeline("We cannot change suppliers. What should we do?",
                              constraints={"no_supplier_change": True})
        self.assertIsNotNone(output.conclusion)

    @patch('backend.agents.execution.execution.call_llm')
    @patch('backend.agents.planner.planner.call_llm')
    def test_report_pipeline(self, mock_planner_llm, mock_exec_llm):
        mock_planner_llm.return_value = '{"intent": "generate_report"}'
        mock_exec_llm.return_value = "Report generated."
        output = run_pipeline("Generate a report for the plant manager.")
        self.assertGreater(len(output.generated_reports), 0)
        self.assertIn("ForgeOps", output.generated_reports[0].markdown)


if __name__ == "__main__":
    unittest.main()
