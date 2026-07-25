"""
Audit Log — SQLite-based trail of every agent pipeline run.
Records: question, intent, tools used, record refs, simulation version, output, timestamp.
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_log.db")


def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            query TEXT NOT NULL,
            intent TEXT NOT NULL,
            required_servers TEXT NOT NULL,
            evidence_sources TEXT NOT NULL,
            simulation_version TEXT NOT NULL,
            conclusion TEXT NOT NULL,
            confidence REAL NOT NULL,
            evidence_refs TEXT NOT NULL,
            assumptions TEXT NOT NULL,
            ui_actions TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()


def log_pipeline_run(
    query: str,
    intent: str,
    required_servers: list,
    evidence_sources: list,
    conclusion: str,
    confidence: float,
    evidence_refs: list,
    assumptions: list,
    ui_actions: list,
    simulation_version: str = "forgeops-sim-v1.0",
):
    init_db()
    con = sqlite3.connect(DB_PATH)
    con.execute(
        """INSERT INTO audit_log
           (timestamp, query, intent, required_servers, evidence_sources,
            simulation_version, conclusion, confidence, evidence_refs, assumptions, ui_actions)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            datetime.utcnow().isoformat(),
            query,
            intent,
            json.dumps(required_servers),
            json.dumps(evidence_sources),
            simulation_version,
            conclusion,
            confidence,
            json.dumps(evidence_refs),
            json.dumps(assumptions),
            json.dumps(ui_actions),
        ),
    )
    con.commit()
    con.close()


def get_audit_log(limit: int = 50) -> list:
    init_db()
    con = sqlite3.connect(DB_PATH)
    rows = con.execute(
        "SELECT * FROM audit_log ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    con.close()
    columns = ["id", "timestamp", "query", "intent", "required_servers", "evidence_sources",
               "simulation_version", "conclusion", "confidence", "evidence_refs", "assumptions", "ui_actions"]
    result = []
    for row in rows:
        d = dict(zip(columns, row))
        for field in ["required_servers", "evidence_sources", "evidence_refs", "assumptions", "ui_actions"]:
            d[field] = json.loads(d[field])
        result.append(d)
    return result
