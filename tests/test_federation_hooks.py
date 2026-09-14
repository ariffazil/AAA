#!/usr/bin/env python3
"""
test_federation_hooks.py — Conformance and Validation Suite for Federation Hook Engine
Canonical Path: /root/AAA/tests/test_federation_hooks.py

Verifies:
  1. Boot phase initialization, token binding, and active scar priming
  2. Gate phase unconditional pass-through for read/probe/bootstrap
  3. Gate phase auto-minting reflex for mutating tools
  4. Monotonicity ladder invariant (restriction cannot degrade downstream)
  5. Forbidden target escalation (e.g., /etc/shadow -> VOID)
  6. Post-tool auto-healing on HTTP 406 content negotiation
  7. Post-tool auto-healing on missing dependency and swap exhaustion
  8. Turn metabolize anti-tangguh sentry tripwire
  9. Turn metabolize autonomous scar crystallization
 10. Session seal generational carry-forward append and vault stamp
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add hook engine library path
sys.path.insert(0, "/root/AAA/hooks/lib")
from federation_hook_engine import (
    FederationHookEngine,
    HookPhase,
    RestrictionLevel,
    UNCONDITIONAL_PASS_TOOLS,
)


class TestFederationHookEngine(unittest.TestCase):
    def setUp(self):
        self.engine = FederationHookEngine(actor_id="333-AGI", session_id="test-session-001")

    def test_01_boot_initialization_and_scar_priming(self):
        """Phase 0: Boot must bind token and prime context with active scars."""
        res = self.engine.boot()
        self.assertEqual(res["phase"], HookPhase.BOOT.value)
        self.assertEqual(res["status"], "OK")
        self.assertIsNotNone(res["session_token"])
        self.assertTrue(len(res["session_token"]) > 0)
        self.assertIn("Active Constraint Brief", res["brief"])
        self.assertIn("F1 Amanah", res["brief"])
        self.assertIn("MUBAH", res["brief"])
        # Verify scars were loaded if scars dir exists
        self.assertGreaterEqual(res["scars_count"], 0)

    def test_02_gate_unconditional_pass_through(self):
        """Phase 1: arif_init and read tools must pass unconditionally without token checks."""
        for tool in ["arif_init", "read", "view_file", "glob", "grep_search", "forge_probe"]:
            gate_res = self.engine.gate(tool_name=tool, tool_args={"path": "/root/test"})
            self.assertEqual(gate_res["verdict"], "ALLOW")
            self.assertEqual(gate_res["phase"], HookPhase.GATE.value)
            self.assertIn("read/probe/bootstrap pass-through", gate_res["reason"])

    def test_03_gate_auto_mint_on_missing_token(self):
        """Phase 1: Mutating tool without an active session token must auto-mint an ACT token."""
        engine_no_token = FederationHookEngine(actor_id="555-ASI", session_id="test-session-002")
        self.assertIsNone(engine_no_token.session_token)

        gate_res = engine_no_token.gate(
            tool_name="write_to_file",
            tool_args={"TargetFile": "/root/test.txt", "CodeContent": "hello"},
            provided_token=None,
        )
        self.assertEqual(gate_res["verdict"], "ALLOW")
        self.assertTrue(gate_res["auto_minted"])
        self.assertIsNotNone(gate_res["session_token"])
        self.assertTrue(gate_res["session_token"].startswith("act-minted-555-ASI"))
        self.assertIsNotNone(gate_res.get("journal_id"))

    def test_04_monotonic_restriction_ladder(self):
        """Phase 1: Restriction level must never be degraded downstream."""
        engine = FederationHookEngine(actor_id="333-AGI")
        self.assertEqual(engine.current_restriction, RestrictionLevel.ALLOW)

        # Escalate to HOLD
        gate_res1 = engine.gate(
            tool_name="bash",
            tool_args={"command": "rm -rf /"},
            incoming_restriction="HOLD",
        )
        self.assertEqual(gate_res1["verdict"], "HOLD")
        self.assertEqual(engine.current_restriction, RestrictionLevel.HOLD)

        # Subsequent request with lower restriction 'ALLOW' must be rejected / kept at HOLD
        gate_res2 = engine.gate(
            tool_name="bash",
            tool_args={"command": "ls -la"},
            incoming_restriction="ALLOW",
        )
        self.assertEqual(gate_res2["verdict"], "HOLD")
        self.assertEqual(engine.current_restriction, RestrictionLevel.HOLD)

    def test_05_gate_forbidden_target_escalation(self):
        """Phase 1: Mutating forbidden target (e.g. /etc/shadow) must ratchet to VOID."""
        engine = FederationHookEngine(actor_id="333-AGI")
        gate_res = engine.gate(
            tool_name="replace_file_content",
            tool_args={"TargetFile": "/etc/shadow", "ReplacementContent": "root:x:"},
        )
        self.assertEqual(gate_res["verdict"], "VOID")
        self.assertEqual(engine.current_restriction, RestrictionLevel.VOID)
        self.assertIn("forbidden target", gate_res["reason"].lower())

    def test_06_heal_http_406_content_negotiation(self):
        """Phase 2: HTTP 406 must trigger auto-healing with Accept: application/json fix."""
        heal_res = self.engine.heal(
            tool_name="run_command",
            tool_args={"url": "http://127.0.0.1:8088/kernel/call"},
            exit_code=1,
            http_status=406,
            error_message="HTTP 406 Not Acceptable",
        )
        self.assertTrue(heal_res["remediated"])
        self.assertTrue(heal_res["auto_retry"])
        self.assertEqual(heal_res["healing_action"]["type"], "HTTP_406_CONTENT_NEGOTIATION")
        self.assertIn("Accept: application/json", heal_res["healing_action"]["fix"])

    def test_07_heal_missing_dependency(self):
        """Phase 2: Missing module/binary must trigger dependency diagnosis."""
        heal_res = self.engine.heal(
            tool_name="bash",
            exit_code=127,
            stderr="bash: jq: command not found",
        )
        self.assertTrue(heal_res["remediated"])
        self.assertEqual(heal_res["healing_action"]["type"], "DEPENDENCY_MISSING")
        self.assertEqual(heal_res["healing_action"]["target"], "jq")

    def test_08_metabolize_anti_tangguh_sentry(self):
        """Phase 3: Permission-seeking on digital work must trigger Anti-Tangguh tripwire."""
        # Case A: Anti-pattern detected
        res_ask = self.engine.metabolize(
            assistant_text="I have prepared the code. Shall I proceed to execute it?",
            turn_index=2,
        )
        self.assertTrue(res_ask["anti_tangguh_tripwire"])
        self.assertIn("TRIPWIRE", res_ask["instruction"])

        # Case B: Malaysian dialect anti-pattern
        res_ask_bm = self.engine.metabolize(
            assistant_text="Semua fail dah ready. Jalan?",
            turn_index=3,
        )
        self.assertTrue(res_ask_bm["anti_tangguh_tripwire"])

        # Case C: Clean declarative execution response
        res_clean = self.engine.metabolize(
            assistant_text="Executed test suite. All 10 tests passed with exit code 0.",
            turn_index=4,
        )
        self.assertFalse(res_clean["anti_tangguh_tripwire"])
        self.assertEqual(res_clean["instruction"], "CLEAR")

    def test_09_metabolize_autonomous_scar_crystallization(self):
        """Phase 3: Recurring errors (>= 2) must trigger scar crystallization."""
        engine = FederationHookEngine(actor_id="333-AGI", session_id="test-scar-session")
        # Simulate repeating tool error twice
        engine.heal(
            tool_name="git_commit",
            exit_code=1,
            stderr="fatal: refusing to merge unrelated histories",
        )
        engine.heal(
            tool_name="git_commit",
            exit_code=1,
            stderr="fatal: refusing to merge unrelated histories",
        )
        metabolize_res = engine.metabolize(assistant_text="Processing next step.", turn_index=5)
        # Should have detected and crystallized a recurring scar
        self.assertTrue(metabolize_res["new_scar_created"])
        self.assertIsNotNone(metabolize_res["created_scar"])

    def test_10_seal_generational_carry_forward(self):
        """Phase 4: Seal must append entry and stamp seal receipt."""
        seal_res = self.engine.seal(
            verdict="ALL_SYSTEMS_GO",
            completed_tasks=["Task A: Deployed OpenAPI", "Task B: Patched Hooks"],
            open_loops=["Loop 1: Monitor external indexers"],
        )
        self.assertEqual(seal_res["phase"], HookPhase.SEAL.value)
        self.assertEqual(seal_res["status"], "SEALED")
        self.assertIsNotNone(seal_res["seal_id"])
        self.assertEqual(seal_res["completed_count"], 2)
        self.assertEqual(seal_res["open_loops_count"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
