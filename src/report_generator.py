"""
Executive & Technical Report Generator for ZenOps (Role 3: Simulation & Data Engineer).
Produces Markdown and HTML exports for Engineer (detailed) and Manager (summary) views.
"""

import json
import os
from typing import Dict, Any
from diagnostic_engine import DiagnosticEngine
from recommendation_engine import RecommendationEngine

class ReportGenerator:
    def __init__(self, data_dir: str = None):
        self.diagnostic = DiagnosticEngine(data_dir=data_dir)
        self.recommender = RecommendationEngine(data_dir=data_dir)

    def generate_manager_report_markdown(self) -> str:
        diag_res = self.diagnostic.analyze_batch()
        recs = self.recommender.generate_recommendations()
        top_rec = recs[0]

        md = f"""# Executive Incident Report & Decision Record - ZenOps

**Plant**: Plant Alpha - Detroit  
**Batch ID**: {diag_res['batch_id']}  
**Status**: {diag_res['status']}  
**Yield Performance**: Baseline 96.0% → Actual {diag_res['yield_pct']}% (Yield Loss: {diag_res['yield_loss_pct']}%)  

---

## Executive Summary
During the production run of Batch `{diag_res['batch_id']}`, yield dropped sharply by {diag_res['yield_loss_pct']}% below baseline targets, resulting in final batch rejection. Root cause analysis confirms a combined environmental and machinery anomaly.

## Root Cause Statement
- **Primary Causal Pathway**: Material moisture degradation in staging queue coupled with Machine 7 spindle thermal drift.
- **Key Contributing Factors**: Elevated humidity (76% RH), extended queue delay (85 minutes), and Machine 7 spindle drift (28.4°C).

---

## Top Recommended Intervention
### {top_rec['title']}
- **Predicted Yield Recovery**: {diag_res['yield_pct']}% → **{top_rec['predicted_yield_pct']}%** (+{top_rec['yield_recovery_pct']}%)
- **Implementation Speed**: {top_rec['implementation_speed']}
- **Cost / Effort**: {top_rec['cost_estimate'].capitalize()} Cost / {top_rec['effort'].capitalize()} Effort
- **Model Confidence**: {int(top_rec['confidence'] * 100)}%

### Business Financial Impact
- **Monthly Loss Avoided**: ${top_rec['business_impact']['monthly_financial_loss_avoided_usd']:,.2f}
- **Downtime Avoided**: {top_rec['business_impact']['downtime_avoided_hours']} hours (${top_rec['business_impact']['downtime_savings_usd']:,.2f})
- **Basis**: {top_rec['business_impact']['calculation_basis']}

---

## Decision Record Sign-Off
- [ ] **Approved Action**: Recalibrate Machine 7 & Enforce 30-min Queue Ceiling
- **Approved By**: Plant Operations Manager  
- **Timestamp**: 2026-07-25 14:52:00 UTC  
- **Follow-up Owner**: Lead Maintenance & Dispatch Engineer
"""
        return md

    def generate_manager_report_html(self) -> str:
        diag_res = self.diagnostic.analyze_batch()
        recs = self.recommender.generate_recommendations()
        top_rec = recs[0]

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ZenOps Executive Incident Report - {diag_res['batch_id']}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #0f172a; color: #f8fafc; }}
        .card {{ background-color: #1e293b; padding: 24px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 24px; }}
        h1 {{ color: #38bdf8; font-size: 24px; margin-top: 0; }}
        h2 {{ color: #818cf8; font-size: 18px; border-bottom: 1px solid #334155; padding-bottom: 8px; }}
        .badge {{ background: #ef4444; color: white; padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: bold; }}
        .metric-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 16px; }}
        .metric-item {{ background: #0f172a; padding: 16px; border-radius: 8px; border: 1px solid #334155; text-align: center; }}
        .metric-val {{ font-size: 24px; font-weight: bold; color: #4ade80; }}
        .metric-lbl {{ font-size: 12px; color: #94a3b8; margin-top: 4px; }}
        ul {{ line-height: 1.6; color: #cbd5e1; }}
        .signoff {{ background: #0284c7; padding: 16px; border-radius: 8px; font-weight: 500; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>Executive Incident Report & Decision Record <span class="badge">{diag_res['status']}</span></h1>
        <p><strong>Batch ID:</strong> {diag_res['batch_id']} | <strong>Plant:</strong> Plant Alpha - Detroit</p>
        <p><strong>Yield Delta:</strong> Baseline 96.0% → Actual {diag_res['yield_pct']}% (<span style="color:#f87171">-{diag_res['yield_loss_pct']}% Loss</span>)</p>
    </div>

    <div class="card">
        <h2>Root Cause Statement</h2>
        <ul>
            <li><strong>Primary Cause:</strong> Material moisture degradation in staging queue coupled with Machine 7 spindle thermal drift.</li>
            <li><strong>Contributing Factors:</strong> Elevated Humidity (76% RH), Queue Delay (85 mins), Spindle Drift (28.4°C).</li>
        </ul>
    </div>

    <div class="card">
        <h2>Top Recommended Action: {top_rec['title']}</h2>
        <div class="metric-grid">
            <div class="metric-item">
                <div class="metric-val">{top_rec['predicted_yield_pct']}%</div>
                <div class="metric-lbl">Predicted Yield</div>
            </div>
            <div class="metric-item">
                <div class="metric-val">${top_rec['business_impact']['monthly_financial_loss_avoided_usd']:,.0f}</div>
                <div class="metric-lbl">Monthly Loss Avoided</div>
            </div>
            <div class="metric-item">
                <div class="metric-val">{top_rec['business_impact']['downtime_avoided_hours']} hrs</div>
                <div class="metric-lbl">Downtime Avoided</div>
            </div>
        </div>
    </div>

    <div class="card signoff">
        <h3>Decision Sign-Off Record</h3>
        <p>✔ Approved Action: Recalibrate Machine 7 & Enforce 30-min Queue Ceiling</p>
        <p>Approved By: Plant Operations Manager | Timestamp: 2026-07-25 14:52:00 UTC</p>
    </div>
</body>
</html>
"""
        return html

    def generate_engineer_report_markdown(self) -> str:
        diag_res = self.diagnostic.analyze_batch()
        recs = self.recommender.generate_recommendations()

        md = f"""# Detailed Engineering & Diagnostics Report - ZenOps

**Batch ID**: {diag_res['batch_id']}  
**Plant**: Plant Alpha - Detroit | **Line**: Line 3  
**Anomalies Detected**: {diag_res['anomalies_detected']}  

---

## 1. Sensor Anomaly Breakdown
"""
        for a in diag_res['anomalies']:
            md += f"- **[{a['severity']}] {a['sensor']}**: {a['description']} (Time: `{a['timestamp']}`)\n"

        md += "\n--- \n\n## 2. Root Cause Correlation Analysis\n"
        for path in diag_res['root_cause_analysis']:
            md += f"### Pathway {path['pathway_id']}: {path['primary_cause']} (Confidence: {int(path['confidence_score']*100)}%)\n"
            md += "**Causal Sequence**:\n"
            for step in path['causal_chain']:
                md += f"1. {step}\n"

        md += "\n--- \n\n## 3. What-if Simulation Interventions Evaluated\n"
        for rec in recs:
            md += f"### Rank #{rec['rank']}: {rec['title']}\n"
            md += f"- **Predicted Yield**: {rec['predicted_yield_pct']}%\n"
            md += f"- **Validated Operating Range**: {'VALIDATED' if rec['in_validated_range'] else 'WARNING: OUT OF BOUNDS'}\n"
            md += f"- **Assumptions**: {', '.join(rec['simulation_details']['assumptions'])}\n"
            md += f"- **Inputs**: `{json.dumps(rec['simulation_details']['inputs'])}`\n\n"

        return md

    def export_all_reports(self, output_dir: str = None):
        if output_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            output_dir = os.path.join(base_dir, "reports")
        os.makedirs(output_dir, exist_ok=True)

        mgr_md = self.generate_manager_report_markdown()
        mgr_html = self.generate_manager_report_html()
        eng_md = self.generate_engineer_report_markdown()

        with open(os.path.join(output_dir, "manager_executive_report.md"), "w") as f:
            f.write(mgr_md)

        with open(os.path.join(output_dir, "manager_executive_report.html"), "w") as f:
            f.write(mgr_html)

        with open(os.path.join(output_dir, "engineer_detailed_report.md"), "w") as f:
            f.write(eng_md)

        print(f"Reports successfully exported to {output_dir} directory!")

if __name__ == "__main__":
    gen = ReportGenerator()
    gen.export_all_reports()
