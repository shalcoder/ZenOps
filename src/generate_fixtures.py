"""
Generator script to produce golden dataset fixtures for ZenOps demo.
- Incident Batch (BATCH-INC-2026-07): Yield 96% -> 82%
- Healthy Reference Batch (BATCH-REF-2026-06): Nominal yield 97.2%
- Operating Ranges (calibration limits for simulator validation)
"""

import json
import os
from typing import Dict, Any

def create_operating_ranges() -> Dict[str, Any]:
    return {
        "queue_delay_minutes": {
            "min_valid": 0.0,
            "max_valid": 120.0,
            "nominal": 15.0,
            "unit": "minutes"
        },
        "humidity_pct": {
            "min_valid": 30.0,
            "max_valid": 75.0,
            "nominal": 45.0,
            "unit": "%"
        },
        "temperature_c": {
            "min_valid": 18.0,
            "max_valid": 28.0,
            "nominal": 22.0,
            "unit": "°C"
        },
        "cycle_time_seconds": {
            "min_valid": 40.0,
            "max_valid": 100.0,
            "nominal": 55.0,
            "unit": "seconds"
        }
    }

def create_incident_batch_data() -> Dict[str, Any]:
    batch_id = "BATCH-INC-2026-07"
    return {
        "batch": {
            "batch_id": batch_id,
            "product": "Precision Alloy Casing X4",
            "line": "Line 3",
            "plant": "Plant Alpha - Detroit",
            "start_time": "2026-07-25T06:00:00Z",
            "end_time": "2026-07-25T13:30:00Z",
            "yield_pct": 82.0,
            "baseline_yield_pct": 96.0,
            "status": "REJECTED",
            "source": "MES_PROD_DB",
            "record_id": "REC-BATCH-INC-07",
            "timestamp": "2026-07-25T13:30:00Z"
        },
        "materials": {
            "material_id": "MAT-LOT-8841",
            "material_name": "High-Grade Titanium Resin Blend",
            "supplier": "AeroMaterials Corp",
            "lot_number": "LOT-8841-B",
            "formulation": "v3.2-HumiditySensitive",
            "storage_condition": "Ambient Temp (High relative humidity recorded in staging)",
            "source": "ERP_INV_SYS",
            "record_id": "REC-MAT-8841",
            "timestamp": "2026-07-25T05:45:00Z"
        },
        "machine": {
            "machine_id": "M7-CNC-MILL",
            "name": "Machine 7 - Multi-Axis CNC Mill",
            "line": "Line 3",
            "maintenance_state": "NEEDS_CALIBRATION",
            "alert_history": [
                {
                    "alert_id": "ALT-M7-0941",
                    "type": "SPINDLE_THERMAL_DRIFT",
                    "severity": "HIGH",
                    "timestamp": "2026-07-25T09:15:00Z"
                }
            ],
            "source": "SCADA_MNT_LOG",
            "record_id": "REC-M7-STATE",
            "timestamp": "2026-07-25T09:15:00Z"
        },
        "sensor_readings": [
            {
                "reading_id": "SR-01",
                "batch_id": batch_id,
                "timestamp": "2026-07-25T06:30:00Z",
                "humidity_pct": 44.5,
                "temperature_c": 22.1,
                "pressure_bar": 4.0,
                "queue_delay_minutes": 12.0,
                "cycle_time_seconds": 54.0,
                "source": "SCADA_IOT_SENSORS",
                "record_id": "REC-SR-01"
            },
            {
                "reading_id": "SR-02",
                "batch_id": batch_id,
                "timestamp": "2026-07-25T08:00:00Z",
                "humidity_pct": 68.2,
                "temperature_c": 23.5,
                "pressure_bar": 4.1,
                "queue_delay_minutes": 35.0,
                "cycle_time_seconds": 62.0,
                "source": "SCADA_IOT_SENSORS",
                "record_id": "REC-SR-02"
            },
            {
                "reading_id": "SR-03",
                "batch_id": batch_id,
                "timestamp": "2026-07-25T09:15:00Z",
                "humidity_pct": 74.5,
                "temperature_c": 27.8,
                "pressure_bar": 3.8,
                "queue_delay_minutes": 78.0,
                "cycle_time_seconds": 88.0,
                "source": "SCADA_IOT_SENSORS",
                "record_id": "REC-SR-03"
            },
            {
                "reading_id": "SR-04",
                "batch_id": batch_id,
                "timestamp": "2026-07-25T11:00:00Z",
                "humidity_pct": 76.0,
                "temperature_c": 28.4,
                "pressure_bar": 3.7,
                "queue_delay_minutes": 85.0,
                "cycle_time_seconds": 92.0,
                "source": "SCADA_IOT_SENSORS",
                "record_id": "REC-SR-04"
            }
        ],
        "events": [
            {
                "event_id": "EVT-101",
                "batch_id": batch_id,
                "source_system": "MES",
                "event_type": "BATCH_STARTED",
                "timestamp": "2026-07-25T06:00:00Z",
                "stage": "Staging",
                "severity": "INFO",
                "value": "Batch initialization completed",
                "confidence": 1.0,
                "source": "MES_DB",
                "record_id": "REC-EVT-101"
            },
            {
                "event_id": "EVT-102",
                "batch_id": batch_id,
                "source_system": "ENVIRONMENTAL_SENSORS",
                "event_type": "HUMIDITY_ELEVATED",
                "timestamp": "2026-07-25T07:45:00Z",
                "stage": "Staging",
                "severity": "WARNING",
                "value": "74.5% RH (Threshold: 60.0% RH)",
                "confidence": 0.98,
                "source": "ENV_MONITOR",
                "record_id": "REC-EVT-102"
            },
            {
                "event_id": "EVT-103",
                "batch_id": batch_id,
                "source_system": "MES_DISPATCH",
                "event_type": "QUEUE_DELAY_SPIKE",
                "timestamp": "2026-07-25T08:30:00Z",
                "stage": "Machining Prep",
                "severity": "HIGH",
                "value": "78 minutes in staging queue",
                "confidence": 0.95,
                "source": "DISPATCH_LOGGER",
                "record_id": "REC-EVT-103"
            },
            {
                "event_id": "EVT-104",
                "batch_id": batch_id,
                "source_system": "SCADA_MACHINE7",
                "event_type": "MAINTENANCE_ALERT",
                "timestamp": "2026-07-25T09:15:00Z",
                "stage": "Machining",
                "severity": "CRITICAL",
                "value": "Machine 7 Spindle thermal drift + micro-vibration warning",
                "confidence": 0.99,
                "source": "SCADA_M7",
                "record_id": "REC-EVT-104"
            },
            {
                "event_id": "EVT-105",
                "batch_id": batch_id,
                "source_system": "THERMAL_MONITOR",
                "event_type": "TEMPERATURE_DRIFT",
                "timestamp": "2026-07-25T09:40:00Z",
                "stage": "Machining",
                "severity": "HIGH",
                "value": "28.4°C coolant exit temp",
                "confidence": 0.96,
                "source": "THERM_SENS_07",
                "record_id": "REC-EVT-105"
            },
            {
                "event_id": "EVT-106",
                "batch_id": batch_id,
                "source_system": "QUALITY_VISION_AI",
                "event_type": "MICRO_FRACTURE_DEFECTS",
                "timestamp": "2026-07-25T12:00:00Z",
                "stage": "Final Quality Inspection",
                "severity": "CRITICAL",
                "value": "Defect code DEF-MICRO-88; 18% surface porosity defect rate",
                "confidence": 0.97,
                "source": "VISION_AI_INSP",
                "record_id": "REC-EVT-106"
            },
            {
                "event_id": "EVT-107",
                "batch_id": batch_id,
                "source_system": "MES",
                "event_type": "BATCH_REJECTED",
                "timestamp": "2026-07-25T13:30:00Z",
                "stage": "Disposition",
                "severity": "CRITICAL",
                "value": "Batch rejected; Final yield 82.0%",
                "confidence": 1.0,
                "source": "MES_DB",
                "record_id": "REC-EVT-107"
            }
        ],
        "quality_records": [
            {
                "inspection_id": "INSP-9001",
                "batch_id": batch_id,
                "stage": "Final Inspection",
                "defect_code": "DEF-MICRO-88",
                "pass_fail": "FAIL",
                "severity": "CRITICAL",
                "source": "QUALITY_LAB",
                "record_id": "REC-INSP-9001",
                "timestamp": "2026-07-25T12:15:00Z"
            }
        ]
    }

def create_healthy_reference_batch_data() -> Dict[str, Any]:
    batch_id = "BATCH-REF-2026-06"
    return {
        "batch": {
            "batch_id": batch_id,
            "product": "Precision Alloy Casing X4",
            "line": "Line 3",
            "plant": "Plant Alpha - Detroit",
            "start_time": "2026-07-24T06:00:00Z",
            "end_time": "2026-07-24T12:30:00Z",
            "yield_pct": 97.2,
            "baseline_yield_pct": 96.0,
            "status": "APPROVED",
            "source": "MES_PROD_DB",
            "record_id": "REC-BATCH-REF-06",
            "timestamp": "2026-07-24T12:30:00Z"
        },
        "materials": {
            "material_id": "MAT-LOT-8830",
            "material_name": "High-Grade Titanium Resin Blend",
            "supplier": "AeroMaterials Corp",
            "lot_number": "LOT-8830-A",
            "formulation": "v3.2-Standard",
            "storage_condition": "Climate-controlled staging (42% RH)",
            "source": "ERP_INV_SYS",
            "record_id": "REC-MAT-8830",
            "timestamp": "2026-07-24T05:45:00Z"
        },
        "machine": {
            "machine_id": "M7-CNC-MILL",
            "name": "Machine 7 - Multi-Axis CNC Mill",
            "line": "Line 3",
            "maintenance_state": "HEALTHY",
            "alert_history": [],
            "source": "SCADA_MNT_LOG",
            "record_id": "REC-M7-STATE-REF",
            "timestamp": "2026-07-24T06:00:00Z"
        },
        "sensor_readings": [
            {
                "reading_id": "SR-REF-01",
                "batch_id": batch_id,
                "timestamp": "2026-07-24T06:30:00Z",
                "humidity_pct": 42.0,
                "temperature_c": 21.8,
                "pressure_bar": 4.0,
                "queue_delay_minutes": 12.0,
                "cycle_time_seconds": 52.0,
                "source": "SCADA_IOT_SENSORS",
                "record_id": "REC-SR-REF-01"
            },
            {
                "reading_id": "SR-REF-02",
                "batch_id": batch_id,
                "timestamp": "2026-07-24T09:00:00Z",
                "humidity_pct": 43.1,
                "temperature_c": 22.0,
                "pressure_bar": 4.0,
                "queue_delay_minutes": 14.0,
                "cycle_time_seconds": 53.0,
                "source": "SCADA_IOT_SENSORS",
                "record_id": "REC-SR-REF-02"
            }
        ],
        "events": [
            {
                "event_id": "EVT-REF-01",
                "batch_id": batch_id,
                "source_system": "MES",
                "event_type": "BATCH_STARTED",
                "timestamp": "2026-07-24T06:00:00Z",
                "stage": "Staging",
                "severity": "INFO",
                "value": "Nominal startup",
                "confidence": 1.0,
                "source": "MES_DB",
                "record_id": "REC-EVT-REF-01"
            },
            {
                "event_id": "EVT-REF-02",
                "batch_id": batch_id,
                "source_system": "MES",
                "event_type": "BATCH_COMPLETED",
                "timestamp": "2026-07-24T12:30:00Z",
                "stage": "Disposition",
                "severity": "INFO",
                "value": "Batch approved; Yield 97.2%",
                "confidence": 1.0,
                "source": "MES_DB",
                "record_id": "REC-EVT-REF-02"
            }
        ],
        "quality_records": [
            {
                "inspection_id": "INSP-REF-8820",
                "batch_id": batch_id,
                "stage": "Final Inspection",
                "defect_code": None,
                "pass_fail": "PASS",
                "severity": "NONE",
                "source": "QUALITY_LAB",
                "record_id": "REC-INSP-REF-8820",
                "timestamp": "2026-07-24T12:10:00Z"
            }
        ]
    }

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    # Save Operating Ranges
    with open(os.path.join(data_dir, "operating_ranges.json"), "w") as f:
        json.dump(create_operating_ranges(), f, indent=2)

    # Save Incident Batch
    with open(os.path.join(data_dir, "incident_batch.json"), "w") as f:
        json.dump(create_incident_batch_data(), f, indent=2)

    # Save Reference Batch
    with open(os.path.join(data_dir, "healthy_reference_batch.json"), "w") as f:
        json.dump(create_healthy_reference_batch_data(), f, indent=2)

    print("All fixtures successfully generated in data/ directory!")

if __name__ == "__main__":
    main()
