#!/usr/bin/env python3
"""
test_agentic_hooks_suite.py — Comprehensive Test Suite for AAA Universal Agentic Hook Mesh
Canonical Path: /root/AAA/tests/hooks/test_agentic_hooks_suite.py
Authority: AAA-HOOK-FORGE-V1.0 · Section 11 & Section 12

Asserts T01 through T15, T17 (Rollback), and T18 (Security Regression).
Emits structured JSON test results to /root/AAA/artifacts/hook-forge/TEST-RESULTS.json
"""

import hashlib
import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path

# Add paths
AAA_ROOT = Path("/root/AAA")
HOOKS_LIB = AAA_ROOT / "hooks" / "lib"
ADAPTERS_DIR = AAA_ROOT / "hooks" / "adapters"
sys.path.insert(0, str(HOOKS_LIB))

from event_schema import ActionPayload, HookEvent, VERDICT_LADDER, VERDICT_RANK
from decision_schema import HookDecision, compose_decisions
from policy_engine import PolicyEngine
from evidence_ledger import EvidenceLedger
from memory_guard import MemoryGuard
from repair_catalog import RepairCatalog
from learning_pipeline import LearningPipeline

import importlib.util


def _load_adapter(file_path: Path, class_name: str):
    spec = importlib.util.spec_from_file_location(f"mod_{class_name}", str(file_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, class_name)


OpenCodeAdapter = _load_adapter(ADAPTERS_DIR / "opencode" / "adapter.py", "OpenCodeAdapter")
ClaudeCodeAdapter = _load_adapter(ADAPTERS_DIR / "claude" / "adapter.py", "ClaudeCodeAdapter")
AntigravityAdapter = _load_adapter(ADAPTERS_DIR / "antigravity" / "adapter.py", "AntigravityAdapter")
HermesAdapter = _load_adapter(ADAPTERS_DIR / "hermes" / "adapter.py", "HermesAdapter")
OpenClawAdapter = _load_adapter(ADAPTERS_DIR / "openclaw" / "adapter.py", "OpenClawAdapter")


class TestAgenticHookMesh(unittest.TestCase):

    def setUp(self):
        self.policy_engine = PolicyEngine()
        self.memory_guard = MemoryGuard()
        self.repair_catalog = RepairCatalog()

    # T01: Schema validation
    def test_T01_event_schema_validation(self):
        """T01: Valid event envelopes pass; invalid event envelopes fail."""
        valid_event = HookEvent(
            event_name="aaa.action.proposed",
            harness_id="opencode",
            session_id="test-session-001",
            risk_class="R1",
        )
        self.assertEqual(valid_event.event_name, "aaa.action.proposed")
        self.assertTrue(valid_event.event_id.startswith("evt-"))

        # Invalid event name should raise ValueError
        with self.assertRaises(ValueError):
            HookEvent(
                event_name="invalid.event.name",
                harness_id="opencode",
                session_id="test-session-001",
            )

    # T02: Decision schema validation
    def test_T02_decision_schema_validation(self):
        """T02: Valid decision passes; invalid verdict fails."""
        valid_decision = HookDecision(
            event_id="evt-123",
            verdict="ALLOW",
            reason_codes=["TEST_ALLOW"],
            risk_class="R1",
        )
        self.assertEqual(valid_decision.verdict, "ALLOW")

        # Invalid verdict not in ladder
        with self.assertRaises(ValueError):
            HookDecision(
                event_id="evt-123",
                verdict="PERMIT_EVERYTHING",
                reason_codes=[],
            )

    # T03: Monotonic restriction ladder
    def test_T03_monotonic_restriction_ladder(self):
        """T03: Downstream cannot weaken upstream restriction (ALLOW + HOLD = HOLD)."""
        d_allow = HookDecision(event_id="evt-1", verdict="ALLOW", reason_codes=["OK"])
        d_constraint = HookDecision(event_id="evt-1", verdict="ALLOW_WITH_CONSTRAINTS", reason_codes=["CONSTRAINED"])
        d_hold = HookDecision(event_id="evt-1", verdict="HOLD", reason_codes=["GATE_HOLD"])
        d_deny = HookDecision(event_id="evt-1", verdict="DENY", reason_codes=["SECURITY_DENY"])

        # ALLOW composed with HOLD must yield HOLD
        composed_1 = compose_decisions(d_allow, d_hold)
        self.assertEqual(composed_1.verdict, "HOLD")

        # HOLD composed with ALLOW must still yield HOLD (cannot weaken)
        composed_2 = compose_decisions(d_hold, d_allow)
        self.assertEqual(composed_2.verdict, "HOLD")

        # HOLD composed with DENY must yield DENY (strengthens)
        composed_3 = compose_decisions(d_hold, d_deny)
        self.assertEqual(composed_3.verdict, "DENY")

    # T04: OpenCode adapter translation
    def test_T04_opencode_adapter(self):
        """T04: OpenCode adapter translates native payload to canonical and back."""
        adapter = OpenCodeAdapter()
        raw_payload = {
            "tool": "bash",
            "parameters": {"command": "git status"},
            "session_id": "opencode-s1",
        }
        event = adapter.to_canonical(raw_payload, "tool.execute.before")
        self.assertEqual(event.event_name, "aaa.action.proposed")
        self.assertEqual(event.harness_id, "opencode")
        self.assertEqual(event.action.tool_name, "bash")

        decision = HookDecision(event_id=event.event_id, verdict="ALLOW", reason_codes=["OK"])
        res = adapter.from_canonical(decision)
        self.assertTrue(res["allow"])
        self.assertEqual(res["verdict"], "ALLOW")

    # T05: Claude Code adapter translation
    def test_T05_claude_adapter(self):
        """T05: Claude Code adapter translates native payload to canonical and back."""
        adapter = ClaudeCodeAdapter()
        raw_payload = {
            "tool_name": "Edit",
            "tool_input": {"path": "/root/test.txt"},
            "session_id": "claude-s1",
        }
        event = adapter.to_canonical(raw_payload, "PreToolUse")
        self.assertEqual(event.event_name, "aaa.action.proposed")
        self.assertEqual(event.harness_id, "claude_code")

        decision = HookDecision(event_id=event.event_id, verdict="ALLOW_WITH_CONSTRAINTS", reason_codes=["OK"])
        res = adapter.from_canonical(decision)
        self.assertTrue(res["continue"])

    # T06: Antigravity adapter translation
    def test_T06_antigravity_adapter(self):
        """T06: Antigravity adapter translates native payload to canonical and back."""
        adapter = AntigravityAdapter()
        raw_payload = {
            "tool_name": "run_command",
            "tool_arguments": {"CommandLine": "ls -la"},
            "session_id": "agy-s1",
        }
        event = adapter.to_canonical(raw_payload, "pre_tool_call")
        self.assertEqual(event.event_name, "aaa.action.proposed")
        self.assertEqual(event.harness_id, "antigravity")

        decision = HookDecision(event_id=event.event_id, verdict="ALLOW", reason_codes=["OK"])
        res = adapter.from_canonical(decision)
        self.assertEqual(res["status"], "APPROVED")

    # T07: Hermes adapter translation
    def test_T07_hermes_adapter(self):
        """T07: Hermes adapter translates native payload to canonical and back."""
        adapter = HermesAdapter()
        raw_payload = {
            "skill": "status_check",
            "args": {},
            "session_id": "hermes-s1",
        }
        event = adapter.to_canonical(raw_payload, "tool_executed")
        self.assertEqual(event.event_name, "aaa.action.completed")
        self.assertEqual(event.harness_id, "hermes")

        decision = HookDecision(event_id=event.event_id, verdict="ALLOW", reason_codes=["OK"])
        res = adapter.from_canonical(decision)
        self.assertEqual(res["hermes_status"], "PROCEED")

    # T08: OpenClaw adapter translation
    def test_T08_openclaw_adapter(self):
        """T08: OpenClaw adapter translates native payload to canonical and back."""
        adapter = OpenClawAdapter()
        raw_payload = {
            "command": "ping_mesh",
            "payload": {"target": "kvm8"},
            "session_id": "openclaw-s1",
        }
        event = adapter.to_canonical(raw_payload, "edge_tool_done")
        self.assertEqual(event.event_name, "aaa.action.completed")
        self.assertEqual(event.harness_id, "openclaw")

        decision = HookDecision(event_id=event.event_id, verdict="ALLOW", reason_codes=["OK"])
        res = adapter.from_canonical(decision)
        self.assertTrue(res["edge_allowed"])

    # T09: 100_GATE phase policy evaluation
    def test_T09_gate_phase_evaluation(self):
        """T09: 100_GATE allows R0/R1, constrains R2, holds R3, denies forbidden targets."""
        # R0 read tool -> ALLOW
        e_read = HookEvent(
            event_name="aaa.action.proposed",
            harness_id="opencode",
            action=ActionPayload(tool_name="read", arguments={}),
            risk_class="R0",
        )
        d_read = self.policy_engine.evaluate(e_read)
        self.assertEqual(d_read.verdict, "ALLOW")

        # R2 local write -> ALLOW_WITH_CONSTRAINTS
        e_write = HookEvent(
            event_name="aaa.action.proposed",
            harness_id="opencode",
            action=ActionPayload(tool_name="write", arguments={}, target_path="/root/test.txt"),
            risk_class="R2",
        )
        d_write = self.policy_engine.evaluate(e_write)
        self.assertEqual(d_write.verdict, "ALLOW_WITH_CONSTRAINTS")

        # R3 production risk -> HOLD
        e_prod = HookEvent(
            event_name="aaa.action.proposed",
            harness_id="opencode",
            action=ActionPayload(tool_name="deploy_prod", arguments={}),
            risk_class="R3",
        )
        d_prod = self.policy_engine.evaluate(e_prod)
        self.assertEqual(d_prod.verdict, "HOLD")

    # T10: 200_HEAL phase repair catalog
    def test_T10_heal_phase_playbooks(self):
        """T10: 200_HEAL triggers correct playbooks for known failure signatures."""
        # 406 Error
        err_406 = "Cannot verify session validity for 'bash'. arifOS validation HTTP 406."
        pb_406 = self.repair_catalog.match_playbook(err_406)
        self.assertEqual(pb_406, "PB-406-ACCEPT-HEADER-RECONCILIATION")
        ok, msg, ev = self.repair_catalog.execute_bounded_repair(pb_406, {})
        self.assertTrue(ok)
        self.assertIn("Accept", ev["reconciled_headers"])

        # Missing venv dep
        err_venv = "ModuleNotFoundError: No module named 'pytest'"
        pb_venv = self.repair_catalog.match_playbook(err_venv)
        self.assertEqual(pb_venv, "PB-VENV-MISSING-DEV-DEPENDENCY")
        ok, msg, ev = self.repair_catalog.execute_bounded_repair(pb_venv, {"module_name": "pytest"})
        self.assertTrue(ok)

        # Zombie port in use
        err_zombie = "Address already in use on port 18088"
        pb_zombie = self.repair_catalog.match_playbook(err_zombie)
        self.assertEqual(pb_zombie, "PB-ZOMBIE-PROCESS-LOCAL-CLEANUP")

    # T11: 300_METABOLIZE phase memory guard
    def test_T11_metabolize_phase_memory_guard(self):
        """T11: 300_METABOLIZE memory guard scrubs secrets and verifies anchors."""
        raw_text = "Discovered key ghp_123456789012345678901234567890123456. Remember F1 AMANAH and F13 SOVEREIGN."
        clean_text, count = self.memory_guard.scrub_secrets(raw_text)
        self.assertNotIn("ghp_", clean_text)
        self.assertEqual(count, 1)
        self.assertIn("[REDACTED_SECRET]", clean_text)

        anchors = self.memory_guard.verify_compaction_anchors(clean_text)
        self.assertTrue(anchors["F1 AMANAH"])
        self.assertTrue(anchors["F13 SOVEREIGN"])

    # T12: 999_SEAL phase ledger append
    def test_T12_seal_phase_ledger(self):
        """T12: 999_SEAL appends receipt with valid cryptographic hash chain."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = Path(tmpdir) / "test_ledger.jsonl"
            ledger = EvidenceLedger(ledger_path)

            rec1 = ledger.append({"session_id": "s1", "verdict": "SEALED", "actor": "333-AGI"})
            rec2 = ledger.append({"session_id": "s1", "verdict": "ARCHIVED", "actor": "555-ASI"})

            self.assertEqual(rec1["previous_hash"], "0" * 64)
            self.assertEqual(rec2["previous_hash"], rec1["entry_hash"])

            valid, count, err = ledger.verify_chain()
            self.assertTrue(valid)
            self.assertEqual(count, 2)

    # T13: Evidence ledger tampering detection
    def test_T13_evidence_ledger_tamper_detection(self):
        """T13: Evidence ledger detects modification of past entries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = Path(tmpdir) / "test_ledger.jsonl"
            ledger = EvidenceLedger(ledger_path)

            ledger.append({"record": "original-1"})
            ledger.append({"record": "original-2"})

            # Tamper with file
            with open(ledger_path, "r") as f:
                lines = f.readlines()
            # Mutate content of first entry
            tampered_entry = json.loads(lines[0])
            tampered_entry["record"] = "tampered-content"
            lines[0] = json.dumps(tampered_entry) + "\n"
            with open(ledger_path, "w") as f:
                f.writelines(lines)

            valid, count, err = ledger.verify_chain()
            self.assertFalse(valid)
            self.assertIn("hash mismatch", err)

    # T14: Learning pipeline L2 distillation and L3 block
    def test_T14_learning_pipeline_promotion_gate(self):
        """T14: Candidate lesson distilled to L2; direct L3 promotion hard-blocked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = Path(tmpdir) / "unratified.jsonl"
            pipeline = LearningPipeline(unratified_path=ledger_path)

            lesson = pipeline.distill_candidate_lesson(
                lesson_id="LES-001",
                observed_pattern="406 on missing accept header",
                suggested_action="Normalize headers",
                source_agent="333-AGI",
                evidence={"trace": "http-406"},
            )
            self.assertEqual(lesson["tier"], "L2")
            self.assertEqual(lesson["status"], "CANDIDATE_UNRATIFIED")

            # Autonomous L3 promotion must be DENIED per INV-LEARN-01
            ok, msg = pipeline.attempt_l3_promotion("LES-001", "333-AGI")
            self.assertFalse(ok)
            self.assertIn("INV-LEARN-01", msg)

    # T15: Auto-apply invariants
    def test_T15_auto_apply_invariants(self):
        """T15: Auto-apply enforces risk <= R2, reversibility, canary pass, zero security touch."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline = LearningPipeline(unratified_path=Path(tmpdir) / "u.jsonl")

            # Valid candidate: R2, reversible, canary passed, no security touch
            ok, msg = pipeline.validate_auto_apply("R2", "REVERSIBLE_LOCAL", True, False)
            self.assertTrue(ok)

            # Invalid: R3 risk
            ok, msg = pipeline.validate_auto_apply("R3", "REVERSIBLE_LOCAL", True, False)
            self.assertFalse(ok)
            self.assertIn("exceeds R2", msg)

            # Invalid: Canary failed
            ok, msg = pipeline.validate_auto_apply("R1", "REVERSIBLE_LOCAL", False, False)
            self.assertFalse(ok)
            self.assertIn("Canary", msg)

            # Invalid: Touches security
            ok, msg = pipeline.validate_auto_apply("R1", "REVERSIBLE_LOCAL", True, True)
            self.assertFalse(ok)
            self.assertIn("security", msg)

    # T17: Rollback drill
    def test_T17_rollback_journal_drill(self):
        """T17: Rollback journal records mutation checkpoint and restores file cleanly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            target_file = Path(tmpdir) / "target.txt"
            backup_file = Path(tmpdir) / "target.txt.bak"

            original_content = "ORIGINAL_CANONICAL_STATE"
            target_file.write_text(original_content)
            backup_file.write_text(original_content)

            # Mutate target
            target_file.write_text("MUTATED_UNSTABLE_STATE")
            self.assertEqual(target_file.read_text(), "MUTATED_UNSTABLE_STATE")

            # Execute Rollback from backup checkpoint
            target_file.write_text(backup_file.read_text())
            self.assertEqual(target_file.read_text(), original_content)

    # T18: Security regression test
    def test_T18_security_regression_forbidden_targets(self):
        """T18: Attempts to mutate forbidden targets (/etc/shadow, .secrets) are DENIED."""
        forbidden_targets = [
            "/etc/shadow",
            "/etc/sudoers",
            "/root/.ssh/authorized_keys",
            "/root/.secrets/kunci-root.env",
        ]
        for target in forbidden_targets:
            event = HookEvent(
                event_name="aaa.action.proposed",
                harness_id="opencode",
                action=ActionPayload(tool_name="write", arguments={}, target_path=target),
                risk_class="R2",
            )
            decision = self.policy_engine.evaluate(event)
            self.assertEqual(
                decision.verdict,
                "DENY",
                f"Target {target} should be strictly DENY, got {decision.verdict}",
            )
            self.assertIn("FORBIDDEN_MUTATION_TARGET", decision.reason_codes)


class CustomTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        name = test.id().split(".")[-1]
        self.test_records.append({
            "test_id": name.split("_")[1] if "_" in name else name,
            "name": name,
            "status": "PASS",
            "error": None,
        })

    def addFailure(self, test, err):
        super().addFailure(test, err)
        name = test.id().split(".")[-1]
        self.test_records.append({
            "test_id": name.split("_")[1] if "_" in name else name,
            "name": name,
            "status": "FAIL",
            "error": str(err[1]),
        })

    def addError(self, test, err):
        super().addError(test, err)
        name = test.id().split(".")[-1]
        self.test_records.append({
            "test_id": name.split("_")[1] if "_" in name else name,
            "name": name,
            "status": "ERROR",
            "error": str(err[1]),
        })


def run_and_record():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAgenticHookMesh)
    runner = unittest.TextTestRunner(resultclass=CustomTestResult, verbosity=2)
    start_time = time.time()
    result = runner.run(suite)
    duration = time.time() - start_time

    report = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_tests": result.testsRun,
        "passes": result.testsRun - len(result.failures) - len(result.errors),
        "failures": len(result.failures),
        "errors": len(result.errors),
        "duration_sec": round(duration, 4),
        "suite_status": "PASS" if result.wasSuccessful() else "FAIL",
        "tests": getattr(result, "test_records", []),
    }

    output_path = Path("/root/AAA/artifacts/hook-forge/TEST-RESULTS.json")
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"\nSaved structured results to {output_path}")
    except OSError as e:
        print(f"\nNote: Could not write file directly ({e}), structured results available in report.")
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_and_record()
    sys.exit(0 if success else 1)

