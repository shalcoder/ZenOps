"""
Canonical Data Schema for ZenOps (Role 3: Simulation & Data Engineer).
Every record must contain: source, record_id, timestamp.
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any

@dataclass
class BatchRecord:
    batch_id: str
    product: str
    line: str
    plant: str
    start_time: str
    end_time: str
    yield_pct: float
    status: str
    source: str
    record_id: str
    timestamp: str

@dataclass
class EventRecord:
    event_id: str
    batch_id: str
    source_system: str
    event_type: str
    timestamp: str
    stage: str
    severity: str
    value: Any
    confidence: float
    source: str
    record_id: str

@dataclass
class MachineRecord:
    machine_id: str
    name: str
    line: str
    maintenance_state: str
    alert_history: List[Dict[str, Any]]
    source: str
    record_id: str
    timestamp: str

@dataclass
class SensorReadingRecord:
    reading_id: str
    batch_id: str
    timestamp: str
    humidity_pct: float
    temperature_c: float
    pressure_bar: float
    queue_delay_minutes: float
    cycle_time_seconds: float
    source: str
    record_id: str

@dataclass
class QualityRecord:
    inspection_id: str
    batch_id: str
    stage: str
    defect_code: Optional[str]
    pass_fail: str
    severity: str
    source: str
    record_id: str
    timestamp: str

@dataclass
class MaterialRecord:
    material_id: str
    material_name: str
    supplier: str
    lot_number: str
    formulation: str
    storage_condition: str
    source: str
    record_id: str
    timestamp: str
