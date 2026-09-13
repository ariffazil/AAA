"""
test_admissibility.py — Test suite for MemoryAdmissibilityGate
Validates SRO v1 policy against synthetic fixtures and live Qdrant collection samples.
"""

import os
import sys
import json
import unittest
import urllib.request
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from admissibility_gate import MemoryAdmissibilityGate


class TestMemoryAdmissibility(unittest.TestCase):
    def setUp(self):
        self.gate = MemoryAdmissibilityGate()
        self.now = datetime.now(timezone.utc)

    def test_active_memory_operational(self):
        point = {
            "id": "mem_active_01",
            "payload": {
                "content": "Malay Basin B-sands verified clean reservoir facies.",
                "truth_class": {"class": "OBS", "confidence": 0.95},
                "sro": {
                    "sro_version": 1,
                    "expiry": {
                        "status": "ACTIVE",
                        "expires_at": (self.now + timedelta(days=100)).isoformat(),
                        "review_by": (self.now + timedelta(days=70)).isoformat()
                    },
                    "supersession": {"supersedes": None, "superseded_by": None},
                    "calibration": {"confidence_at_creation": 0.95}
                }
            }
        }
        res = self.gate.evaluate(point, mode="operational_default", current_time=self.now)
        self.assertTrue(res["admissible"])
        self.assertEqual(res["code"], "ADMISSIBLE")
        self.assertEqual(res["effective_status"], "ACTIVE")

    def test_expired_by_status(self):
        point = {
            "id": "mem_exp_status",
            "payload": {
                "sro": {
                    "sro_version": 1,
                    "expiry": {"status": "EXPIRED", "expires_at": None},
                    "supersession": {"superseded_by": None}
                }
            }
        }
        res = self.gate.evaluate(point, mode="operational_default", current_time=self.now)
        self.assertFalse(res["admissible"])
        self.assertEqual(res["code"], "EXCLUDED_EXPIRED")

    def test_expired_by_past_timestamp(self):
        point = {
            "id": "mem_past_dt",
            "payload": {
                "sro": {
                    "sro_version": 1,
                    "expiry": {
                        "status": "ACTIVE",  # status flag not yet flipped
                        "expires_at": (self.now - timedelta(days=5)).isoformat()
                    },
                    "supersession": {"superseded_by": None}
                }
            }
        }
        res = self.gate.evaluate(point, mode="operational_default", current_time=self.now)
        self.assertFalse(res["admissible"])
        self.assertEqual(res["code"], "EXCLUDED_EXPIRED")
        self.assertEqual(res["effective_status"], "EXPIRED")

    def test_superseded_memory(self):
        point = {
            "id": "mem_superseded",
            "payload": {
                "sro": {
                    "sro_version": 1,
                    "expiry": {"status": "ACTIVE", "expires_at": (self.now + timedelta(days=50)).isoformat()},
                    "supersession": {"superseded_by": "mem_newer_02"}
                }
            }
        }
        res = self.gate.evaluate(point, mode="operational_default", current_time=self.now)
        self.assertFalse(res["admissible"])
        self.assertEqual(res["code"], "EXCLUDED_SUPERSEDED")
        self.assertEqual(res["superseded_by"], "mem_newer_02")

    def test_low_confidence_exclusion(self):
        point = {
            "id": "mem_low_conf",
            "payload": {
                "truth_class": {"class": "OBS", "confidence": 0.85},  # OBS requires 0.90
                "sro": {
                    "sro_version": 1,
                    "expiry": {"status": "ACTIVE", "expires_at": (self.now + timedelta(days=50)).isoformat()},
                    "supersession": {"superseded_by": None}
                }
            }
        }
        res = self.gate.evaluate(point, mode="operational_default", current_time=self.now)
        self.assertFalse(res["admissible"])
        self.assertEqual(res["code"], "EXCLUDED_LOW_CONFIDENCE")

    def test_schema_invalid_exclusion(self):
        point = {"id": "mem_unmigrated", "payload": {"content": "raw content without sro"}}
        res = self.gate.evaluate(point, mode="operational_default")
        self.assertFalse(res["admissible"])
        self.assertEqual(res["code"], "EXCLUDED_SCHEMA_INVALID")

    def test_historical_mode_admissibility(self):
        point = {
            "id": "mem_historical_test",
            "payload": {
                "sro": {
                    "sro_version": 1,
                    "expiry": {"status": "EXPIRED"},
                    "supersession": {"superseded_by": "mem_target_09"}
                }
            }
        }
        res = self.gate.evaluate(point, mode="historical_lineage")
        self.assertTrue(res["admissible"])
        self.assertEqual(res["code"], "ADMISSIBLE_HISTORICAL")
        self.assertIn("RETRIEVED_UNDER_HISTORICAL_AUDIT_MODE", res["historical_banner"])

    def test_live_qdrant_collection_admissibility(self):
        """Verify the live points in arifos_memory against the gate.
        Note: On 2026-09-12T05:50Z, 333-AGI remediated arifos_memory, archiving 59
        points into forge_work/memory-remediation-backup-20260912.json.
        Live collection holds 40 points (9 ACTIVE / 31 EXPIRED).
        """
        try:
            req = urllib.request.Request(
                "http://127.0.0.1:6333/collections/arifos_memory/points/scroll",
                data=json.dumps({"limit": 200, "with_payload": True, "with_vector": False}).encode(),
                headers={"Content-Type": "application/json"}
            )
            res = json.loads(urllib.request.urlopen(req, timeout=3).read())
            points = res.get("result", {}).get("points", [])
        except Exception as e:
            self.skipTest(f"Qdrant not reachable: {e}")

        # Post-remediation reality check (40 points remain in active collection)
        self.assertEqual(len(points), 40)

        operational_admissible = 0
        operational_excluded = 0
        historical_admissible = 0

        for p in points:
            op_eval = self.gate.evaluate(p, mode="operational_default")
            if op_eval["admissible"]:
                operational_admissible += 1
            else:
                operational_excluded += 1
                self.assertIn(op_eval["code"], ("EXCLUDED_EXPIRED", "EXCLUDED_LOW_CONFIDENCE", "EXCLUDED_SUPERSEDED", "EXCLUDED_SANCTUARY"))

            hist_eval = self.gate.evaluate(p, mode="historical_lineage")
            if hist_eval["admissible"]:
                historical_admissible += 1

        # 31 expired legacy points must be excluded from operational mode; 9 active admitted
        # 31 EXPIRED + 2 sanctuary denylist (F9) = 33 excluded operationally
        self.assertEqual(operational_excluded, 33)
        self.assertEqual(operational_admissible, 7)
        # Sanctuary IDs are denied in historical mode too
        self.assertEqual(historical_admissible, 38)


if __name__ == "__main__":
    unittest.main()
