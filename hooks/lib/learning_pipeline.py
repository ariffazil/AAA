#!/usr/bin/env python3
"""
learning_pipeline.py — Governed Learning Pipeline & Promotion Gates (L0–L4)
Canonical Path: /root/AAA/hooks/lib/learning_pipeline.py
Authority: AAA-HOOK-FORGE-V1.0 · Section 10 & governance/AAA-LEARNING-POLICY-V1.yaml

Enforces learning tier invariants:
- L0: Ephemeral working context
- L1: Session summary & carry-forward
- L2: Unratified candidate lesson distillation
- L3: Ratified operational artifacts (STRICT GATE)
- L4: Constitutional invariant changes (F13 ONLY, HARD BLOCK ON AUTO-PROMOTION)
"""

from __future__ import annotations

import fcntl
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from event_schema import canonical_json, utc_now_iso

UNRATIFIED_LEDGER_PATH = Path("/root/AAA/UNRATIFIED-LESSONS-LEDGER.jsonl")


class LearningPipeline:
    """Governs distillation of session insights into unratified candidates without illegal auto-promotion."""

    def __init__(self, unratified_path: Optional[Path] = None):
        self.unratified_path = unratified_path or UNRATIFIED_LEDGER_PATH
        self.unratified_path.parent.mkdir(parents=True, exist_ok=True)

    def distill_candidate_lesson(
        self,
        lesson_id: str,
        observed_pattern: str,
        suggested_action: str,
        source_agent: str,
        evidence: Dict[str, Any],
        risk_class: str = "R1",
    ) -> Dict[str, Any]:
        """Distills an observed pattern into an L2 candidate lesson record."""
        record = {
            "tier": "L2",
            "lesson_id": lesson_id,
            "status": "CANDIDATE_UNRATIFIED",
            "source_agent": source_agent,
            "risk_class": risk_class,
            "observed_pattern": observed_pattern,
            "suggested_action": suggested_action,
            "evidence": evidence,
            "timestamp": utc_now_iso(),
            "f13_ratified": False,
        }

        # Write to unratified ledger under flock
        with open(self.unratified_path, "a+", encoding="utf-8") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                f.write(json.dumps(record, separators=(",", ":")) + "\n")
                f.flush()
                os.fsync(f.fileno())
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

        return record

    def validate_auto_apply(
        self,
        risk_class: str,
        reversibility: str,
        canary_passed: bool,
        touches_security: bool,
    ) -> Tuple[bool, str]:
        """Validates if a candidate fix is eligible for autonomous local application.
        INV-LEARN-02: risk <= R2, reversible, canary passed, zero security touch.
        """
        if touches_security:
            return (False, "BLOCKED: Touches security/auth surface. Requires Arif/888.")

        if risk_class not in ("R0", "R1", "R2"):
            return (False, f"BLOCKED: Risk class {risk_class} exceeds R2 ceiling for autonomous apply.")

        if reversibility not in ("REVERSIBLE_LOCAL", "REVERSIBLE_WITH_CHECKPOINT"):
            return (False, f"BLOCKED: Reversibility {reversibility} is not local reversible.")

        if not canary_passed:
            return (False, "BLOCKED: Canary verification predicate failed.")

        return (True, "ELIGIBLE: Satisfies all autonomous local apply invariants.")

    def attempt_l3_promotion(self, lesson_id: str, actor_id: str) -> Tuple[bool, str]:
        """Hard-blocks autonomous L3 promotion attempts."""
        # Autonomous promotion to L3 is strictly blocked per INV-LEARN-01
        return (
            False,
            f"DENIED: INV-LEARN-01 violation. Autonomous promotion to L3 is prohibited for actor '{actor_id}'. Requires ratified test bake and sovereign approval.",
        )
