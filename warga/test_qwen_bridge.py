#!/usr/bin/env python3
"""
test_qwen_bridge.py — Tier-1 unit tests (pure functions, no I/O, no network)
═══════════════════════════════════════════════════════════════════════════════════════

Tests two pure functions in qwen_bridge.py:
    1. compile_policy(lease)   — lease → acpx permission policy
    2. classify_event(event)   — JSON-RPC event → arifOS-shaped record

Run: python3 /root/AAA/warga/test_qwen_bridge.py
Exit: 0 = all pass, 1 = any fail
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

# Make the bridge module importable.
sys.path.insert(0, str(Path(__file__).parent))
import qwen_bridge as qb  # noqa: E402


class TestCompilePolicy(unittest.TestCase):
    """compile_policy must map AAA lease.scope to acpx permission policy correctly."""

    def test_observe_only_is_fail_closed(self):
        lease = {"scope": "OBSERVE_ONLY", "reversibility": "REVERSIBLE", "max_turns": 5, "ttl_seconds": 300}
        p = qb.compile_policy(lease)
        self.assertEqual(p["bridgeFloor"], "OBSERVE_ONLY")
        self.assertEqual(p["defaultAction"], "escalate")
        self.assertIn("write_file", p["autoDeny"])
        self.assertIn("read_file", p["autoApprove"])
        self.assertEqual(p["schema_version"], "qwen-bridge.policy.v1")
        self.assertFalse(p["thoughtStreamAllowed"])

    def test_standard_allows_writes(self):
        lease = {"scope": "STANDARD", "reversibility": "REVERSIBLE", "max_turns": 10, "ttl_seconds": 600}
        p = qb.compile_policy(lease)
        self.assertEqual(p["bridgeFloor"], "STANDARD")
        self.assertEqual(p["defaultAction"], "approve")
        self.assertNotIn("write_file", p["autoDeny"])

    def test_irreversible_forces_escalate(self):
        # Even at STANDARD scope, irreversible actions must escalate.
        lease = {"scope": "STANDARD", "reversibility": "IRREVERSIBLE", "max_turns": 3, "ttl_seconds": 120}
        p = qb.compile_policy(lease)
        self.assertEqual(p["defaultAction"], "escalate")

    def test_thought_stream_consent(self):
        lease = {"scope": "OBSERVE_ONLY", "reversibility": "REVERSIBLE",
                 "max_turns": 5, "ttl_seconds": 300,
                 "consent": {"thought_stream": True}}
        p = qb.compile_policy(lease)
        self.assertTrue(p["thoughtStreamAllowed"])

    def test_unknown_scope_rejected(self):
        with self.assertRaises(ValueError):
            qb.compile_policy({"scope": "WILDLY_PERMISSIVE"})

    def test_policy_is_json_serializable(self):
        lease = {"scope": "OBSERVE_ONLY", "reversibility": "REVERSIBLE", "max_turns": 5, "ttl_seconds": 300}
        p = qb.compile_policy(lease)
        # If this raises, the policy will break acpx.
        s = json.dumps(p)
        self.assertIsInstance(json.loads(s), dict)


class TestClassifyEvent(unittest.TestCase):
    """classify_event must map JSON-RPC events to truth classes correctly."""

    def test_initialize_is_obs(self):
        e = {"method": "initialize", "params": {"protocolVersion": 1}}
        r = qb.classify_event(e)
        self.assertEqual(r["truth_class"], "OBS")
        self.assertEqual(r["kind"], "agent_initialize")

    def test_session_new_is_obs(self):
        e = {"method": "session/new", "result": {"sessionId": "x"}}
        r = qb.classify_event(e)
        self.assertEqual(r["truth_class"], "OBS")
        self.assertEqual(r["kind"], "agent_session_new")

    def test_available_commands_is_obs(self):
        e = {"method": "session/update", "params": {"update": {"sessionUpdate": "available_commands_update"}}}
        r = qb.classify_event(e)
        self.assertEqual(r["truth_class"], "OBS")
        self.assertEqual(r["kind"], "agent_capability_surface")

    def test_thought_chunk_is_der(self):
        e = {"method": "session/update", "params": {"update": {"sessionUpdate": "agent_thought_chunk"}}}
        r = qb.classify_event(e)
        self.assertEqual(r["truth_class"], "DER")
        self.assertEqual(r["kind"], "agent_thought_chunk")

    def test_message_chunk_defaults_to_int(self):
        e = {"method": "session/update", "params": {"update": {"sessionUpdate": "agent_message_chunk"}}}
        r = qb.classify_event(e)
        self.assertEqual(r["truth_class"], "INT")
        self.assertEqual(r["kind"], "agent_message_chunk")

    def test_usage_update_is_obs(self):
        e = {"method": "session/update", "params": {"update": {"sessionUpdate": "usage_update"}}}
        r = qb.classify_event(e)
        self.assertEqual(r["truth_class"], "OBS")
        self.assertEqual(r["kind"], "agent_usage_update")

    def test_unknown_event_is_spec(self):
        e = {"method": "future_event_we_havent_seen", "params": {}}
        r = qb.classify_event(e)
        self.assertEqual(r["truth_class"], "SPEC")
        self.assertTrue(r["kind"].startswith("unknown_"))

    def test_result_event_is_obs(self):
        e = {"result": {"stopReason": "end_turn"}}
        r = qb.classify_event(e)
        self.assertEqual(r["truth_class"], "OBS")
        self.assertEqual(r["kind"], "agent_result")


if __name__ == "__main__":
    # Minimal runner so we don't require pytest.
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCompilePolicy)
    suite.addTests(loader.loadTestsFromTestCase(TestClassifyEvent))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)