"""
Lightweight REST API Server for ZenOps / ForgeOps (Role 3 Data & Simulation Engine).
Exposes HTTP JSON endpoints for Role 1 (MCP Agent) and Role 2 (Frontend UI).
Runs on standard Python http.server (no external dependencies required).
"""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulation_engine import SimulationEngine
from diagnostic_engine import DiagnosticEngine
from recommendation_engine import RecommendationEngine
from report_generator import ReportGenerator

class ZenOpsAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_OPTIONS(self):
        self._send_json({"status": "ok"})

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        if path == "/api/incident":
            with open(os.path.join(base_dir, "data", "incident_batch.json"), "r") as f:
                self._send_json(json.load(f))
        elif path == "/api/reference":
            with open(os.path.join(base_dir, "data", "healthy_reference_batch.json"), "r") as f:
                self._send_json(json.load(f))
        elif path == "/api/diagnose":
            diag = DiagnosticEngine()
            self._send_json(diag.analyze_batch())
        elif path == "/api/recommendations":
            rec = RecommendationEngine()
            self._send_json(rec.generate_recommendations())
        elif path == "/api/report/manager":
            gen = ReportGenerator()
            self._send_json({"markdown": gen.generate_manager_report_markdown(), "html": gen.generate_manager_report_html()})
        else:
            self._send_json({"error": "Endpoint not found", "available_endpoints": ["/api/incident", "/api/reference", "/api/diagnose", "/api/recommendations", "/api/report/manager"]}, status=404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len) if content_len > 0 else b"{}"

        try:
            payload = json.loads(body.decode("utf-8"))
        except Exception:
            payload = {}

        if path == "/api/simulate":
            sim = SimulationEngine()
            inputs = payload.get("inputs", {})
            constraints = payload.get("constraints", {})
            name = payload.get("name", "Custom Scenario")
            result = sim.run_scenario(inputs, scenario_name=name, constraints=constraints)
            self._send_json(result)
        else:
            self._send_json({"error": "Endpoint not found"}, status=404)

def run_server(port=8080):
    server_address = ("", port)
    httpd = HTTPServer(server_address, ZenOpsAPIHandler)
    print(f"ZenOps Data & Simulation Engine API server running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
