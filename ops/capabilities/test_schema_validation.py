"""Unit test: capability ledger validates against its JSON Schema.

Verifies the ledger is structurally coherent — the three-dimension model
(implementation / reachability / governance) is present and enum-legal per
capability-ledger.schema.json. This is the "implemented != reachable != governed"
machine gate: a structurally broken ledger must fail here before any probe runs.
"""

import json
import unittest
import yaml
from pathlib import Path
import jsonschema

DIR = Path(__file__).resolve().parent
LEDGER_PATH = DIR / "capability-ledger.yaml"
SCHEMA_PATH = DIR / "capability-ledger.schema.json"


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


class TestLedgerSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = load_yaml(LEDGER_PATH)
        cls.schema = json.loads(SCHEMA_PATH.read_text())

    def test_ledger_validates_against_json_schema(self):
        jsonschema.validate(type(self).ledger, type(self).schema)

    def test_top_level_metadata_present(self):
        for field in ("ledger_version", "capabilities"):
            self.assertIn(field, type(self).ledger, f"missing top-level {field}")

    def test_every_capability_has_three_dimensions(self):
        for cap in type(self).ledger["capabilities"]:
            for dim in ("implementation", "reachability", "governance"):
                self.assertIn(dim, cap, f"{cap.get('id')} missing dimension {dim}")

    def test_capability_ids_unique_and_namespaced(self):
        ids = [c["id"] for c in type(self).ledger["capabilities"]]
        self.assertEqual(len(ids), len(set(ids)), "duplicate capability ids")
        for cid in ids:
            self.assertRegex(cid, r"^[a-z][a-z0-9_.]*$", f"bad id: {cid}")


if __name__ == "__main__":
    unittest.main()
