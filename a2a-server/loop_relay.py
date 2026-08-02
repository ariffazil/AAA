#!/usr/bin/env python3
"""
arifOS / AAA Federation — Governed Prompt Loop Relay (Phase 3 & 4)
DITEMPA BUKAN DIBERI — Forged, Not Given.

Validates candidate PromptLoopEnvelopes, evaluates the Zen Convergence Gate,
and manages delegated SCT context across inter-agent turns.
"""

import sys
import os
import json
import time
import hashlib
from datetime import datetime, timezone

SCHEMA_PATH = "/root/AAA/schemas/prompt-loop-envelope.schema.json"
REGISTRY_PATH = "/root/AAA/registries/AGENTS_UNIFIED.yaml"
LOG_PATH = "/root/AAA/logs/prompt_loop_relay.jsonl"

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

class PromptLoopRelay:
    def __init__(self, observe_only=True):
        self.observe_only = observe_only
        self.schema = self._load_schema()

    def _load_schema(self):
        if not os.path.exists(SCHEMA_PATH):
            raise FileNotFoundError(f"Schema not found: {SCHEMA_PATH}")
        with open(SCHEMA_PATH, "r") as f:
            return json.load(f)

    def validate_envelope(self, envelope: dict) -> tuple[bool, str]:
        """Validate envelope structure against schema rules."""
        required = self.schema.get("required", [])
        for field in required:
            if field not in envelope:
                return False, f"Missing required field: {field}"

        if envelope.get("via_agent") not in ["openclaw", "aaa-a2a"]:
            return False, f"Invalid via_agent: {envelope.get('via_agent')}"

        verdict = envelope.get("verdict")
        valid_verdicts = ["UNKNOWN", "CONTINUE", "SABAR", "HOLD", "SEAL", "VOID"]
        if verdict not in valid_verdicts:
            return False, f"Invalid verdict: {verdict}"

        if envelope.get("mutation_allowed") is not False:
            return False, "mutation_allowed must be false"

        return True, "VALID"

    def evaluate_zen_gate(self, envelope: dict, history: list = None) -> tuple[str, str]:
        """
        Phase 4 — Zen Convergence Gate
        Determines if the turn should CONTINUE, SABAR, HOLD, SEAL, or VOID.
        """
        turn_id = envelope.get("turn_id", 1)
        max_turns = envelope.get("max_turns", 3)

        if turn_id > max_turns:
            return "HOLD", f"Turn limit exceeded ({turn_id}/{max_turns})"

        sct = envelope.get("sct_ref", "")
        if not sct.startswith("sct_v1."):
            return "VOID", "Missing or invalid delegated SCT context"

        if history:
            # Check prompt repetition
            last_prompts = [h.get("prompt") for h in history]
            if envelope.get("prompt") in last_prompts:
                return "SABAR", "Duplicate prompt detected — loop converging or stagnating"

        if envelope.get("verdict") in ["HOLD", "VOID", "UNKNOWN"]:
            return envelope.get("verdict"), "Inherited restrictive verdict"

        return "CONTINUE", "Zen gate passed: constructive delta detected"

    def process_envelope(self, envelope: dict, history: list = None) -> dict:
        is_valid, msg = self.validate_envelope(envelope)
        if not is_valid:
            envelope["verdict"] = "VOID"
            envelope["reason"] = msg
            self._log(envelope)
            return envelope

        zen_verdict, zen_reason = self.evaluate_zen_gate(envelope, history)
        envelope["verdict"] = zen_verdict
        envelope["zen_reason"] = zen_reason
        envelope["processed_at"] = datetime.now(timezone.utc).isoformat()
        envelope["observe_only_mode"] = self.observe_only

        self._log(envelope)

        if self.observe_only:
            print(f"[RELAY] OBSERVE ONLY — Envelope {envelope.get('loop_id')} turn {envelope.get('turn_id')} evaluated as {zen_verdict} ({zen_reason}). Prompt NOT auto-forwarded.", file=sys.stderr)
        else:
            print(f"[RELAY] ACTIVE — Envelope {envelope.get('loop_id')} turn {envelope.get('turn_id')} dispatched.", file=sys.stderr)

        return envelope

    def _log(self, data: dict):
        with open(LOG_PATH, "a") as f:
            f.write(json.dumps(data) + "\n")

if __name__ == "__main__":
    relay = PromptLoopRelay(observe_only=True)
    sample_envelope = {
        "loop_id": "loop_20260802_a1b2c3d4",
        "turn_id": 1,
        "parent_turn_id": None,
        "from_agent": "hermes",
        "to_agent": "opencode",
        "via_agent": "openclaw",
        "prompt": "Evaluate code formatting in /root/AAA/registries/AGENTS_UNIFIED.yaml",
        "context_ref": "ref_20260802_001",
        "sct_ref": "sct_v1.delegated_hermes_to_opencode",
        "receipt_ref": "RECEIPT-2026-08-02-001",
        "entropy_receipt_ref": "ENTROPY-2026-08-02-001",
        "max_turns": 3,
        "mutation_allowed": False,
        "f13_override_available": True,
        "verdict": "CONTINUE",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    result = relay.process_envelope(sample_envelope)
    print("Test Relay Result:", json.dumps(result, indent=2))
