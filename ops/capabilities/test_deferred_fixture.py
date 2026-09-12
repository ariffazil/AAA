"""Fixture test: deferred capabilities report truthful non-error states.

A deferred capability must never be treated as a false alarm. It reports
unreachable / intentionally_unreachable with its activation gate; external
writes carry confirmation_required + non_autonomous flags; financial writes
carry the sovereign human veto. This is the "no improvised fallback write" gate.
"""

import unittest
import yaml
from pathlib import Path

DIR = Path(__file__).resolve().parent
LEDGER_PATH = DIR / "capability-ledger.yaml"


def load_ledger():
    with open(LEDGER_PATH) as f:
        return yaml.safe_load(f)


CAPS = {c["id"]: c for c in load_ledger()["capabilities"]}


class TestDeferredCapabilities(unittest.TestCase):
    def test_email_read_is_deferred_gated_observe(self):
        cap = CAPS["communication.email.read"]
        self.assertEqual(cap["lifecycle"], "deferred")
        self.assertEqual(cap["reachability"]["state"], "unreachable")
        self.assertEqual(cap["governance"]["authority"], "observe")
        self.assertEqual(cap["governance"]["activation_gate"], "888_HOLD")

    def test_email_send_requires_confirmation_non_autonomous(self):
        cap = CAPS["communication.email.send"]
        self.assertEqual(cap["governance"]["authority"], "external_write")
        self.assertTrue(cap["governance"]["confirmation_required"])
        self.assertTrue(cap["governance"]["non_autonomous"])
        self.assertEqual(cap["governance"]["activation_gate"], "888_HOLD")

    def test_payments_is_sovereign_veto_intentionally_unreachable(self):
        cap = CAPS["payments.duitnow_fpx"]
        self.assertEqual(cap["reachability"]["state"], "intentionally_unreachable")
        self.assertEqual(cap["governance"]["authority"], "financial_write")
        self.assertEqual(cap["governance"]["activation_gate"], "F13_888_HOLD")
        self.assertTrue(cap["governance"]["sovereign_human_veto"])

    def test_social_listening_gated_888_hold(self):
        cap = CAPS["intelligence.social.listening"]
        self.assertEqual(cap["reachability"]["state"], "intentionally_unreachable")
        self.assertEqual(cap["governance"]["activation_gate"], "888_HOLD")


if __name__ == "__main__":
    unittest.main()
